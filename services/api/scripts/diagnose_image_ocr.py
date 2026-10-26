"""
Diagnose OCR quality for a resume image and compare predictions.

Usage:
    python diagnose_image_ocr.py ".\resume_image_test.png"

Outputs are saved under LOCALAPPDATA, with a TEMP fallback.
Extracted text can contain personal information; keep diagnostic files private.
"""

import os
import re
import sys
import tempfile
from pathlib import Path

import pytesseract
import requests
from PIL import (
    Image,
    ImageOps,
    ImageEnhance,
    ImageFilter,
    UnidentifiedImageError,
)

# Allow running this helper from services/api/scripts while importing the API module.\nsys.path.insert(0, str(Path(__file__).resolve().parents[1]))\n\nfrom app import normalize_resume_text, TESSERACT_CMD


API_URL = "http://127.0.0.1:8000/predict"


def choose_output_dir() -> Path:
    """Find a writable diagnostics folder outside the project directory."""

    candidates = []

    local_app_data = os.environ.get("LOCALAPPDATA")
    if local_app_data:
        candidates.append(
            Path(local_app_data)
            / "ResumeClassification"
            / "ocr_diagnostics"
        )

    candidates.append(
        Path(tempfile.gettempdir())
        / "resumeclassification_ocr_diagnostics"
    )

    last_error = None

    for directory in candidates:
        try:
            directory.mkdir(parents=True, exist_ok=True)

            test_file = directory / ".write_test"
            test_file.write_text("ok", encoding="utf-8")
            test_file.unlink(missing_ok=True)

            return directory

        except OSError as exc:
            last_error = exc

    raise RuntimeError(
        f"Could not create a writable diagnostic folder: {last_error}"
    )


def redact(text: str) -> str:
    """Redact obvious contact details from the console preview."""

    text = re.sub(
        r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}",
        "[EMAIL REDACTED]",
        text,
        flags=re.I,
    )

    text = re.sub(
        r"https?://\S+|www\.\S+",
        "[URL REDACTED]",
        text,
        flags=re.I,
    )

    text = re.sub(
        r"(?:\+?\d[\d\s()\-]{7,}\d)",
        "[PHONE REDACTED]",
        text,
    )

    return text


def preprocess_image(image: Image.Image) -> Image.Image:
    """Apply basic image enhancement to improve OCR readability."""

    image = ImageOps.exif_transpose(image).convert("RGB")
    gray = ImageOps.grayscale(image)
    gray = ImageOps.autocontrast(gray)

    gray = ImageEnhance.Contrast(gray).enhance(1.35)

    gray = gray.resize(
        (
            int(gray.width * 1.6),
            int(gray.height * 1.6),
        ),
        Image.Resampling.LANCZOS,
    )

    gray = gray.filter(ImageFilter.MedianFilter(size=3))

    return gray.convert("RGB")


def count_words(text: str) -> int:
    return len(re.findall(r"\b[\w+#./-]+\b", text))


def call_api(text: str) -> dict:
    """Send extracted text to the running local API."""

    try:
        response = requests.post(
            API_URL,
            json={"prepared_text": text},
            timeout=120,
        )

        if response.ok:
            return response.json()

        return {
            "_error": (
                f"HTTP {response.status_code}: "
                f"{response.text[:300]}"
            )
        }

    except requests.RequestException as exc:
        return {"_error": f"API unavailable: {exc}"}


def main() -> int:
    if len(sys.argv) != 2:
        print(
            'Usage: python diagnose_image_ocr.py '
            '"C:\\path\\to\\resume_image.png"'
        )
        return 2

    source = Path(sys.argv[1]).expanduser()

    if not source.is_file():
        print(f"Image not found: {source}")
        print("Check the filename and run the command from your project folder.")
        return 2

    try:
        output_dir = choose_output_dir()
    except RuntimeError as exc:
        print(exc)
        return 1

    try:
        with Image.open(source) as image:
            image.load()
            original = ImageOps.exif_transpose(image).convert("RGB")

    except (UnidentifiedImageError, OSError) as exc:
        print(f"Could not open image: {exc}")
        return 1

    enhanced = preprocess_image(original)

    variants = [
        ("current_psm6", original, "--oem 3 --psm 6"),
        ("original_psm4", original, "--oem 3 --psm 4"),
        ("original_psm11", original, "--oem 3 --psm 11"),
        ("enhanced_psm6", enhanced, "--oem 3 --psm 6"),
        ("enhanced_psm11", enhanced, "--oem 3 --psm 11"),
    ]

    print(f"\nImage: {source.name}")
    print(f"Dimensions: {original.width} x {original.height}")
    print(f"Tesseract: {TESSERACT_CMD or 'Configured executable/PATH'}")
    print(f"Diagnostic output directory: {output_dir}")
    print("\nComparing OCR configurations...\n")

    successful_runs = 0

    for name, image, config in variants:
        try:
            raw_text = pytesseract.image_to_string(
                image,
                lang="eng",
                config=config,
            )

            text = normalize_resume_text(raw_text)

        except Exception as exc:
            print(
                f"{name}: OCR failed: "
                f"{type(exc).__name__}: {exc}\n"
            )
            continue

        output_file = output_dir / f"{name}.txt"

        try:
            output_file.write_text(text, encoding="utf-8")
            saved_location = str(output_file)

        except OSError as exc:
            saved_location = f"Not saved: {exc}"

        word_count = count_words(text)

        print("=" * 65)
        print(f"Configuration: {name}")
        print(f"Words extracted: {word_count}")
        print(f"Characters extracted: {len(text)}")
        print(f"Text file: {saved_location}")

        preview_lines = [
            line.strip()
            for line in text.splitlines()
            if line.strip()
        ]

        print("\nRedacted preview:")

        for line in preview_lines[:8]:
            print("  " + redact(line)[:200])

        if word_count < 30:
            print("\nPrediction skipped: too little text extracted.\n")
            continue

        result = call_api(text)

        if "_error" in result:
            print("\nPrediction error:", result["_error"])
            print()
            continue

        successful_runs += 1

        print("\nPredicted category:", result.get("predicted_category"))
        print("Prediction message:", result.get("prediction_message"))
        print("Token count:", result.get("token_count_before_truncation"))
        print("Prediction time (ms):", result.get("prediction_ms"))
        print("Evidence time (ms):", result.get("evidence_ms"))
        print("Total inference time (ms):", result.get("inference_ms"))
        print("Evidence message:", result.get("evidence_message"))
        print()

    print("=" * 65)
    print(f"Successful API comparisons: {successful_runs}/{len(variants)}")
    print(f"Diagnostic files location: {output_dir}")
    print(
        "\nCompare the saved OCR text with the image, especially "
        "Skills, Experience, Projects, and technology names."
    )
    print(
        "\nShare the configuration names, word counts, predicted "
        "categories, timings, and whether the important sections "
        "were extracted correctly. Do not share full OCR files "
        "containing personal details."
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
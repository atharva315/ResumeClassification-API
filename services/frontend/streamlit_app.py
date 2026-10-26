import os
from html import escape
from typing import Any

import requests
import streamlit as st

API_BASE_URL = os.getenv("API_BASE_URL", "http://api:8000").rstrip("/")
PREDICT_FILE_URL = f"{API_BASE_URL}/predict-file"
PREDICT_TEXT_URL = f"{API_BASE_URL}/predict"
MAX_TEXT_CHARS = 200_000

st.set_page_config(
    page_title="Resume Classification",
    page_icon="📄",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Keep styling restrained and let Streamlit's selected theme handle colours.
st.markdown(
    """
    <style>
      .block-container {
        max-width: 900px;
        padding-top: 2.4rem;
        padding-bottom: 3rem;
      }
      .page-kicker {
        font-size: 0.76rem;
        font-weight: 650;
        letter-spacing: 0.095em;
        text-transform: uppercase;
        opacity: 0.72;
        margin-bottom: 0.4rem;
      }
      div[data-testid="stVerticalBlock"] > div:has(> div > .result-primary) {
        margin-bottom: 0.4rem;
      }
      .result-label {
        font-size: 0.76rem;
        font-weight: 650;
        letter-spacing: 0.075em;
        text-transform: uppercase;
        opacity: 0.72;
        margin-bottom: 0.4rem;
      }
      .result-primary {
        font-size: clamp(1.65rem, 4vw, 2.15rem);
        line-height: 1.2;
        font-weight: 650;
        letter-spacing: -0.035em;
        margin: 0 0 0.35rem 0;
        overflow-wrap: anywhere;
      }
      .stButton > button {
        min-height: 2.7rem;
        font-weight: 600;
        border-radius: 0.45rem;
      }
      [data-testid="stFileUploader"] section {
        border-radius: 0.5rem;
      }
      footer { visibility: hidden; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="page-kicker">Resume Classification</div>', unsafe_allow_html=True)
st.title("Classify a resume")
st.caption("ModernBERT · 43 job categories")
st.divider()

if "classification_result" not in st.session_state:
    st.session_state.classification_result = None

request_kind = None
request_file_payload = None
request_text_payload = None

file_tab, text_tab = st.tabs(["Upload a file", "Paste resume text"])

with file_tab:
    with st.container(border=True):
        uploaded_file = st.file_uploader(
            "Resume file",
            type=["pdf", "docx", "txt", "png", "jpg", "jpeg"],
            help="PDF, DOCX, TXT, PNG, JPG, or JPEG. Maximum file size: 10 MB.",
            key="resume_file_upload",
        )
        st.caption("PDF, DOCX, TXT, PNG, JPG, or JPEG · Up to 10 MB")
        if st.button(
            "Classify resume",
            type="primary",
            use_container_width=True,
            disabled=uploaded_file is None,
            key="classify_file_button",
        ):
            request_kind = "file"
            request_file_payload = {
                "file": (
                    uploaded_file.name,
                    uploaded_file.getvalue(),
                    uploaded_file.type or "application/octet-stream",
                )
            }

with text_tab:
    with st.container(border=True):
        resume_text = st.text_area(
            "Resume text",
            placeholder="Paste the resume's professional summary, skills, experience, education, and projects…",
            height=260,
            max_chars=MAX_TEXT_CHARS,
            key="resume_text_input",
            help=f"Up to {MAX_TEXT_CHARS:,} characters. Include enough detail for a meaningful classification.",
        )
        st.caption(f"{len(resume_text):,} / {MAX_TEXT_CHARS:,} characters")
        if st.button(
            "Classify text",
            type="primary",
            use_container_width=True,
            disabled=not resume_text.strip(),
            key="classify_text_button",
        ):
            request_kind = "text"
            request_text_payload = {"prepared_text": resume_text}


def _response_detail(response: requests.Response) -> str:
    try:
        body = response.json()
    except ValueError:
        body = {"detail": response.text[:500]}

    detail: Any = body.get("detail") or body.get("message") or f"HTTP {response.status_code}"
    if isinstance(detail, list):
        messages = []
        for item in detail:
            if isinstance(item, dict) and item.get("msg"):
                messages.append(str(item["msg"]))
            elif item:
                messages.append(str(item))
        detail = "; ".join(messages) or f"HTTP {response.status_code}"
    elif isinstance(detail, dict):
        detail = detail.get("msg") or str(detail)
    return str(detail)


if request_kind:
    st.session_state.classification_result = None
    try:
        with st.spinner("Classifying resume…"):
            if request_kind == "file":
                response = requests.post(
                    PREDICT_FILE_URL,
                    files=request_file_payload,
                    timeout=(10, 180),
                )
            else:
                response = requests.post(
                    PREDICT_TEXT_URL,
                    json=request_text_payload,
                    timeout=(10, 180),
                )

        if not response.ok:
            st.session_state.classification_result = {
                "error": _response_detail(response)
            }
        else:
            try:
                result = response.json()
            except ValueError:
                result = None

            if not isinstance(result, dict):
                st.session_state.classification_result = {
                    "error": "The classification API returned an unexpected response. Please retry."
                }
            else:
                st.session_state.classification_result = {"result": result}
    except requests.Timeout:
        st.session_state.classification_result = {
            "error": "The request timed out. Please try again with a smaller file or shorter text."
        }
    except requests.RequestException:
        st.session_state.classification_result = {
            "error": "Unable to reach the classification service. Please try again when the API is available."
        }

classification_result = st.session_state.classification_result
if classification_result:
    st.divider()
    st.subheader("Result")

    if classification_result.get("error"):
        st.error(classification_result["error"])
    else:
        result = classification_result.get("result", {})
        predicted_category = result.get("predicted_category")

        if not predicted_category:
            st.warning(
                result.get("prediction_message")
                or "This resume could not be classified confidently. Add more relevant skills, experience, education, or project details and try again."
            )
        else:
            with st.container(border=True):
                st.markdown('<div class="result-label">Primary category</div>', unsafe_allow_html=True)
                st.markdown(
                    f'<div class="result-primary">{escape(str(predicted_category))}</div>',
                    unsafe_allow_html=True,
                )

            alternatives = result.get("other_categories") or []
            if alternatives:
                st.markdown("#### Alternative categories")
                rows = []
                for item in alternatives[:4]:
                    category = str(item.get("category") or "Unknown")
                    score = item.get("probability")
                    if isinstance(score, (int, float)):
                        percentage = score * 100 if 0 <= score <= 1 else score
                        score_text = f"{percentage:.2f}%"
                    else:
                        score_text = "—"
                    rows.append({"Category": category, "Score": score_text})

                st.dataframe(
                    rows,
                    hide_index=True,
                    use_container_width=True,
                    height=min(230, 42 + 35 * len(rows)),
                    column_config={
                        "Category": st.column_config.TextColumn("Category", width="large"),
                        "Score": st.column_config.TextColumn("Score", width="small"),
                    },
                )
            st.caption("Use this result as decision support; a person should review the resume before any hiring decision.")

st.divider()
st.caption("Resume Classification · ModernBERT")
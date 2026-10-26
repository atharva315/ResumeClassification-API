# Streamlit frontend

The Streamlit app is the user-facing interface for the ModernBERT resume classifier. It supports pasted resume text and PDF, DOCX, TXT, PNG, JPG and JPEG uploads, then displays the primary category and alternative predictions returned by FastAPI.

## API connection

The UI reads `API_BASE_URL` from the environment and defaults to `http://api:8000`. That default is appropriate when the UI and API share the Docker network `resume-net`. The local Docker Desktop Compose file overrides it to `http://host.docker.internal:8000` for a host-running API.

The UI calls `POST /predict` with JSON containing `prepared_text`, or `POST /predict-file` with the upload in multipart field `file`.

## Build and run

Build context: this directory (`services/frontend`).

```powershell
docker build -t resumeclassification-ui:local services/frontend
```

To run locally against an API already listening on the host, use the repository's `deploy/local/docker-compose.local.yml`.

Do not add API credentials or user resume files to the frontend source. Submitted content is sent to the API for inference; the app does not use a database for persistence.

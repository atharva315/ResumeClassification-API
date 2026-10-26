# Streamlit frontend

The Streamlit application is the user-facing interface for the ModernBERT resume classifier. It accepts pasted resume text and supported resume documents, sends the input to FastAPI, and displays the category returned by the model along with alternative predictions.

## API contract

The app reads `API_BASE_URL` from the environment. Its container default is `http://api:8000`, which resolves on the shared Docker network in the current AWS deployment. The local Docker Compose configuration uses `http://host.docker.internal:8000` when the API runs directly on the host.

- Text inference: `POST /predict` with JSON field `prepared_text`.
- File inference: `POST /predict-file` with the file in multipart field `file`.
- Response display: uses `predicted_category` and `other_categories` from the API response.

The UI does not load the model itself and does not use a database for resume persistence.

# Backend

FastAPI backend for the summarizer app. It accepts input text, sends it to Gemini through LangChain, and returns a summary.

## Requirements

- Python 3.14+
- A valid `GOOGLE_API_KEY`

## Setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file in this folder:

```env
GOOGLE_API_KEY=your_google_api_key_here
```

## Run the server

```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

## API

### `POST /Summarize`

Request body:

```json
{
  "text": "Long text to summarize",
  "length": "short",
  "format": "paragraph"
}
```

Response:

```json
{
  "summary": "Generated summary text"
}
```

## Notes

- The backend uses `ChatGoogleGenerativeAI` from LangChain.
- Swagger docs are available at `/docs`.

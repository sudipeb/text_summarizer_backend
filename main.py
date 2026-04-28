import os
import logging
from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from prompt import get_prompt
from dotenv import load_dotenv

## Loads .env credentials
load_dotenv()

log = logging.getLogger("backend")
app = FastAPI()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
    google_api_key=os.getenv("GOOGLE_API_KEY"),
)


class SummarizeRequest(BaseModel):
    text: str
    length: str
    format: str


async def call_llm(prompt_text: str) -> str:
    """Call the LLM once and handle errors gracefully (no retries).

    Raises HTTPException with appropriate status and message for the client.
    """
    try:
        response = await llm.ainvoke([HumanMessage(content=prompt_text)])
        return response.content

    except Exception as e:
        msg = str(e)
        status: Optional[int] = None

        # Try to extract an HTTP status code from common exception shapes
        if hasattr(e, "response") and getattr(e, "response") is not None:
            try:
                status = int(getattr(e, "response").status_code)
            except Exception:
                status = None
        elif hasattr(e, "status_code"):
            try:
                status = int(getattr(e, "status_code"))
            except Exception:
                status = None

        # Token finished / quota-like errors should be surfaced as 429
        if "token" in msg.lower() and "finished" in msg.lower():
            log.warning("Token finished/quota reached: %s", msg)
            raise HTTPException(status_code=429, detail="Model token quota exhausted. Try again later.")

        # Rate-limit detection
        if status == 429 or "rate limit" in msg.lower() or "too many requests" in msg.lower():
            log.warning("Rate limited by LLM provider: %s", msg)
            raise HTTPException(status_code=429, detail="Rate limited by LLM provider. Try again later.")

        # Fallback: internal server error with original message trimmed
        log.error("LLM call failed: %s", msg)
        raise HTTPException(status_code=500, detail=f"LLM error: {msg}")


@app.post("/Summarize")
async def summarize(req: SummarizeRequest):
    prompt = get_prompt()
    final_prompt = prompt.format(
        text=req.text,
        length=req.length,
        format=req.format,
    )

    summary = await call_llm(final_prompt)
    return {"summary": summary}
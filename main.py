import os
from fastapi import FastAPI
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from prompt import get_prompt
from dotenv import load_dotenv

##Loads .env credentials
load_dotenv()

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

@app.post("/Summarize")
async def summarize(req: SummarizeRequest):
    prompt = get_prompt()
    final_prompt = prompt.format(
        text=req.text,
        length=req.length,
        format=req.format,
    )
    response = await llm.ainvoke([HumanMessage(content=final_prompt)])

    return {"summary": response.content}
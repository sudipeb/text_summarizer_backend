from langchain_core.prompts import ChatPromptTemplate

def get_prompt():
    return ChatPromptTemplate.from_template("""
You are a professional summarizer.

Summarize the text based on instructions:

Length: {length}
Format: {format}

Rules:
- Be concise
- Do not add extra info

Text:
{text}
""")
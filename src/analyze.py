import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from src.prompts import RCA_PROMPT

load_dotenv()


def format_incidents(retrieved_docs) -> str:
    formatted = []
    for i, doc in enumerate(retrieved_docs, start=1):
        formatted.append(f"Incident {i}:\n{doc.page_content}")
    return "\n\n".join(formatted)


def analyze_root_cause(log_summary: str, suspicious_lines: list, retrieved_docs):
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    prompt = RCA_PROMPT.format(
        log_summary=log_summary,
        suspicious_lines="\n".join(suspicious_lines) if suspicious_lines else "None found",
        similar_incidents=format_incidents(retrieved_docs)
    )

    response = llm.invoke(prompt)
    return response.content
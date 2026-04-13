import json
from pathlib import Path
from typing import List, Dict

from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings


DATA_PATH = Path("data/incidents.json")
CHROMA_DIR = "chroma_db"


def load_incidents() -> List[Dict]:
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def build_documents(incidents: List[Dict]) -> List[Document]:
    docs = []
    for incident in incidents:
        content = f"""
Title: {incident['title']}
Symptoms: {incident['symptoms']}
Root Cause: {incident['root_cause']}
Resolution: {incident['resolution']}
Tags: {", ".join(incident['tags'])}
"""
        docs.append(
            Document(
                page_content=content.strip(),
                metadata={
                    "incident_id": incident["incident_id"],
                    "title": incident["title"]
                }
            )
        )
    return docs


def get_vectorstore():
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    incidents = load_incidents()
    docs = build_documents(incidents)

    vectorstore = Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        persist_directory=CHROMA_DIR
    )
    return vectorstore


def retrieve_similar_incidents(query: str, k: int = 3):
    vectorstore = get_vectorstore()
    return vectorstore.similarity_search(query, k=k)
from functools import lru_cache
from langchain_groq import ChatGroq
from app.config.settings import get_settings
from app.generation.prompts import GENERATION_PROMPT

@lru_cache
def get_generation_llm():
    s = get_settings()
    return ChatGroq(model=s.generation_model, temperature=s.generation_temperature, api_key=s.groq_api_key)

def build_context(docs):
    return "\n\n".join(
        f"SOURCE {i}\n3GPP TS 23.501\nSection: {d['section']}\nTitle: {d['title']}\n\n{d['text']}"
        for i, d in enumerate(docs, 1)
    )

def generate_answer(query, docs):
    response = get_generation_llm().invoke(
        GENERATION_PROMPT.format(query=query, context=build_context(docs))
    )
    return response.content.strip()

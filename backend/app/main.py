from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router


app = FastAPI(
    title="3GPP Corrective RAG API",
    version="1.0.0",
    description="Grounded 3GPP TS 23.501 RAG backend.",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router)


@app.get("/health")
def health():
    return {"status": "ok"}
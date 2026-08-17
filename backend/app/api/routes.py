from time import perf_counter
from fastapi import APIRouter
from pydantic import BaseModel, Field
from app.config.settings import get_settings
from app.graph.workflow import rag_graph

router = APIRouter(prefix="/api/v1", tags=["rag"])

class QueryRequest(BaseModel):
    query: str = Field(min_length=2, max_length=2000)

@router.post("/query")
def query_rag(request: QueryRequest):
    settings = get_settings()
    start = perf_counter()
    result = rag_graph.invoke({
        "original_query": request.query,
        "current_query": request.query,
        "retrieved_docs": [],
        "answer": "",
        "evaluation": {},
        "feedback": "",
        "iteration": 0,
        "max_iterations": settings.max_iterations,
        "latency": {},
    })
    return {
        "query": request.query,
        "answer": result["answer"],
        "evaluation": result["evaluation"],
        "latency_ms": round((perf_counter() - start) * 1000, 2),
        "stage_latency_ms": result.get("latency", {}),
        "iteration": result["iteration"],
    }

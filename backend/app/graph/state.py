from typing import Any, TypedDict

class RAGState(TypedDict, total=False):
    original_query: str
    current_query: str
    retrieved_docs: list[dict[str, Any]]
    answer: str
    evaluation: dict[str, Any]
    feedback: str
    iteration: int
    max_iterations: int
    latency: dict[str, float]

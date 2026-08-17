from time import perf_counter
from app.config.settings import get_settings
from app.retrieval.retriever import retrieve
from app.generation.generator import generate_answer
from app.evaluation.evaluator import evaluate_answer

def retrieve_node(state):
    t = perf_counter()
    docs = retrieve(state["current_query"])
    latency = state.get("latency", {})
    latency["retrieval_ms"] = round((perf_counter() - t) * 1000, 2)
    return {"retrieved_docs": docs, "latency": latency}

def generate_node(state):
    t = perf_counter()
    answer = generate_answer(state["current_query"], state["retrieved_docs"])
    latency = state.get("latency", {})
    latency["generation_ms"] = round((perf_counter() - t) * 1000, 2)
    return {"answer": answer, "latency": latency}

def evaluate_node(state):
    t = perf_counter()
    evaluation = evaluate_answer(
        state["original_query"], state["answer"], state["retrieved_docs"]
    )
    latency = state.get("latency", {})
    latency["evaluation_ms"] = round((perf_counter() - t) * 1000, 2)
    return {"evaluation": evaluation, "feedback": evaluation.get("feedback", ""), "latency": latency}

def rewrite_query_node(state):
    # Fast corrective query expansion; avoids a second LLM rewrite call.
    new_query = (
        f"{state['original_query']} "
        "3GPP TS 23.501 general functions responsibilities relevant "
        "Network Function interfaces procedures. "
        f"Evaluator feedback: {state.get('feedback','')}"
    ).strip()
    return {"current_query": new_query, "iteration": state["iteration"] + 1}

def route_after_evaluation(state):
    s = get_settings()
    ev = state["evaluation"]
    if ev.get("correct", False) and float(ev.get("score", 0)) >= s.min_accept_score:
        return "final"
    if state["iteration"] < state["max_iterations"]:
        return "rewrite"
    return "final"

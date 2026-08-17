from langgraph.graph import StateGraph, END
from app.graph.state import RAGState
from app.graph.nodes import retrieve_node, generate_node, evaluate_node, rewrite_query_node

def build_rag_graph():
    graph = StateGraph(RAGState)
    graph.add_node("retrieve", retrieve_node)
    graph.add_node("generate", generate_node)
    graph.add_node("evaluate", evaluate_node)
    graph.add_node("rewrite", rewrite_query_node)
    graph.set_entry_point("retrieve")
    graph.add_edge("retrieve", "generate")
    graph.add_edge("generate", "evaluate")
    graph.add_conditional_edges(
        "evaluate",
        lambda state: (
            "final"
            if state["evaluation"].get("correct", False)
            and state["evaluation"].get("score", 0) >= 0.90
            else ("rewrite" if state["iteration"] < state["max_iterations"] else "final")
        ),
        {"final": END, "rewrite": "rewrite"},
    )
    graph.add_edge("rewrite", "retrieve")
    return graph.compile()

rag_graph = build_rag_graph()

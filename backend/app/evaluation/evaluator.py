import json, re
from functools import lru_cache
from langchain_groq import ChatGroq
from app.config.settings import get_settings
from app.evaluation.prompts import EVALUATION_PROMPT
from app.generation.generator import build_context

@lru_cache
def get_evaluation_llm():
    s = get_settings()
    return ChatGroq(model=s.evaluation_model, temperature=s.evaluation_temperature, api_key=s.groq_api_key)

def evaluate_answer(query, answer, docs):
    try:
        response = get_evaluation_llm().invoke(
            EVALUATION_PROMPT.format(query=query, answer=answer, context=build_context(docs))
        )
        text = response.content.strip()
        text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.I)
        text = re.sub(r"\s*```$", "", text)
        evaluation = json.loads(text)

        required = ["correct","score","faithfulness","relevance","completeness",
                    "unsupported_claims","missing_important_points","feedback","retry_needed"]
        missing = [x for x in required if x not in evaluation]
        if missing:
            raise ValueError(f"Missing evaluator fields: {missing}")

        for key in ["score","faithfulness","relevance","completeness"]:
            evaluation[key] = max(0.0, min(1.0, float(evaluation[key])))

        if evaluation["unsupported_claims"] or evaluation["faithfulness"] < 0.80 or evaluation["relevance"] < 0.70:
            evaluation["correct"] = False
            evaluation["retry_needed"] = True

        return evaluation
    except Exception as exc:
        return {
            "correct": False, "score": 0.0, "faithfulness": 0.0,
            "relevance": 0.0, "completeness": 0.0, "claims": [],
            "unsupported_claims": [], "missing_important_points": [],
            "feedback": f"Evaluator error: {exc}", "retry_needed": True
        }

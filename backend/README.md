# 3GPP Corrective RAG Backend

Industry-style backend for a grounded 3GPP TS 23.501 RAG assistant.

## Flow

Query → Retrieval → Reranking → Grounded Generation → Claim Evaluation
→ Final OR Corrective Rewrite → Retrieval again.

## Structure

```text
backend/
├── app/
│   ├── api/routes.py
│   ├── config/settings.py
│   ├── evaluation/{evaluator.py,prompts.py}
│   ├── generation/{generator.py,prompts.py}
│   ├── graph/{state.py,nodes.py,workflow.py}
│   ├── ingestion/{loader.py,chunker.py,indexer.py}
│   ├── retrieval/{embeddings.py,reranker.py,retriever.py}
│   └── main.py
├── data/raw/3gpp/
├── data/indexes/faiss/
├── scripts/build_index.py
├── tests/
├── .env.example
├── .gitignore
├── pyproject.toml
└── README.md
```

## Run

```powershell
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -e .
copy .env.example .env
```

Put `23501-j80.docx` in `data/raw/3gpp/`, then:

```powershell
python scripts/build_index.py
uvicorn app.main:app --reload
```

API:
`POST /api/v1/query`

Example body:

```json
{"query":"What is the role of the AMF in the 5G Core Network?"}
```

The system deliberately keeps corrective RAG as a fallback rather than
running rewrite/evaluation loops unnecessarily.


3GPP RAG Chatbot

A 3GPP standards-based Retrieval-Augmented Generation (RAG) chatbot with a FastAPI backend and modern frontend. The system is designed to provide grounded answers using 3GPP standards documentation while minimizing hallucinations.

Project Structure
3GP_RAG/
├── backend/
│   ├── app/
│   ├── data/
│   ├── requirements.txt
│   └── ...
│
└── 3gpp-rag-frontend/
    ├── package.json
    ├── src/
    └── ...
Architecture
                    ┌─────────────────────┐
                    │       User          │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │      Frontend       │
                    │   React / Vite      │
                    └──────────┬──────────┘
                               │
                         HTTP API
                               │
                               ▼
                    ┌─────────────────────┐
                    │   FastAPI Backend   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    RAG Pipeline     │
                    └──────────┬──────────┘
                               │
                ┌──────────────┴──────────────┐
                ▼                             ▼
        ┌───────────────┐             ┌───────────────┐
        │ FAISS Search  │             │ 3GPP Index    │
        │ Vector Search │◄────────────│ Embeddings    │
        └───────┬───────┘             └───────────────┘
                │
                ▼
        ┌──────────────────┐
        │ CrossEncoder     │
        │ Reranking        │
        └────────┬─────────┘
                 │
                 ▼
        ┌──────────────────┐
        │ Relevant 3GPP    │
        │ Context          │
        └────────┬─────────┘
                 │
                 ▼
        ┌──────────────────┐
        │ LLM Generation   │
        │ GPT-OSS-120B     │
        │ via Groq         │
        └────────┬─────────┘
                 │
                 ▼
        ┌──────────────────┐
        │ Grounded Answer  │
        └────────┬─────────┘
                 │
                 ▼
              Frontend
RAG Flow
User Query
    ↓
Query Embedding
    ↓
FAISS Retrieval
    ↓
Top Candidate Documents
    ↓
CrossEncoder Reranking
    ↓
Relevant 3GPP Context
    ↓
LLM Generation
    ↓
Grounded Response
    ↓
Frontend

1. Clone the Repository
   git clone https://github.com/Rohit2332000/3GP_RAG_Backend.git
   cd 3GP_RAG_Backend
2. Start the Backend

Open Terminal 1.

cd backend

Create a virtual environment:

python -m venv venv
Windows
venv\Scripts\activate
Linux/macOS
source venv/bin/activate

Install dependencies:

pip install -r requirements.txt
Configure Environment Variables

Create:

backend/.env

Add:

GROQ_API_KEY=your_groq_api_key

GENERATION_MODEL=openai/gpt-oss-120b
EVALUATION_MODEL=openai/gpt-oss-120b

GENERATION_TEMPERATURE=0
EVALUATION_TEMPERATURE=0

FETCH_K=30
TOP_K=5

Start FastAPI:

uvicorn app.main:app --reload --port 8000

Backend:

http://localhost:8000

Swagger:

http://localhost:8000/docs

Keep Terminal 1 running.

3. Start the Frontend

Open Terminal 2.

From the project root:

cd 3gpp-rag-frontend

Install dependencies:

npm install

Start the frontend:

npm run dev

The frontend will normally be available at:

http://localhost:5173

Open the displayed URL in your browser.

Run npm install only during the initial setup or when frontend dependencies change.

4. Run Order
   Terminal 1 — Backend
   cd backend
   venv\Scripts\activate
   uvicorn app.main:app --reload --port 8000
   Terminal 2 — Frontend
   cd 3gpp-rag-frontend
   npm install
   npm run dev

Start the backend first, then start the frontend.

5. Key Technologies
   Python
   FastAPI
   LangChain / LangGraph
   FAISS
   Sentence Transformers
   CrossEncoder Reranker
   Groq / GPT-OSS-120B
   React / Vite
   3GPP Standards Documentation
   Embedding Model
   sentence-transformers/all-MiniLM-L6-v2
   Reranker
   cross-encoder/ms-marco-MiniLM-L-6-v2
6. Hallucination Reduction

The system focuses on grounded responses using:

3GPP standards as the primary knowledge source
Semantic vector retrieval
CrossEncoder reranking
Context-based generation
Deterministic temperature (0)
Retrieval and answer evaluation

The LLM is provided with relevant retrieved standards context instead of relying only on its pretrained knowledge.

7. Important

Make sure the backend is running before using the frontend.

Verify the backend through:

http://localhost:8000/docs

If the frontend cannot connect to the backend, verify that it is configured to use:

http://localhost:8000

Never commit .env, API keys, or other secrets to GitHub.

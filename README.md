# 3GPP RAG Chatbot

A 3GPP standards-based **Retrieval-Augmented Generation (RAG)** chatbot with a FastAPI backend and modern frontend. The system is designed to provide grounded answers using 3GPP standards documentation while minimizing hallucinations.

## Project Structure

```text
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
```

---

# Architecture

```text
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
```

### RAG Flow

```text
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
```

---

# 1. Clone the Repository

```bash
git clone https://github.com/Rohit2332000/3GP_RAG_Backend.git
cd 3GP_RAG_Backend
```

---

# 2. Start the Backend

Open **Terminal 1**.

```bash
cd backend
```

Create a virtual environment:

```bash
python -m venv venv
```

### Windows

```powershell
venv\Scripts\activate
```

### Linux/macOS

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Configure Environment Variables

Create:

```text
backend/.env
```

Add:

```env
GROQ_API_KEY=your_groq_api_key

GENERATION_MODEL=openai/gpt-oss-120b
EVALUATION_MODEL=openai/gpt-oss-120b

GENERATION_TEMPERATURE=0
EVALUATION_TEMPERATURE=0

FETCH_K=30
TOP_K=5
```

Start FastAPI:

```bash
uvicorn app.main:app --reload --port 8000
```

Backend:

```text
http://localhost:8000
```

Swagger:

```text
http://localhost:8000/docs
```

Keep Terminal 1 running.

---

# 3. Start the Frontend

Open **Terminal 2**.

From the project root:

```bash
cd 3gpp-rag-frontend
```

## Configure Frontend Environment Variables

Create:

```text
3gpp-rag-frontend/.env
```

Add:

```env
VITE_API_URL=http://127.0.0.1:8000/api/v1
```

Install dependencies:

```bash
npm install
```

Start the frontend:

```bash
npm run dev
```

The frontend will normally be available at:

```text
http://localhost:5173
```

Open the displayed URL in your browser.

> Run `npm install` only during the initial setup or whenever frontend dependencies change.

---

# 4. Run Order

### Terminal 1 — Backend

```bash
cd backend
venv\Scripts\activate
uvicorn app.main:app --reload --port 8000
```

### Terminal 2 — Frontend

```bash
cd 3gpp-rag-frontend
npm install
npm run dev
```

**Start the backend first, then start the frontend.**

---

# 5. Key Technologies

* **Python**
* **FastAPI**
* **LangChain / LangGraph**
* **FAISS**
* **Sentence Transformers**
* **CrossEncoder Reranker**
* **Groq / GPT-OSS-120B**
* **React / Vite**
* **3GPP Standards Documentation**

### Embedding Model

```text
sentence-transformers/all-MiniLM-L6-v2
```

### Reranker

```text
cross-encoder/ms-marco-MiniLM-L-6-v2
```

---

# 6. Hallucination Reduction

The system focuses on grounded responses using:

* 3GPP standards as the primary knowledge source
* Semantic vector retrieval
* CrossEncoder reranking
* Context-based generation
* Deterministic temperature (`0`)
* Retrieval and answer evaluation

The LLM is provided with relevant retrieved standards context instead of relying only on its pretrained knowledge.

---

# 7. Important

Make sure the backend is running before using the frontend.

Verify the backend through:

```text
http://localhost:8000/docs
```

The frontend is configured to communicate with:

```text
http://127.0.0.1:8000/api/v1
```

**Never commit `.env`, API keys, or other secrets to GitHub.**

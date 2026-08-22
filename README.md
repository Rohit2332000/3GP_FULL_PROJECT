# 3GPP Standards-Based RAG Chatbot

## Project Design & Technical Architecture

**Project:** 3GPP Standards-Based Retrieval-Augmented Generation (RAG) Chatbot
**Repository:** https://github.com/Rohit2332000/3GP_FULL_PROJECT
**Backend Repository:** https://github.com/Rohit2332000/3GP_RAG_Backend
**Domain:** 3GPP / 5G Telecommunications Standards
**Backend:** Python + FastAPI
**Frontend:** React + Vite
**Workflow:** LangGraph
**Retrieval:** Sentence Transformers + FAISS
**Reranking:** Cross-Encoder
**Generation:** GPT-OSS-120B via Groq

---

# 1. Executive Summary

This project implements a **standards-grounded Retrieval-Augmented Generation (RAG) chatbot** designed to answer technical questions using **3GPP telecommunications specifications as the primary knowledge source**.

The main objective is to reduce hallucinations and improve answer reliability by retrieving relevant information from authoritative 3GPP documentation before generating an answer.

Unlike a conventional LLM chatbot, the system does not rely solely on the model's pretrained knowledge.

The system follows a multi-stage pipeline:

```text
User Query
    ↓
Query Processing
    ↓
Semantic Retrieval
    ↓
Cross-Encoder Reranking
    ↓
Relevant 3GPP Context
    ↓
LLM Generation
    ↓
Claim Extraction / Evaluation
    ↓
Citation & Evidence Mapping
    ↓
Corrective Generation if Required
    ↓
Final Grounded Answer
```

The final response can provide:

* the generated answer;
* individual claims;
* supporting evidence;
* source/citation information;
* correction when a claim is not sufficiently grounded.

The overall design focuses on **grounding, traceability, modularity, and evaluation**.

---

# 2. Problem Statement

3GPP specifications contain highly technical information covering:

* network architecture;
* network functions;
* interfaces;
* procedures;
* protocols;
* registration;
* mobility management;
* session management;
* security;
* system behaviour;
* technical requirements.

General-purpose LLMs can explain these concepts fluently, but they may also:

* generate unsupported information;
* mix information from different concepts;
* rely on pretrained knowledge rather than the requested specification;
* introduce plausible but incorrect technical details;
* provide answers without showing the evidence behind them.

For a standards-oriented application, fluent generation alone is not sufficient.

The system therefore follows an evidence-first design:

> **Retrieve relevant 3GPP evidence first, generate from that evidence, evaluate the generated claims, and provide source attribution wherever possible.**

---

# 3. Project Objectives

## 3.1 Standards-Grounded Question Answering

Use 3GPP specifications as the primary knowledge source for answering technical questions.

## 3.2 Hallucination Reduction

Reduce unsupported model-generated information using retrieval, reranking, grounded prompting, claim evaluation, and corrective generation.

## 3.3 High-Quality Retrieval

Retrieve semantically relevant passages even when the user's wording differs from the wording used in the specification.

## 3.4 Evidence-Based Answers

Ensure that the final answer is based on retrieved evidence rather than unrestricted model knowledge.

## 3.5 Claim-Level Verification

Break the generated response into claims and evaluate whether those claims are supported by the retrieved context.

## 3.6 Source Attribution

Provide source/citation information so users can trace the answer back to the relevant 3GPP material.

## 3.7 Corrective Generation

If the generated answer contains unsupported or weakly supported information, trigger a corrective step.

## 3.8 Full-Stack Implementation

Provide the complete system through:

* FastAPI backend;
* React/Vite frontend;
* retrieval pipeline;
* generation pipeline;
* evaluation workflow.

---

# 4. High-Level Architecture

```text
                         ┌───────────────────────┐
                         │         User          │
                         └───────────┬───────────┘
                                     │
                                     ▼
                         ┌───────────────────────┐
                         │   React + Vite UI     │
                         └───────────┬───────────┘
                                     │ HTTP
                                     ▼
                         ┌───────────────────────┐
                         │     FastAPI API       │
                         └───────────┬───────────┘
                                     │
                                     ▼
                         ┌───────────────────────┐
                         │    LangGraph Flow     │
                         └───────────┬───────────┘
                                     │
                                     ▼
                         ┌───────────────────────┐
                         │   Query Embedding     │
                         └───────────┬───────────┘
                                     │
                                     ▼
                         ┌───────────────────────┐
                         │   FAISS Retrieval     │
                         │  Candidate Retrieval  │
                         └───────────┬───────────┘
                                     │
                                     ▼
                         ┌───────────────────────┐
                         │  Cross-Encoder        │
                         │     Reranking         │
                         └───────────┬───────────┘
                                     │
                                     ▼
                         ┌───────────────────────┐
                         │  Relevant 3GPP        │
                         │       Context         │
                         └───────────┬───────────┘
                                     │
                                     ▼
                         ┌───────────────────────┐
                         │   GPT-OSS-120B        │
                         │       via Groq        │
                         └───────────┬───────────┘
                                     │
                                     ▼
                         ┌───────────────────────┐
                         │ Claim Evaluation      │
                         └───────────┬───────────┘
                                     │
                           ┌─────────┴─────────┐
                           │                   │
                       Supported          Unsupported
                           │                   │
                           ▼                   ▼
                       Citation           Corrective
                       Mapping            Generation
                           │                   │
                           └─────────┬─────────┘
                                     ▼
                         ┌───────────────────────┐
                         │ Final Answer + Claims │
                         │ + Source Citations   │
                         └───────────────────────┘
```

---

# 5. End-to-End Request Flow

A typical user request passes through the following stages:

```text
1. User submits a question
          ↓
2. React sends request to FastAPI
          ↓
3. Query is converted into an embedding
          ↓
4. FAISS retrieves candidate passages
          ↓
5. Cross-Encoder reranks candidates
          ↓
6. Relevant 3GPP context is selected
          ↓
7. GPT-OSS-120B generates a response
          ↓
8. Generated claims are evaluated
          ↓
9. Supporting sources are associated
          ↓
10. Unsupported content triggers correction
          ↓
11. Final grounded response is returned
```

---

# 6. Knowledge Source

The primary knowledge source for the project is **3GPP standards documentation**.

The system is designed so that the indexed standards become the source of evidence used during retrieval and generation.

This is important because the target domain is technical standards rather than general conversational knowledge.

The project therefore follows:

```text
3GPP Standards
       ↓
Knowledge Base
       ↓
Retrieval
       ↓
Evidence
       ↓
Answer
```

---

# 7. Knowledge Base Construction

The knowledge base is constructed through an offline ingestion pipeline.

```text
3GPP Specification
        ↓
Document Loading
        ↓
Text Extraction
        ↓
Text Cleaning
        ↓
Chunking
        ↓
Embedding Generation
        ↓
FAISS Index
        ↓
Persistent Retrieval Store
```

The ingestion stage is separated from online querying.

This avoids repeating expensive document processing every time a user asks a question.

---

# 8. Document Processing

The ingestion pipeline handles the source documents and converts them into searchable text units.

The process includes:

1. loading the source documents;
2. extracting text;
3. cleaning and normalizing the content;
4. splitting content into chunks;
5. generating embeddings;
6. creating the vector index.

The processed representation allows the retrieval system to search technical content efficiently.

---

# 9. Chunking Strategy

Large standards documents cannot efficiently be provided to an LLM as a single context.

The documents are therefore divided into smaller chunks.

The chunking strategy aims to maintain a balance between:

* context completeness;
* retrieval precision;
* embedding efficiency;
* LLM context size.

Overlapping chunks help reduce the possibility of losing information when a relevant statement occurs near a chunk boundary.

The project contains dedicated ingestion/chunking functionality so that chunking can be changed independently from retrieval and generation.

---

# 10. Embedding Model

The project uses a Sentence Transformer embedding model for semantic representation.

Configured embedding model:

```text
sentence-transformers/all-MiniLM-L6-v2
```

Each document chunk is transformed into a vector representation.

During querying, the user question is embedded using the same embedding model.

This creates a shared vector space in which semantic similarity can be calculated.

```text
Document Chunk
      ↓
Embedding Model
      ↓
Vector

User Query
      ↓
Embedding Model
      ↓
Query Vector
```

---

# 11. FAISS Vector Retrieval

FAISS is used for dense vector similarity search.

The retrieval stage compares the query embedding with the indexed document embeddings and returns a candidate set.

```text
User Query
    ↓
Query Embedding
    ↓
FAISS Similarity Search
    ↓
Candidate Passages
```

The system retrieves more candidates than the final context size so that a subsequent reranking stage can select the strongest evidence.

---

# 12. Why FAISS?

FAISS was selected because it provides:

* efficient vector similarity search;
* local index persistence;
* relatively low infrastructure complexity;
* fast candidate retrieval;
* easy integration with Python-based RAG systems.

It also avoids making the core retrieval layer dependent on a hosted vector database.

---

# 13. Cross-Encoder Reranking

Dense retrieval is efficient, but vector similarity alone does not always provide the best ranking.

The project therefore uses a second-stage Cross-Encoder reranker.

Configured reranker:

```text
cross-encoder/ms-marco-MiniLM-L-6-v2
```

The retrieval pipeline becomes:

```text
Query
  ↓
FAISS
  ↓
Candidate Passages
  ↓
Cross-Encoder
  ↓
Reranked Passages
  ↓
Top-K Context
```

The Cross-Encoder evaluates the query and candidate passage together.

This provides a more precise relevance signal before the passages are sent to the generation model.

---

# 14. Retrieval Architecture

The retrieval architecture follows a two-stage approach.

## Stage 1 — Candidate Retrieval

FAISS performs fast semantic search across the indexed knowledge base.

## Stage 2 — Precision Reranking

The Cross-Encoder evaluates the smaller candidate set and selects the most relevant passages.

This provides the following trade-off:

```text
FAISS
 ↓
Fast + Broad Retrieval
 ↓
Cross-Encoder
 ↓
Slower + More Precise Ranking
```

The expensive reranker is therefore not applied to the entire document collection.

---

# 15. Context Construction

After reranking, the highest-ranked passages are selected as the context provided to the LLM.

The generation input conceptually contains:

```text
User Question
+
Retrieved 3GPP Evidence
+
Grounding Instructions
```

This is preferable to sending the complete knowledge base to the model.

The context is therefore both:

* relevant to the current question;
* limited to the retrieved evidence.

---

# 16. LLM Generation

The project uses:

```text
openai/gpt-oss-120b
```

through Groq for response generation.

The model receives the user question together with the retrieved 3GPP context.

The generation configuration uses:

```text
temperature = 0
```

The purpose is to reduce unnecessary variability and encourage consistent outputs.

---

# 17. Grounded Generation Strategy

The generation stage follows an evidence-first principle.

The LLM is instructed to prioritize the retrieved 3GPP context rather than freely generating information from its pretrained knowledge.

Conceptually:

```text
Is the answer supported by the retrieved context?

        ┌──────────────┐
        │              │
       YES             NO
        │              │
        ▼              ▼
     Answer        Avoid invention /
                  request correction
```

This does not mathematically eliminate hallucinations.

Instead, it creates a controlled generation environment where the available evidence is explicitly provided to the model.

---

# 18. Claim-Level Grounding

One of the key features of the system is the ability to reason about the generated answer at the **claim level**.

A response may contain multiple technical statements:

```text
Answer
 ├── Claim 1
 ├── Claim 2
 └── Claim 3
```

Each claim can be evaluated against the retrieved context.

This is more informative than treating the entire response as one indivisible unit.

---

# 19. Claim-to-Evidence Architecture

The claim-level pipeline is:

```text
Generated Answer
       ↓
Claim Extraction
       ↓
Individual Claims
       ↓
Claim ↔ Retrieved Evidence
       ↓
Grounding Evaluation
       ↓
Supported / Unsupported
```

Conceptually:

```text
Claim 1 ─────► Evidence 1 ─────► Supported
Claim 2 ─────► Evidence 2 ─────► Supported
Claim 3 ─────► Evidence ? ─────► Unsupported
```

If a claim cannot be adequately supported by the retrieved evidence, it can be flagged for corrective processing.

---

# 20. Why Claim-Level Evaluation?

A complete answer may look correct while containing one unsupported statement.

For example:

```text
Claim A → Supported
Claim B → Supported
Claim C → Unsupported
```

A simple answer-level evaluation may not clearly expose this distinction.

Claim-level evaluation makes unsupported information more visible and allows the system to target correction at the problematic content.

This is particularly valuable for technical standards where a small incorrect detail can materially change the meaning of an answer.

---

# 21. Source Attribution and Citations

The system provides **source/citation information associated with the retrieved evidence used for answering the question**.

The objective is to allow the user to trace an answer back to the underlying 3GPP material.

Conceptually:

```text
Question
   ↓
Retrieved Chunk
   ↓
Document Metadata
   ↓
Source Reference
   ↓
Generated Claim
```

Depending on the indexed metadata, source information can identify:

* specification/document;
* section;
* source passage;
* retrieved chunk;
* document location/reference.

This makes the system more transparent than an LLM-only chatbot.

---

# 22. Why Citations Matter

Citations provide three major benefits.

### 22.1 Verifiability

Users can inspect the underlying standards content rather than relying entirely on the generated response.

### 22.2 Hallucination Detection

A claim without adequate supporting evidence becomes easier to identify.

### 22.3 Technical Trust

Engineers can trace the answer back to the source material and independently validate it.

The design therefore follows:

```text
Answer
  ↓
Claim
  ↓
Evidence
  ↓
Source
```

instead of:

```text
Question
  ↓
LLM
  ↓
Answer
```

---

# 23. Final Response Structure

The final response can contain three logically related components:

```text
┌────────────────────────────────────────┐
│                 ANSWER                 │
├────────────────────────────────────────┤
│ Generated technical explanation        │
├────────────────────────────────────────┤
│                 CLAIMS                 │
│                                        │
│ • Claim 1                              │
│ • Claim 2                              │
│ • Claim 3                              │
├────────────────────────────────────────┤
│             SOURCES / CITATIONS        │
│                                        │
│ • 3GPP source 1                        │
│ • 3GPP source 2                        │
│ • 3GPP source 3                        │
└────────────────────────────────────────┘
```

This structure makes the response more useful for technical users.

---

# 24. Corrective RAG

The system introduces a corrective step after answer generation.

The conceptual workflow is:

```text
Retrieved Context
       ↓
LLM Generation
       ↓
Claim Evaluation
       ↓
   ┌───────────────┐
   │ Grounded?     │
   └───────┬───────┘
           │
      ┌────┴────┐
      │         │
     YES        NO
      │         │
      ▼         ▼
   Return    Corrective
   Answer    Generation
                │
                ▼
           Final Answer
```

The correction stage is conditional.

It is not desirable to run additional LLM calls for every query because that would increase:

* latency;
* token usage;
* API cost;
* system complexity.

Conditional correction provides a better quality/cost trade-off.

---

# 25. Complete Grounding Pipeline

The full evidence-based generation pipeline is:

```text
3GPP Standards
       ↓
Document Ingestion
       ↓
Chunking
       ↓
Embeddings
       ↓
FAISS Retrieval
       ↓
Cross-Encoder Reranking
       ↓
Relevant Evidence
       ↓
LLM Generation
       ↓
Claim Extraction
       ↓
Claim ↔ Evidence Verification
       ↓
Citation Mapping
       ↓
 ┌───────────────────────┐
 │ Grounded / Supported? │
 └───────────┬───────────┘
             │
       ┌─────┴─────┐
       │           │
      YES          NO
       │           │
       ▼           ▼
    Final       Corrective
    Answer      Generation
       │           │
       └─────┬─────┘
             ▼
   Answer + Claims + Sources
```

---

# 26. Example Query

Example user question:

> What is the role of the AMF in the 5G Core Network?

The system processes the question as follows:

```text
Question
   ↓
Embedding
   ↓
FAISS Retrieval
   ↓
Candidate 3GPP Passages
   ↓
Cross-Encoder Reranking
   ↓
Top Relevant Passages
   ↓
GPT-OSS-120B
   ↓
Generated Answer
   ↓
Claims
   ↓
Claim Verification
   ↓
Source Mapping
   ↓
Final Response
```

The final response can contain an explanation along with the claims and supporting 3GPP source references.

---

# 27. Evaluation Strategy

Evaluation is treated as a separate engineering layer.

The project considers several dimensions of RAG quality.

## 27.1 Retrieval Quality

Measures whether relevant information is retrieved for a given question.

## 27.2 Context Relevance

Measures whether retrieved passages are actually useful for answering the question.

## 27.3 Faithfulness / Grounding

Measures whether the generated answer is supported by the retrieved context.

## 27.4 Answer Relevancy

Measures whether the generated answer directly addresses the user's question.

## 27.5 Corrective Effectiveness

Measures whether unsupported responses can be detected and improved.

The objective is to determine where failures occur:

```text
Question
   ↓
Retrieval?
   ↓
Reranking?
   ↓
Generation?
   ↓
Evaluation?
```

---

# 28. Golden Evaluation Dataset

A fixed evaluation dataset can be used to measure the system consistently.

A useful evaluation record contains:

```text
Question
Expected Relevant Document / Context
Expected Answer Characteristics
```

The dataset can be used for regression testing when changing:

* embedding models;
* chunking parameters;
* retrieval parameters;
* reranking models;
* prompts;
* generation models;
* evaluation logic.

This prevents improvements from being judged only through a small number of manual examples.

---

# 29. Retrieval vs Generation Evaluation

The project separates retrieval quality from generation quality.

## Retrieval Question

> Did the system retrieve the correct evidence?

## Generation Question

> Given the retrieved evidence, did the model produce a relevant and faithful answer?

This separation makes debugging significantly easier.

```text
Incorrect Final Answer
        ↓
Inspect Retrieved Context
        ↓
     Relevant?
     /       \
   NO         YES
   │           │
   ▼           ▼
Retrieval   Generation /
Problem     Prompt Problem
```

---

# 30. Backend Architecture

The backend is organized into separate modules for different responsibilities.

Conceptually:

```text
backend/
│
├── app/
│   ├── api/
│   ├── config/
│   ├── evaluation/
│   ├── generation/
│   ├── graph/
│   ├── ingestion/
│   ├── retrieval/
│   └── main.py
│
├── data/
│   ├── raw/
│   └── indexes/
│
├── scripts/
│
├── tests/
│
├── .env.example
├── Dockerfile
├── pyproject.toml
├── requirements.txt
└── uv.lock
```

The exact repository structure remains the source of truth for implementation-specific paths.

---

# 31. LangGraph Workflow

LangGraph is used to model the RAG workflow as explicit processing stages and state transitions.

Conceptually:

```text
START
  ↓
Retrieve
  ↓
Rerank
  ↓
Generate
  ↓
Evaluate
  ↓
 ┌──────────────┐
 │              │
PASS           FAIL
 │              │
 ▼              ▼
END          Correct
               │
               ▼
              END
```

This provides a cleaner workflow than placing the complete RAG process inside one large function.

Individual nodes can be:

* tested independently;
* modified independently;
* observed independently;
* reused in different workflows.

---

# 32. FastAPI Backend

FastAPI provides the API layer between the frontend and the RAG pipeline.

Primary query endpoint:

```text
POST /api/v1/query
```

Example request:

```json
{
  "query": "What is the role of the AMF in 5G?"
}
```

The API is responsible for:

* request validation;
* invoking the RAG workflow;
* returning the generated response;
* exposing the backend to the frontend.

FastAPI also provides interactive API documentation during local development.

---

# 33. Frontend Architecture

The frontend is implemented using:

```text
React
Vite
```

Its main responsibilities are:

1. accept user questions;
2. send requests to the backend;
3. display generated answers;
4. display claims and source information returned by the backend.

The frontend and backend remain independently deployable.

```text
User
 ↓
React
 ↓
HTTP
 ↓
FastAPI
 ↓
RAG Pipeline
 ↓
Response
 ↓
React
```

---

# 34. Configuration

Runtime configuration is managed using environment variables.

### Backend

```env
GROQ_API_KEY=your_groq_api_key

GENERATION_MODEL=openai/gpt-oss-120b
EVALUATION_MODEL=openai/gpt-oss-120b

GENERATION_TEMPERATURE=0
EVALUATION_TEMPERATURE=0

FETCH_K=30
TOP_K=5
```

### Frontend

```env
VITE_API_URL=http://127.0.0.1:8000/api/v1
```

Actual secrets must not be committed to the repository.

---

# 35. Security Considerations

For production deployment, the following controls should be applied:

* never commit API keys;
* use secure secret management;
* validate incoming requests;
* restrict CORS origins;
* add authentication where appropriate;
* apply rate limiting;
* monitor external API usage;
* avoid exposing sensitive information in logs;
* pin dependencies;
* regularly scan dependencies for vulnerabilities.

Retrieved document content should also be treated as untrusted data and should not be allowed to override system-level application controls.

---

# 36. Performance Considerations

The architecture uses multiple stages to balance retrieval quality and latency.

### FAISS

Provides fast candidate retrieval.

### Cross-Encoder

Provides higher-quality ranking over a smaller candidate set.

### LLM

Receives only selected context rather than the entire knowledge base.

### Corrective Generation

Runs conditionally instead of for every query.

Therefore:

```text
Fast Candidate Retrieval
        +
Focused Reranking
        +
Limited Context
        +
Conditional Correction
```

provides a practical quality/latency trade-off.

---

# 37. Maintainability

The architecture separates:

```text
Ingestion
Retrieval
Reranking
Generation
Evaluation
Workflow
API
Frontend
```

This makes individual components replaceable.

For example:

```text
Change Embedding Model
        ↓
Retrieval Layer Changes
        ↓
Frontend/API Remain Unchanged
```

Similarly, the LLM provider can be changed without requiring a redesign of the frontend.

---

# 38. Error Handling

Potential failure points include:

```text
Frontend
   ↓
API Validation
   ↓
Index Loading
   ↓
Embedding
   ↓
Retrieval
   ↓
Reranking
   ↓
LLM Provider
   ↓
Evaluation
```

Possible failures include:

* invalid requests;
* missing index files;
* embedding errors;
* model loading failures;
* API timeouts;
* API rate limits;
* malformed model output;
* external provider failures.

Clear component boundaries make these failures easier to diagnose.

---

# 39. Testing Strategy

The system should be tested at multiple levels.

## 39.1 Unit Tests

Test individual components such as:

```text
Chunker
Retriever
Reranker
Generator
Evaluator
```

## 39.2 Integration Tests

Test:

```text
API
 ↓
RAG Workflow
 ↓
Retrieval
 ↓
Generation
 ↓
Evaluation
 ↓
Response
```

## 39.3 Retrieval Evaluation

Use known questions and expected relevant documents/passages.

## 39.4 End-to-End Evaluation

Evaluate the complete pipeline:

```text
Question
   ↓
Retrieval
   ↓
Generation
   ↓
Claims
   ↓
Citations
   ↓
Final Answer
```

This layered strategy helps identify whether a failure originates from retrieval, generation, or evaluation.

---

# 40. Hallucination Reduction Strategy

The project uses multiple controls rather than relying on a single prompt.

```text
Authoritative 3GPP Documents
           ↓
Semantic Retrieval
           ↓
Cross-Encoder Reranking
           ↓
Evidence-Constrained Generation
           ↓
Claim-Level Evaluation
           ↓
Source Attribution
           ↓
Corrective Generation
```

Each layer addresses a different failure mode.

| Layer           | Purpose                                 |
| --------------- | --------------------------------------- |
| 3GPP source     | Domain-specific authoritative knowledge |
| Embeddings      | Semantic matching                       |
| FAISS           | Efficient retrieval                     |
| Cross-Encoder   | Retrieval precision                     |
| Grounded prompt | Evidence-constrained generation         |
| Claims          | Verifiable response units               |
| Evaluation      | Detect unsupported statements           |
| Citations       | Source traceability                     |
| Corrective RAG  | Repair unsupported output               |

No LLM system can guarantee absolute zero hallucinations. The goal of this architecture is instead to make unsupported information **less likely, detectable, traceable, and correctable**.

---

# 41. Deployment Architecture

The frontend and backend can be deployed independently.

```text
                   Internet
                      │
                      ▼
             ┌──────────────────┐
             │ React Frontend   │
             └────────┬─────────┘
                      │ HTTPS
                      ▼
             ┌──────────────────┐
             │ FastAPI Backend  │
             └────────┬─────────┘
                      │
              ┌───────┴────────┐
              │                │
              ▼                ▼
         FAISS / Models     Groq API
                           GPT-OSS-120B
```

The backend can be containerized and deployed separately from the frontend.

---

# 42. Complete Local Setup

## Prerequisites

Make sure the following are installed:

* Python 3.10+;
* Node.js and npm;
* Git;
* a Groq API key.

---

## 42.1 Clone the Repository

```bash
git clone https://github.com/Rohit2332000/3GP_RAG_Backend.git
cd 3GP_RAG_Backend
```

---

## 42.2 Start the Backend

Open **Terminal 1**.

Move into the backend directory:

```bash
cd backend
```

Create a Python virtual environment:

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

Install the backend dependencies:

```bash
pip install -r requirements.txt
```

---

## 42.3 Configure Backend Environment Variables

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

Replace `your_groq_api_key` with your actual Groq API key.

Do not commit `.env` or API keys to GitHub.

---

## 42.4 Start FastAPI

From the `backend` directory:

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

Keep **Terminal 1** running.

---

## 42.5 Start the Frontend

Open **Terminal 2**.

From the project root:

```bash
cd 3gpp-rag-frontend
```

Create:

```text
3gpp-rag-frontend/.env
```

Add:

```env
VITE_API_URL=http://127.0.0.1:8000/api/v1
```

Install frontend dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

The frontend will normally be available at:

```text
http://localhost:5173
```

Open the URL displayed by Vite in your browser.

Run `npm install` during the initial setup or whenever frontend dependencies change.

---

## 42.6 Complete Run Order

### Terminal 1 — Backend

```powershell
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

Start the **backend first**, then start the frontend.

---

## 42.7 Verify the Backend

Open:

```text
http://localhost:8000/docs
```

The Swagger UI should load successfully.

Primary RAG endpoint:

```text
POST /api/v1/query
```

The frontend communicates with:

```text
http://127.0.0.1:8000/api/v1
```

---

## 42.8 Local Application Flow

Once both services are running:

```text
Browser
   ↓
React + Vite
   ↓
VITE_API_URL
   ↓
FastAPI
   ↓
/api/v1/query
   ↓
LangGraph RAG Workflow
   ↓
FAISS Retrieval
   ↓
Cross-Encoder Reranking
   ↓
3GPP Context
   ↓
GPT-OSS-120B via Groq
   ↓
Claim / Grounding Evaluation
   ↓
Final Response
   ↓
React UI
```

---

# 43. Key Technologies

| Technology            | Purpose                            |
| --------------------- | ---------------------------------- |
| Python                | Backend and AI pipeline            |
| FastAPI               | REST API                           |
| LangChain             | LLM/RAG integration                |
| LangGraph             | Workflow orchestration             |
| FAISS                 | Vector similarity retrieval        |
| Sentence Transformers | Semantic embeddings                |
| Cross-Encoder         | Passage reranking                  |
| Groq                  | LLM inference                      |
| GPT-OSS-120B          | Response generation                |
| React                 | Frontend UI                        |
| Vite                  | Frontend development/build tooling |
| 3GPP Standards        | Primary knowledge source           |

### Embedding Model

```text
sentence-transformers/all-MiniLM-L6-v2
```

### Reranker

```text
cross-encoder/ms-marco-MiniLM-L-6-v2
```

### Generation Model

```text
openai/gpt-oss-120b
```

---

# 44. Example Grounded Response

For:

> What is the role of the AMF in the 5G Core Network?

the response can conceptually contain:

```text
Answer:

The AMF performs access and mobility management functions
within the 5G Core Network.

Claims:

1. The AMF performs access and mobility management functions.
2. The AMF participates in relevant access and mobility procedures.

Sources:

[1] 3GPP specification — relevant retrieved section
[2] 3GPP specification — relevant retrieved passage
```

The important architectural property is that the source information is associated with the retrieved evidence used during the answer-generation process.

---

# 45. Example Claim Verification

A generated answer might contain:

```text
Claim 1:
The AMF performs access and mobility management.
```

The evaluator checks the claim against retrieved context.

```text
Claim
  ↓
Retrieved Evidence
  ↓
Supported?
```

If supported:

```text
Claim → Accepted → Citation attached
```

If unsupported:

```text
Claim → Flagged → Corrective generation
```

This creates a traceable relationship:

```text
Question
   ↓
Retrieved Evidence
   ↓
Claim
   ↓
Verification
   ↓
Citation
```

---

# 46. Why This Architecture Is Suitable for Technical Standards

Standards-oriented systems have different requirements from general chatbots.

A typical chatbot primarily optimizes:

```text
Fluency
Engagement
Response Speed
```

This project instead prioritizes:

```text
Evidence
Grounding
Traceability
Correctness
Verification
```

The architecture therefore uses:

```text
Retrieval
+
Reranking
+
Grounded Generation
+
Claim Verification
+
Citations
+
Corrective Processing
```

This is better aligned with technical users who need to validate information against an authoritative source.

---

# 47. Key Engineering Decisions

| Engineering Decision  | Reason                            |
| --------------------- | --------------------------------- |
| RAG                   | Ground responses in 3GPP evidence |
| Sentence Transformers | Semantic representation           |
| FAISS                 | Efficient vector retrieval        |
| Cross-Encoder         | Improve ranking precision         |
| LangGraph             | Explicit workflow orchestration   |
| FastAPI               | Lightweight API layer             |
| React/Vite            | Independent web interface         |
| GPT-OSS-120B          | High-capability generation        |
| Groq                  | Fast LLM inference                |
| Temperature 0         | More deterministic generation     |
| Claim evaluation      | Detect unsupported statements     |
| Citations             | Provide source traceability       |
| Corrective RAG        | Improve weakly grounded responses |

---

# 48. Limitations

The system is designed to reduce hallucination risk but does not claim to mathematically eliminate hallucinations.

Important limitations include:

1. Answer quality depends on the indexed 3GPP documents.
2. Retrieval quality depends on chunking and embedding quality.
3. Dense retrieval may miss some exact technical terminology.
4. Cross-Encoder reranking adds inference latency.
5. LLM-based evaluation is not perfect.
6. External LLM APIs can introduce latency or availability issues.
7. New 3GPP releases require updating the knowledge base.
8. Citation quality depends on the metadata retained during ingestion.
9. The chatbot should not be considered a replacement for consulting the official 3GPP specification.

---

# 49. Future Improvements

## 49.1 Hybrid Retrieval

Combine dense vector retrieval with lexical/BM25 retrieval.

This can improve exact matching of:

* specification identifiers;
* technical abbreviations;
* interface names;
* section numbers;
* protocol terms.

## 49.2 Metadata-Aware Retrieval

Store metadata such as:

```text
Specification Number
Release
Section
Subsection
Document Title
Page / Location
```

This would allow more precise filtering and source attribution.

## 49.3 Citation-Aware Generation

Improve citation granularity by mapping individual claims directly to specification sections.

```text
Claim 1 → 3GPP Section 6.x
Claim 2 → 3GPP Section 7.x
Claim 3 → 3GPP Section 8.x
```

This would make technical verification even easier.

## 49.4 Retrieval Confidence

Introduce explicit retrieval confidence thresholds.

```text
Low Retrieval Confidence
        ↓
Do Not Guess
        ↓
Return Insufficient Evidence
```

This is preferable to generating a confident unsupported answer.

## 49.5 Automated Regression Testing

Run the golden dataset automatically whenever:

* retrieval logic changes;
* embedding models change;
* chunking changes;
* prompts change;
* LLM models change;
* evaluation logic changes.

This would help detect performance regressions before deployment.

## 49.6 Observability

Production monitoring can track:

```text
Retrieval Latency
Reranking Latency
Generation Latency
Total Latency
Retrieved Documents
Reranker Scores
Evaluation Results
Correction Frequency
Token Usage
API Errors
```

These metrics provide visibility into both quality and operational performance.

---

# 50. Recommended Evaluation Dashboard

A future evaluation dashboard could track:

```text
┌─────────────────────────────────────────┐
│              RAG Evaluation             │
├─────────────────────────────────────────┤
│ Retrieval Recall       █████████░  XX%  │
│ Context Relevance      █████████░  XX%  │
│ Faithfulness           ████████░░  XX%  │
│ Answer Relevancy       █████████░  XX%  │
│ Citation Coverage      █████████░  XX%  │
│ Correction Rate        ███░░░░░░░  XX%  │
│ Average Latency                    X sec │
└─────────────────────────────────────────┘
```

This allows changes to the system to be evaluated quantitatively.

---

# 51. Working Project Screenshots

The screenshots below demonstrate the **working implementation of the project**, including the chatbot interface, claims and citations, hallucination testing,  FastAPI Swagger documentation, and the overall system architecture.

### Chatbot Interface

![1787347990583](image/README/1787347990583.jpg)

### Claims and Citations

![1787348039894](image/README/1787348039894.jpg)

![1787348494325](image/README/1787348494325.jpg)

**Hallucination Testing**:

![1787348156788](image/README/1787348156788.jpg)

### FastAPI Swagger

![1787348676047](image/README/1787348676047.jpg)

### System Architecture

![1787349122402](image/README/1787349122402.png)

---


# 53. Design Principles

The project follows the following principles.

## Evidence Before Generation

Retrieve relevant standards evidence before generating an answer.

## Retrieval Before Reasoning

Do not provide the entire knowledge base to the LLM unnecessarily.

## Verify Before Returning

Do not assume that a fluent LLM response is automatically grounded.

## Claim-Level Transparency

Make individual technical claims easier to evaluate.

## Source Traceability

Provide source information so users can verify the response.

## Correct Conditionally

Use corrective generation when the initial response does not satisfy grounding requirements.

## Separate Components

Keep ingestion, retrieval, reranking, generation, evaluation, API, and frontend components modular.

## Measure Instead of Assuming

Use evaluation datasets and metrics to identify regressions.

---

# 54. Complete System Summary

The complete architecture can be summarized as:

```text
                    3GPP Standards
                          │
                          ▼
                   Document Ingestion
                          │
                          ▼
                       Chunking
                          │
                          ▼
                     Embeddings
                          │
                          ▼
                     FAISS Index
                          │
                          │
User ──► React ──► FastAPI ──► Retrieval
                              │
                              ▼
                       Cross-Encoder
                         Reranking
                              │
                              ▼
                       3GPP Evidence
                              │
                              ▼
                       GPT-OSS-120B
                          via Groq
                              │
                              ▼
                       Generated Answer
                              │
                              ▼
                       Claim Extraction
                              │
                              ▼
                    Claim Verification
                              │
                              ▼
                       Source Mapping
                              │
                    ┌─────────┴─────────┐
                    │                   │
                 Supported          Unsupported
                    │                   │
                    ▼                   ▼
                Citation           Corrective
                 Mapping            Generation
                    │                   │
                    └─────────┬─────────┘
                              ▼
                  Final Grounded Response
                              │
                    ┌─────────┴─────────┐
                    ▼                   ▼
                  Claims             Sources
```

---

# 55. Final Design Principle

The core principle of this project is:

> **Retrieve authoritative evidence → rerank the evidence → generate from the evidence → decompose the response into claims → verify claims against evidence → provide source attribution → correct unsupported content → return the grounded answer.**

The system is therefore designed not merely to answer questions, but to make the answers **grounded, inspectable, traceable, and correctable**.

---

# 56. Repository and Technical Information

**GitHub Repository:**
https://github.com/Rohit2332000/3GP_FULL_PROJECT

**Backend Repository:**
https://github.com/Rohit2332000/3GP_RAG_Backend

**Primary API Endpoint:**

```text
POST /api/v1/query
```

**Knowledge Domain:**

```text
3GPP Telecommunications Standards
```

**Embedding Model:**

```text
sentence-transformers/all-MiniLM-L6-v2
```

**Reranker:**

```text
cross-encoder/ms-marco-MiniLM-L-6-v2
```

**Generation Model:**

```text
openai/gpt-oss-120b
```

**LLM Provider:**

```text
Groq
```

**Application Stack:**

```text
React + Vite
        +
FastAPI
        +
LangGraph
        +
Sentence Transformers
        +
FAISS
        +
Cross-Encoder
        +
GPT-OSS-120B
        +
Claim / Grounding Evaluation
        +
Source Attribution
```

---

# Conclusion

This project demonstrates an end-to-end approach to building a **domain-specific, standards-grounded RAG system**.

The architecture goes beyond basic retrieval and generation by incorporating:

* semantic retrieval;
* Cross-Encoder reranking;
* evidence-constrained generation;
* claim-level evaluation;
* source attribution;
* corrective generation;
* retrieval and answer evaluation;
* modular backend architecture;
* full-stack API and frontend integration.

The resulting system is designed to provide technically useful answers while making the underlying evidence available for verification.

The key engineering objective is therefore:

> **Do not simply generate an answer. Retrieve the evidence, ground the answer in that evidence, verify the claims, and make the source traceable.**

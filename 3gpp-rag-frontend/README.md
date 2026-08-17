# 3GPP RAG Frontend

React + Vite frontend for the FastAPI 3GPP RAG backend.

## Run

npm install
npm run dev

Expected backend endpoint:
POST /query
Body: {"query":"What is the role of the AMF in the 5G Core Network?"}
Response: {"answer":"..."}

Set `VITE_API_URL` in `.env` if the backend is not at http://127.0.0.1:8000.

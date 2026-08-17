import React, { useState } from "react";
import { createRoot } from "react-dom/client";
import {
  Send,
  Sparkles,
  ShieldCheck,
  Database,
  Activity,
  BookOpen,
  Settings,
  Menu,
  X,
  Copy,
  Check,
  RotateCcw,
} from "lucide-react";

import "./styles.css";

const API =
  import.meta.env.VITE_API_URL || "http://127.0.0.1:8000/api/v1";

const examples = [
  "What is the role of the AMF in the 5G Core Network?",
  "What are the main functions of the UPF in the 5G Core Network?",
  "What is the role of the SMF in the 5G Core Network?",
  "How does the AMF handle paging in CM-IDLE state?",
];

function App() {
  const [q, setQ] = useState("");
  const [a, setA] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [copied, setCopied] = useState(false);
  const [side, setSide] = useState(false);

  const [history, setHistory] = useState([]);

  const [evaluation, setEvaluation] = useState({});
  const [latency, setLatency] = useState(null);
  const [stageLatency, setStageLatency] = useState({});
  const [iteration, setIteration] = useState(0);

  async function ask(question = q) {
    const x = question.trim();

    if (!x || loading) return;

    setQ(x);
    setLoading(true);
    setError("");
    setA("");

    setEvaluation({});
    setLatency(null);
    setStageLatency({});
    setIteration(0);

    try {
      const response = await fetch(`${API}/query`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          query: x,
        }),
      });

      if (!response.ok) {
        let errorMessage = `Request failed with status ${response.status}`;

        try {
          const errorData = await response.json();

          if (errorData.detail) {
            errorMessage =
              typeof errorData.detail === "string"
                ? errorData.detail
                : JSON.stringify(errorData.detail);
          }
        } catch {
          // Ignore JSON parsing errors
        }

        throw new Error(errorMessage);
      }

      const data = await response.json();

      const answer =
        data.answer ||
        data.response ||
        "No answer returned from the RAG system.";

      setA(answer);

      setEvaluation(data.evaluation || {});
      setLatency(data.latency_ms ?? null);
      setStageLatency(data.stage_latency_ms || {});
      setIteration(data.iteration ?? 0);

      setHistory((previous) => [
        {
          query: x,
          answer,
        },
        ...previous.filter((item) => item.query !== x),
      ].slice(0, 8));
    } catch (err) {
      console.error("RAG API Error:", err);

      setError(
        err.message ||
          "Could not connect to the backend. Make sure FastAPI is running and VITE_API_URL is correct."
      );
    } finally {
      setLoading(false);
    }
  }

  async function copyAnswer() {
    if (!a) return;

    try {
      await navigator.clipboard.writeText(a);

      setCopied(true);

      setTimeout(() => {
        setCopied(false);
      }, 1200);
    } catch (err) {
      console.error("Copy failed:", err);
    }
  }

  function newQuery() {
    setQ("");
    setA("");
    setError("");
    setEvaluation({});
    setLatency(null);
    setStageLatency({});
    setIteration(0);
  }

  function selectHistory(item) {
    setQ(item.query);
    setA(item.answer);
    setError("");
  }

  return (
    <div className="app">
      {/* HEADER */}
      <header>
        <button
          className="icon mobile"
          onClick={() => setSide(!side)}
          aria-label="Toggle sidebar"
        >
          {side ? <X /> : <Menu />}
        </button>

        <div className="brand">
          <div className="logo">
            <Sparkles />
          </div>

          <div>
            <b>3GPP RAG</b>
            <small>Technical Knowledge Assistant</small>
          </div>
        </div>

        <div className="right">
          <span className="online">
            <i />
            System Online
          </span>

          <button className="icon" aria-label="Settings">
            <Settings />
          </button>
        </div>
      </header>

      <div className="layout">
        {/* SIDEBAR */}
        <aside className={side ? "show" : ""}>
          <button className="new" onClick={newQuery}>
            ＋ New query
          </button>

          <label>SYSTEM</label>

          <div className="sidecard">
            <ShieldCheck />

            <div>
              <b>Grounded RAG</b>
              <small>3GPP evidence only</small>
            </div>
          </div>

          <div className="sidecard">
            <Database />

            <div>
              <b>FAISS Retrieval</b>
              <small>Semantic + reranking</small>
            </div>
          </div>

          <label>RECENT QUERIES</label>

          {history.length ? (
            history.map((item, index) => (
              <button
                className="history"
                key={`${item.query}-${index}`}
                onClick={() => selectHistory(item)}
              >
                {item.query}
              </button>
            ))
          ) : (
            <p className="empty">
              Your recent questions will appear here.
            </p>
          )}

          <div className="sidefoot">
            <div>
              <Activity />
              RAG pipeline <b>Ready</b>
            </div>

            <div>
              <BookOpen />
              Source <b>TS 23.501</b>
            </div>
          </div>
        </aside>

        {/* MAIN */}
        <main>
          {/* HERO */}
          <section className="hero">
            <span className="badge">
              <Sparkles />
              Evidence-grounded answers
            </span>

            <h1>
              Ask the 5G Core.
              <br />
              <em>Get specification-backed answers.</em>
            </h1>

            <p>
              Query your 3GPP knowledge base with concise answers
              grounded in retrieved specification evidence.
            </p>
          </section>

          {/* QUERY COMPOSER */}
          <section className="composer">
            <textarea
              value={q}
              onChange={(e) => setQ(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter" && !e.shiftKey) {
                  e.preventDefault();
                  ask();
                }
              }}
              placeholder="Ask about AMF, SMF, UPF, interfaces, procedures..."
              disabled={loading}
            />

            <div className="composefoot">
              <span>
                Enter to ask · Shift + Enter for new line
              </span>

              <button
                className="ask"
                disabled={!q.trim() || loading}
                onClick={() => ask()}
              >
                {loading ? (
                  <>
                    <i className="spinner" />
                    Searching
                  </>
                ) : (
                  <>
                    <Send />
                    Ask
                  </>
                )}
              </button>
            </div>
          </section>

          {/* EXAMPLES */}
          {!a && !loading && !error && (
            <section className="examples">
              <label>TRY AN EXAMPLE</label>

              <div className="grid">
                {examples.map((example, index) => (
                  <button
                    key={index}
                    onClick={() => ask(example)}
                  >
                    {example}
                    <span>↗</span>
                  </button>
                ))}
              </div>
            </section>
          )}

          {/* LOADING */}
          {loading && (
            <div className="answer loading">
              <div />
              <div />
              <div />

              <p>
                <i className="spinner" />
                Retrieving evidence and generating answer…
              </p>
            </div>
          )}

          {/* ERROR */}
          {error && (
            <div className="error">
              <b>Backend connection failed</b>

              <p>{error}</p>

              <button onClick={() => ask()}>
                <RotateCcw />
                Retry
              </button>
            </div>
          )}

          {/* ANSWER */}
          {a && !loading && (
            <section className="answer">
              <div className="answerhead">
                <div>
                  <label>
                    <ShieldCheck />
                    VERIFIED RESPONSE
                  </label>

                  <h2>Answer</h2>
                </div>

                <button onClick={copyAnswer}>
                  {copied ? <Check /> : <Copy />}
                  {copied ? "Copied" : "Copy"}
                </button>
              </div>

              <article>{a}</article>

              {/* RAG METRICS */}
              <div className="metrics">
                {latency !== null && (
                  <div>
                    <span>Total latency</span>
                    <b>{latency} ms</b>
                  </div>
                )}

                <div>
                  <span>Iterations</span>
                  <b>{iteration}</b>
                </div>

                {stageLatency &&
                  Object.entries(stageLatency).map(
                    ([stage, value]) => (
                      <div key={stage}>
                        <span>{stage}</span>
                        <b>{value} ms</b>
                      </div>
                    )
                  )}
              </div>

              {/* EVALUATION */}
              {evaluation &&
                Object.keys(evaluation).length > 0 && (
                  <div className="evaluation">
                    <div className="evaluation-title">
                      <ShieldCheck />
                      Evaluation
                    </div>

                    <div className="evaluation-grid">
                      {Object.entries(evaluation).map(
                        ([key, value]) => (
                          <div key={key}>
                            <span>{key}</span>
                            <b>
                              {typeof value === "number"
                                ? value.toFixed(3)
                                : String(value)}
                            </b>
                          </div>
                        )
                      )}
                    </div>
                  </div>
                )}

              <div className="evidence">
                <span>
                  <ShieldCheck />
                  Grounded in retrieved 3GPP evidence
                </span>

                <b>TS 23.501</b>
              </div>
            </section>
          )}

          {/* FOOTER */}
          <footer>
            3GPP RAG Assistant
            <span>•</span>
            Built for precise technical retrieval
          </footer>
        </main>
      </div>
    </div>
  );
}

createRoot(document.getElementById("root")).render(
  <App />
);
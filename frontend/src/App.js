import React, { useState } from "react";
import "./App.css";

function App() {
  const [pdfUrl, setPdfUrl] = useState("");
  const [question, setQuestion] = useState("");
  const [summary, setSummary] = useState([]);
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState("");
  const [paperLoaded, setPaperLoaded] = useState(false);
  const [depth, setDepth] = useState(5);

  const BACKEND_URL = "http://127.0.0.1:8000";

  // ✅ Correct: Process Paper
  const processPaper = async () => {
    try {
      setLoading(true);
      setStatus("📄 Processing research paper...");

      const res = await fetch(
        `${BACKEND_URL}/research/read?pdf_url=${encodeURIComponent(pdfUrl)}`,
        { method: "POST" }
      );

      const data = await res.json();

      if (data.error) {
        setStatus("❌ " + data.error);
        return;
      }

      setPaperLoaded(true);
      setStatus("✅ Paper processed successfully. You can now ask questions.");
    } catch {
      setStatus("❌ Backend not reachable.");
    } finally {
      setLoading(false);
    }
  };

  // ✅ Correct: Ask Question
  const askQuestion = async () => {
    try {
      setLoading(true);
      setStatus("🤖 Analyzing research...");

      const res = await fetch(
        `${BACKEND_URL}/research/ask?question=${encodeURIComponent(
          question
        )}&depth=${depth}`,
        { method: "POST" }
      );

      const data = await res.json();

      if (data.error) {
        setStatus("❌ " + data.error);
        return;
      }

      setSummary(data.summary || []);
      setStatus("📌 Research insights generated.");
    } catch {
      setStatus("❌ Failed to fetch answer.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <header>
        <h1>📚 ResearchPilot AI</h1>
        <p className="subtitle">Autonomous Research Intelligence Hub</p>
      </header>

      {/* STEP 1 */}
      <div className="step-card">
        <span className="step">STEP 1</span>
        <h3>Upload Research Paper (PDF URL)</h3>
        <input
          type="text"
          placeholder="https://arxiv.org/pdf/xxxx.pdf"
          value={pdfUrl}
          onChange={(e) => setPdfUrl(e.target.value)}
        />
        <button disabled={!pdfUrl || loading} onClick={processPaper}>
          Process Paper
        </button>
      </div>

      {/* STEP 2 */}
      <div className={`step-card ${!paperLoaded ? "disabled" : ""}`}>
        <span className="step">STEP 2</span>
        <h3>Ask Research Question</h3>

        <input
          type="text"
          placeholder="How does AI reduce carbon footprint?"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          disabled={!paperLoaded}
        />

        {/* ✅ Summary Depth Selector */}
        <select
          value={depth}
          onChange={(e) => setDepth(e.target.value)}
          disabled={!paperLoaded}
          style={{ marginTop: "10px", padding: "8px", borderRadius: "6px" }}
        >
          <option value="3">Short Summary</option>
          <option value="5">Medium Summary</option>
          <option value="8">Detailed Summary</option>
          <option value="12">Very Detailed</option>
        </select>

        <br /><br />

        <button
          disabled={!question || !paperLoaded || loading}
          onClick={askQuestion}
        >
          Ask
        </button>
      </div>

      {status && <div className="status">{status}</div>}
      {loading && <div className="loader"></div>}

      {summary.length > 0 && (
        <div className="result-card">
          <h3>📌 Research Summary</h3>
          <ul>
            {summary.map((point, idx) => (
              <li key={idx}>{point}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default App;

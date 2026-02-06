import { useState } from "react";
import api from "../services/api";
import NewsForm from "../components/NewsForm";
import ResultCard from "../components/ResultCard";

export default function Home() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [mode, setMode] = useState("text");
  const [url, setUrl] = useState("");
  const [error, setError] = useState(null);

  const analyzeText = async (text) => {
    if (!text.trim()) return;
    setLoading(true);
    setResult(null);
    setError(null);

    try {
      const res = await api.post("/predict/text", { text });
      setResult(res.data);
    } catch (err) {
      setError("Something went wrong while analyzing the text.");
    } finally {
      setLoading(false);
    }
  };

  const analyzeURL = async () => {
    if (!url.trim()) return;
    setLoading(true);
    setResult(null);
    setError(null);

    try {
      const res = await api.post("/predict/url", { url });

      // 👇 VERY IMPORTANT GUARD
      if (res.data?.error) {
        setError(res.data.error);
      } else {
        setResult(res.data);
      }
    } catch (err) {
      setError("Failed to analyze the article URL.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 to-slate-800 flex items-center justify-center px-4">
      <div className="w-full max-w-3xl bg-white rounded-2xl shadow-2xl p-8">

        {/* Header */}
        <h1 className="text-4xl font-extrabold text-slate-900 mb-2">
          Fake News Analyzer
        </h1>
        <p className="text-slate-600 mb-6">
          AI-powered detection with credibility scoring, explainability, and blockchain logging
        </p>

        {/* Mode Toggle */}
        <div className="flex gap-2 mb-6">
          <button
            type="button"
            className={`px-4 py-2 rounded ${
              mode === "text" ? "bg-slate-900 text-white" : "bg-slate-200"
            }`}
            onClick={() => setMode("text")}
          >
            Paste Text
          </button>

          <button
            type="button"
            className={`px-4 py-2 rounded ${
              mode === "url" ? "bg-slate-900 text-white" : "bg-slate-200"
            }`}
            onClick={() => setMode("url")}
          >
            Paste URL
          </button>
        </div>

        {/* Input Area */}
        {mode === "text" ? (
          <NewsForm onAnalyze={analyzeText} />
        ) : (
          <form
            className="space-y-4"
            onSubmit={(e) => {
              e.preventDefault();   // 🚫 stops redirect
              analyzeURL();
            }}
          >
            <input
              type="url"
              placeholder="Paste news article URL..."
              className="w-full p-4 border rounded-xl"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              required
            />
            <button
              type="submit"
              className="w-full bg-slate-900 text-white py-3 rounded-xl hover:bg-slate-800 transition"
            >
              Analyze URL
            </button>
          </form>
        )}

        {/* Loading */}
        {loading && (
          <div className="mt-6 flex items-center gap-3 text-slate-500">
            <div className="h-4 w-4 border-2 border-slate-400 border-t-transparent rounded-full animate-spin" />
            <span>Analyzing credibility…</span>
          </div>
        )}

        {/* Error */}
        {error && (
          <div className="mt-6 p-4 bg-red-100 text-red-700 rounded-lg">
            {error}
          </div>
        )}

        {/* Result */}
        {result && <ResultCard result={result} />}

        {/* Footer */}
        <p className="text-xs text-center text-gray-400 mt-8">
          Built with ML, FastAPI, React & Blockchain • Educational & Research Use
        </p>
      </div>
    </div>
  );
}

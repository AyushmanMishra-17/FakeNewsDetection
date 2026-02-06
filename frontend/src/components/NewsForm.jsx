import { useState } from "react";

export default function NewsForm({ onAnalyze }) {
  const [text, setText] = useState("");

  return (
    <div className="space-y-4">
      <textarea
        className="w-full p-4 border border-slate-300 rounded-xl resize-none focus:outline-none focus:ring-2 focus:ring-slate-800"
        rows="6"
        placeholder="Paste the full news article here..."
        value={text}
        onChange={(e) => setText(e.target.value)}
      />

      <button
        onClick={() => onAnalyze(text)}
        className="w-full bg-slate-900 text-white py-3 rounded-xl font-semibold hover:bg-slate-800 transition"
      >
        Analyze Credibility
      </button>
    </div>
  );
}

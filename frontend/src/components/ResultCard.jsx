import api from "../services/api";

export default function ResultCard({ result }) {
  const sendFeedback = async (label) => {
    await api.post("/feedback", {
      text: "",
      model_prediction: result.prediction,
      user_feedback: label
    });
    alert("Feedback recorded. Thank you!");
  };

  const ringColor =
    result.prediction === "Real" ? "stroke-green-500" : "stroke-red-500";

  return (
    <div className="space-y-6">

      {/* Verdict */}
      <div className="flex items-center justify-between">
        <h2 className="text-xl font-bold">Analysis Result</h2>
        <span className={`px-4 py-1 rounded-full text-white text-sm ${
          result.prediction === "Real" ? "bg-green-600" : "bg-red-600"
        }`}>
          {result.prediction}
        </span>
      </div>

      {/* Confidence Ring */}
      <div className="flex items-center gap-6">
        <svg className="w-24 h-24">
          <circle
            cx="48"
            cy="48"
            r="40"
            stroke="#e5e7eb"
            strokeWidth="8"
            fill="none"
          />
          <circle
            cx="48"
            cy="48"
            r="40"
            strokeWidth="8"
            fill="none"
            strokeDasharray={`${result.confidence * 2.5} 999`}
            className={ringColor}
          />
        </svg>

        <div>
          <p className="text-sm text-gray-500">Model confidence</p>
          <p className="text-2xl font-bold">{result.confidence}%</p>
          <p className="text-sm text-gray-500 mt-1">
            Credibility score: {result.credibility_score}/100
          </p>
        </div>
      </div>

      {/* Explainability */}
      <div>
        <p className="font-semibold mb-2">Key influencing terms</p>
        <div className="flex flex-wrap gap-2">
          {result.explanation.map((e, i) => (
            <span
              key={i}
              className="px-3 py-1 rounded-full text-xs bg-slate-100 border"
            >
              {e.word}
            </span>
          ))}
        </div>
      </div>

      {/* Feedback */}
      <div className="flex gap-3">
        <button
          onClick={() => sendFeedback(1)}
          className="flex-1 bg-green-600 text-white py-2 rounded-lg hover:bg-green-700 transition"
        >
          👍 Correct
        </button>
        <button
          onClick={() => sendFeedback(0)}
          className="flex-1 bg-red-600 text-white py-2 rounded-lg hover:bg-red-700 transition"
        >
          👎 Incorrect
        </button>
      </div>

      <p className="text-xs text-gray-400 break-all">
        Blockchain hash: {result.block_hash}
      </p>
    </div>
  );
}

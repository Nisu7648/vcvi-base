import React, { useState } from "react";
import { sendPrompt } from "../utils/api";

export default function ChatPanel({ logs, addLog }) {
  const [prompt, setPrompt] = useState("");
  const [project, setProject] = useState("demo_app");
  const [loading, setLoading] = useState(false);

  const handleSend = async () => {
    if (!prompt) return;
    setLoading(true);
    addLog(`🧠 Thinking about: ${prompt}`, "user");
    try {
      const res = await sendPrompt(project, prompt);
      addLog("✅ Thinker Plan:\n" + res.plan, "system");
      addLog("💻 Coder Output:\n" + res.review_notes, "system");
      addLog("📂 Saved File:\n" + res.file, "system");
    } catch (e) {
      addLog("❌ Error: " + e.message, "system");
    }
    setPrompt("");
    setLoading(false);
  };

  return (
    <div className="w-full max-w-3xl bg-gray-800 p-4 rounded-2xl shadow-lg">
      <div className="h-96 overflow-y-auto border border-gray-700 p-3 rounded-lg mb-3">
        {logs.map((l, i) => (
          <pre key={i} className={l.role === "user" ? "text-green-400" : "text-blue-300"}>
            {l.msg}
          </pre>
        ))}
      </div>
      <input
        className="w-full p-2 rounded-lg bg-gray-900 border border-gray-700 mb-2"
        placeholder="Describe your app..."
        value={prompt}
        onChange={e => setPrompt(e.target.value)}
      />
      <button
        onClick={handleSend}
        disabled={loading}
        className="w-full bg-blue-600 hover:bg-blue-700 text-white py-2 rounded-lg"
      >
        {loading ? "Building..." : "Send to VCVI"}
      </button>
    </div>
  );
}

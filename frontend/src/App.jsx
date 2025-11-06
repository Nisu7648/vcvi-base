import React, { useState } from "react";
import ChatPanel from "./components/ChatPanel";

export default function App() {
  const [logs, setLogs] = useState([]);

  const addLog = (msg, role = "system") => {
    setLogs(prev => [...prev, { msg, role }]);
  };

  return (
    <div className="min-h-screen bg-gray-950 text-white flex flex-col items-center justify-center p-6">
      <h1 className="text-3xl font-bold mb-4">VCVI Builder Chat</h1>
      <ChatPanel logs={logs} addLog={addLog} />
      <footer className="text-xs mt-4 opacity-50">
        Phase 3 Prototype · Thinker + Coder + Reviewer
      </footer>
    </div>
  );
}

import { useState } from "react";

export default function App() {
  const [desc, setDesc] = useState("");
  const [result, setResult] = useState(null);

  const build = async () => {
    const res = await fetch("/build", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ description: desc })
    });
    const data = await res.json();
    setResult(data);
  };

  return (
    <div className="p-10 text-center">
      <h1 className="text-2xl font-bold mb-4">🤖 VCVI AI App Builder</h1>
      <textarea
        value={desc}
        onChange={(e) => setDesc(e.target.value)}
        placeholder="Describe your app idea..."
        className="border rounded p-2 w-2/3 h-32"
      />
      <div>
        <button
          onClick={build}
          className="bg-blue-500 text-white px-4 py-2 rounded mt-3"
        >
          Build App
        </button>
      </div>
      {result && (
        <div className="mt-5 border p-4 text-left w-2/3 mx-auto bg-gray-50">
          <pre>{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

import React, { useState } from "react";
import axios from "axios";

const QueryBox = () => {
  const [query, setQuery] = useState("");
  const [answers, setAnswers] = useState([]);

  const handleQuery = async () => {
    try {
      const res = await axios.get(`http://localhost:8000/query?q=${query}`);
      setAnswers(res.data.answers);
    } catch (err) {
      setAnswers([{ content: "Query failed", meta: {} }]);
    }
  };

  return (
    <div className="bg-gray-800 p-4 rounded-lg shadow text-white">
      <h2 className="text-xl font-semibold mb-3">Ask a Question</h2>
      <input
        className="bg-gray-700 border border-gray-600 text-white px-3 py-2 w-full mb-3 rounded placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Type your question..."
      />
      <button
        className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded transition"
        onClick={handleQuery}
      >
        Ask
      </button>
      <ul className="mt-4 list-disc list-inside text-sm space-y-1">
        {answers.map((a, idx) => (
          <li key={idx}>{a.content}</li>
        ))}
      </ul>
    </div>
  );
};

export default QueryBox;

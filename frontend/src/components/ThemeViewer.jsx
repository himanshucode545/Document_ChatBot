import React, { useState } from "react";
import axios from "axios";

const ThemeViewer = () => {
  const [query, setQuery] = useState("");
  const [summary, setSummary] = useState("");

  const handleTheme = async () => {
    try {
      const res = await axios.get(`http://localhost:8000/theme?q=${query}`);
      setSummary(res.data.themes);
    } catch (err) {
      const backendMessage =
        err.response?.data?.error || "An unexpected error occurred.";
      setSummary(`Error: ${backendMessage}`);
    }
  };

  return (
    <div className="bg-gray-800 p-4 rounded-lg shadow text-white">
      <h2 className="text-xl font-semibold mb-3">Summarize Themes</h2>
      <input
        className="bg-gray-700 border border-gray-600 text-white px-3 py-2 w-full mb-3 rounded placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Ask to summarize themes..."
      />
      <button
        className="bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded transition"
        onClick={handleTheme}
      >
        Summarize
      </button>
      <div className="mt-4 whitespace-pre-wrap text-sm text-gray-200">
        {summary}
      </div>
    </div>
  );
};

export default ThemeViewer;

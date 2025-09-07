import React, { useState } from "react";
import api from "../services/api";

export default function BlogDetail({ blog }) {
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSummarize = async () => {
    setLoading(true);
    try {
      const res = await api.get(`/blogs/${blog.id}/summarize/`);
      setSummary(res.data.summary);
    } catch (err) {
      console.error(err);
      alert("Error generating summary");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h1 className="text-2xl font-bold">{blog.title}</h1>
      <p className="mt-4">{blog.content}</p>

      <button
        onClick={handleSummarize}
        className="bg-blue-600 text-white px-4 py-2 rounded mt-4"
      >
        {loading ? "Summarizing..." : "Summarize"}
      </button>

      {summary && (
        <div className="mt-4 p-4 bg-gray-100 rounded">
          <h3 className="font-semibold">AI Summary:</h3>
          <p>{summary}</p>
        </div>
      )}
    </div>
  );
}

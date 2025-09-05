import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import api from "../api/axiosInstance.jsx";

export default function BlogDetail() {
  const { id } = useParams();
  const [blog, setBlog] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    api.get("/api/blogs/").then(res => {
      const found = res.data.find(b => b.id === parseInt(id));
      setBlog(found);
    }).catch(console.error);
  }, [id]);

  const handleSummarize = () => {
    setLoading(true);
    api.post(`/api/blogs/${id}/summarize/`)
      .then(res => setBlog(prev => ({ ...prev, summary: res.data.summary })))
      .catch(err => alert("Unauthorized or error"))
      .finally(() => setLoading(false));
  };

  if (!blog) return <p className="p-4">Loading blog...</p>;

  return (
    <div className="p-6 max-w-2xl mx-auto">
      <h1 className="text-2xl font-bold mb-2">{blog.title}</h1>
      <p className="text-gray-600 mb-4">Author: {blog.author_name || "Anonymous"}</p>

      <div className="mb-6">
        <h2 className="text-lg font-semibold">Content</h2>
        <p className="mt-2 whitespace-pre-line">{blog.content}</p>
      </div>

      <div className="mb-6">
        <h2 className="text-lg font-semibold">Summary</h2>
        {blog.summary ? (
          <p className="mt-2 bg-gray-100 p-3 rounded">{blog.summary}</p>
        ) : (
          <p className="text-gray-500">No summary generated yet.</p>
        )}
      </div>

      <button onClick={handleSummarize} disabled={loading}
              className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600">
        {loading ? "Summarizing..." : "Generate Summary"}
      </button>
    </div>
  );
}

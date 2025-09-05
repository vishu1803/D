import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/axiosInstance.jsx";

export default function CreateBlog() {
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!title || !content) return alert("Please fill in both title and content!");
    setLoading(true);
    try {
      await api.post("/api/blogs/create/", { title, content });
      navigate("/");
    } catch (err) {
      alert("You must be logged in to create a blog.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6 max-w-xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">Create a New Blog</h1>
      <form onSubmit={handleSubmit} className="space-y-4">
        <input className="w-full p-2 border rounded" placeholder="Title"
               value={title} onChange={(e) => setTitle(e.target.value)} />
        <textarea className="w-full p-2 border rounded h-40" placeholder="Content"
                  value={content} onChange={(e) => setContent(e.target.value)} />
        <button type="submit" disabled={loading}
                className="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600">
          {loading ? "Posting..." : "Post Blog"}
        </button>
      </form>
    </div>
  );
}

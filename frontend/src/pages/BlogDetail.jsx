import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import api from "../services/api";
import CommentList from "../components/CommentList";


export default function BlogDetail() {
  const { id } = useParams();
  const [blog, setBlog] = useState(null);
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(false);

  // ✅ Fetch blog details
  useEffect(() => {
    api
      .get(`/blogs/${id}/`)
      .then((res) => setBlog(res.data))
      .catch((err) => console.error("Failed to load blog", err));
  }, [id]);

  // ✅ Summarize blog
  const handleSummarize = async () => {
    setLoading(true);
    try {
      const res = await api.get(`/blogs/${id}/summarize/`);
      setSummary(res.data.summary);
    } catch (err) {
      console.error(err);
      alert("Error generating summary");
    } finally {
      setLoading(false);
    }
  };

  // ✅ Toggle like
  const handleLike = async () => {
    try {
      await api.post(`/blogs/${id}/like/`);
      // Refresh blog data to update like count
      const res = await api.get(`/blogs/${id}/`);
      setBlog(res.data);
    } catch (err) {
      console.error("Error toggling like", err);
    }
  };

  if (!blog) return <p>Loading blog...</p>;

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold">{blog.title}</h1>
      <p className="mt-4">{blog.content}</p>

      {/* 🔹 Summarize button */}
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

      {/* 🔹 Like button */}
      <div className="mt-4">
        <button
          onClick={handleLike}
          className="bg-pink-500 text-white px-4 py-2 rounded"
        >
          {blog.is_liked ? "Unlike ❤️" : "Like 🤍"}
        </button>
        <span className="ml-2">{blog.likes_count} likes</span>
      </div>

      {/* 🔹 Comments (separate component) */}
      <div className="mt-6">
        <CommentList blogId={id} />
      </div>
    </div>
  );
}

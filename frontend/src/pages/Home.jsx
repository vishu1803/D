import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import api from "../api/axiosInstance.jsx";

export default function Home() {
  const [blogs, setBlogs] = useState([]);
  useEffect(() => {
  api.get("/api/blogs/")
    .then(res => setBlogs(res.data.results || [])) // <-- take "results"
    .catch(console.error);
}, []);
  return (
    <div className="p-4">
      <h1 className="text-xl font-bold mb-4">All Blogs</h1>
      {blogs.map(blog => (
        <div key={blog.id} className="border p-3 my-2 rounded">
          <h2 className="text-lg font-semibold">{blog.title}</h2>
          <p>{blog.summary ? blog.summary : blog.content.substring(0, 100) + "..."}</p>
          <p className="text-sm opacity-70">By {blog.author_name}</p>
          <Link to={`/blog/${blog.id}`} className="text-blue-500">Read More</Link>
        </div>
      ))}
      <Link to="/create" className="inline-block mt-4 px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600">
        Create Blog
      </Link>
    </div>
  );
}

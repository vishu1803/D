import React, { useEffect, useState } from "react";
import axios from "axios";

export default function BlogList() {
  const [blogs, setBlogs] = useState([]);
  const [nextPage, setNextPage] = useState(null);

  useEffect(() => {
    fetchBlogs("http://127.0.0.1:8000/api/blogs/?page=1&page_size=3");
  }, []);

  const fetchBlogs = async (url) => {
    const response = await axios.get(url, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("access")}`,
      },
    });
    setBlogs((prev) => [...prev, ...response.data.results]);
    setNextPage(response.data.next);
  };

  const toggleLike = async (blogId) => {
    try {
      await axios.post(
        `http://127.0.0.1:8000/api/blogs/${blogId}/like/`,
        {},
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access")}`,
          },
        }
      );

      // Refresh blog list after like/unlike
      setBlogs((prevBlogs) =>
        prevBlogs.map((b) =>
          b.id === blogId
            ? { ...b, likes_count: b.likes_count + (b.is_liked ? -1 : 1), is_liked: !b.is_liked }
            : b
        )
      );
    } catch (error) {
      console.error("Error liking blog:", error);
    }
  };

  return (
    <div className="max-w-3xl mx-auto p-4">
      {blogs.map((blog) => (
        <div
          key={blog.id}
          className="bg-white shadow rounded-xl p-4 mb-6 border"
        >
          {/* Blog Author Info */}
          <div className="flex items-center mb-3">
            <img
              src={blog.author.avatar || "https://i.pravatar.cc/100"}
              alt="avatar"
              className="w-10 h-10 rounded-full mr-3"
            />
            <div>
              <p className="font-semibold">{blog.author.username}</p>
              <p className="text-sm text-gray-500">{blog.author.bio}</p>
            </div>
          </div>

          {/* Blog Content */}
          <h2 className="text-xl font-bold mb-2">{blog.title}</h2>
          <p className="text-gray-700 mb-2">{blog.summary}</p>
          <p className="text-gray-500 text-sm">
            {new Date(blog.created_at).toLocaleString()}
          </p>

          {/* Likes + Like Button */}
          <div className="mt-3 flex items-center space-x-3">
            <button
              onClick={() => toggleLike(blog.id)}
              className={`px-3 py-1 rounded-lg text-sm ${
                blog.is_liked ? "bg-red-500 text-white" : "bg-gray-200 text-gray-700"
              }`}
            >
              {blog.is_liked ? "❤️ Unlike" : "🤍 Like"}
            </button>
            <span className="text-gray-600 text-sm">
              {blog.likes_count} {blog.likes_count === 1 ? "like" : "likes"}
            </span>
          </div>
        </div>
      ))}

      {/* Load More Button */}
      {nextPage && (
        <button
          onClick={() => fetchBlogs(nextPage)}
          className="bg-blue-500 text-white px-4 py-2 rounded-lg mt-4"
        >
          Load More
        </button>
      )}
    </div>
  );
}

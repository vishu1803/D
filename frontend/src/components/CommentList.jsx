import React, { useEffect, useState } from "react";
import axios from "axios";

export default function CommentList({ blogId }) {
  const [comments, setComments] = useState([]);
  const [nextPage, setNextPage] = useState(null);
  const [newComment, setNewComment] = useState("");

  useEffect(() => {
    fetchComments(`http://127.0.0.1:8000/api/blogs/${blogId}/comments/?page=1&page_size=3`);
  }, [blogId]);

  const fetchComments = async (url) => {
    const response = await axios.get(url, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("access")}`,
      },
    });
    setComments((prev) => [...prev, ...response.data.results]);
    setNextPage(response.data.next);
  };

  const postComment = async () => {
    if (!newComment.trim()) return;
    try {
      const response = await axios.post(
        `http://127.0.0.1:8000/api/blogs/${blogId}/comment/`,
        { content: newComment },
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access")}`,
          },
        }
      );
      setComments([response.data, ...comments]); // add new comment on top
      setNewComment("");
    } catch (error) {
      console.error("Error posting comment:", error);
    }
  };

  return (
    <div className="mt-4">
      <h3 className="font-semibold mb-2">Comments</h3>

      {/* Comment Input */}
      <div className="flex mb-4">
        <input
          type="text"
          value={newComment}
          onChange={(e) => setNewComment(e.target.value)}
          placeholder="Write a comment..."
          className="flex-1 border rounded-l-md px-3 py-2 text-sm"
        />
        <button
          onClick={postComment}
          className="bg-blue-500 text-white px-4 rounded-r-md text-sm"
        >
          Post
        </button>
      </div>

      {/* Existing Comments */}
      {comments.map((comment) => (
        <div key={comment.id} className="flex items-start mb-3">
          <img
            src={comment.author.avatar || "https://i.pravatar.cc/100"}
            alt="avatar"
            className="w-8 h-8 rounded-full mr-2"
          />
          <div>
            <p className="font-semibold text-sm">{comment.author.username}</p>
            <p className="text-gray-700 text-sm">{comment.content}</p>
            <p className="text-gray-400 text-xs">
              {new Date(comment.created_at).toLocaleString()}
            </p>
          </div>
        </div>
      ))}

      {/* Load More Button */}
      {nextPage && (
        <button
          onClick={() => fetchComments(nextPage)}
          className="bg-gray-200 px-3 py-1 rounded-md text-sm"
        >
          Load More
        </button>
      )}
    </div>
  );
}

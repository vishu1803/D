import React, { useState, useEffect } from "react";
import api from "../services/api"; // your axios instance

export default function Profile() {
  const [bio, setBio] = useState("");
  const [avatar, setAvatar] = useState(null); // uploaded file
  const [profile, setProfile] = useState(null);

  // Load current profile
  useEffect(() => {
    api.get("/auth/profile/")
      .then(res => setProfile(res.data))
      .catch(err => console.error(err));
  }, []);

  const handleFileChange = (e) => {
    setAvatar(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const formData = new FormData();
    formData.append("bio", bio);
    if (avatar) {
      formData.append("avatar", avatar);
    }

    try {
      const res = await api.put("/auth/profile/update/", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setProfile(res.data);
      alert("Profile updated!");
    } catch (error) {
      console.error(error);
      alert("Error updating profile");
    }
  };

  return (
    <div className="p-4">
      <h2 className="text-xl font-bold">My Profile</h2>

      {profile && (
        <div className="mb-4">
          <img
            src={profile.avatar || "https://via.placeholder.com/150"}
            alt="avatar"
            className="w-32 h-32 rounded-full mb-2"
          />
          <p><strong>Username:</strong> {profile.username}</p>
          <p><strong>Email:</strong> {profile.email}</p>
          <p><strong>Bio:</strong> {profile.bio}</p>
        </div>
      )}

      <form onSubmit={handleSubmit} className="flex flex-col gap-2">
        <textarea
          value={bio}
          onChange={(e) => setBio(e.target.value)}
          placeholder="Update your bio"
          className="border p-2"
        />
        <input type="file" onChange={handleFileChange} />
        <button
          type="submit"
          className="bg-blue-600 text-white px-4 py-2 rounded"
        >
          Update Profile
        </button>
      </form>
    </div>
  );
}

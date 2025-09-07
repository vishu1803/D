import axios from "axios";

// ✅ Axios instance
const api = axios.create({
  baseURL: "http://127.0.0.1:8000/api/",
});

// ✅ Google login function
export const loginWithGoogle = async (token) => {
  try {
    const response = await axios.post("http://127.0.0.1:8000/auth/google/", {
      access_token: token,
    });
    localStorage.setItem("access", response.data.access);
    localStorage.setItem("refresh", response.data.refresh);
    return response.data;
  } catch (error) {
    console.error("Google login failed", error);
  }
};

// ✅ Default export for other components
export default api;

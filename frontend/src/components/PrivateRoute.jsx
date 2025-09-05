import React, { useContext } from "react";
import { Navigate } from "react-router-dom";
import { AuthContext } from "../context/AuthContext.jsx";

export default function PrivateRoute({ children }) {
  const { user } = useContext(AuthContext);
  const hasToken = !!localStorage.getItem("access");
  return hasToken ? children : <Navigate to="/login" replace />;
}

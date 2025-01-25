import React from "react";
import { Navigate } from "react-router-dom";

// Mock function to get user role
const getUserRole = () => {
  // Example: Replace this with your actual logic to get the user's role
  return localStorage.getItem("userRole"); // "artisan" or "client"
};

function ProtectedRoute({ allowedRoles, children }) {
  const userRole = getUserRole();

  // If the user's role isn't allowed, redirect to NotFound
  if (!allowedRoles.includes(userRole)) {
    return <Navigate to="*" replace />;
  }

  return children;
}

export default ProtectedRoute;

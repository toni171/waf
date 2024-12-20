import { getToken } from '../auth';
import React from "react";
import { Navigate } from "react-router-dom";

function RequireAuth({ children }) {
    const token = getToken();
    if (!token) {
        return <Navigate to="/login" />;
    }
    return children;
}

export default RequireAuth;

import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import AddRule from "./components/AddRule";
import ViewRules from "./components/ViewRules";
import Monitoring from "./components/Monitoring";
import ViewLogs from "./components/ViewLogs";
import EditRule from "./components/EditRule";
import Login from './components/Login';
import RequireAuth from './components/RequireAuth';
import Home from './components/Home';

function App() {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<RequireAuth><Home /></RequireAuth>} />
                <Route path="/login" element={<Login />} />
                <Route path="/edit-rule/:id" element={<RequireAuth><EditRule /></RequireAuth>} />
                <Route path="/add-rule" element={<RequireAuth><AddRule /></RequireAuth>} />
                <Route path="/view-rules" element={<RequireAuth><ViewRules /></RequireAuth>} />
                <Route path="/monitoring" element={<RequireAuth><Monitoring /></RequireAuth>} />
                <Route path="/view-logs" element={<RequireAuth><ViewLogs /></RequireAuth>} />
            </Routes>
        </Router>
    );
}

export default App;

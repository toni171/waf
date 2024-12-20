import React from "react";
import { Link } from "react-router-dom";

const Home = () => {
    return (
        <div className="home-container">
            <h1>Admin Panel</h1>
            <p>Welcome to the Admin Panel. Select an option below:</p>
            <ul className="home-links">
                <li>
                    <Link to="/view-rules">View Rules</Link>
                </li>
                <li>
                    <Link to="/add-rule">Add Rule</Link>
                </li>
                <li>
                    <Link to="/monitoring">Real-Time Monitoring</Link>
                </li>
                <li>
                    <Link to="/view-logs">View Logs</Link>
                </li>
            </ul>
        </div>
    );
};

export default Home;

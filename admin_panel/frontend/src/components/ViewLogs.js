import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";

function ViewLogs() {
    const [logs, setLogs] = useState([]);

    useEffect(() => {
        async function fetchLogs() {
            const response = await fetch("http://localhost:8004/logs");
            const data = await response.json();
            setLogs(data);
        }
        fetchLogs();
    }, []);

    return (
        <div className="container">
            <h1>View Logs</h1>
            <Link to="/">Back to Home</Link>
            <ul>
                {logs.map((log) => (
                    <li key={log.id}>
                        {log.method} {log.url} - {log.status} ({log.timestamp})
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default ViewLogs;

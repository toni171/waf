import React, { useEffect, useState } from "react";
import { io } from "socket.io-client";
import { Link } from "react-router-dom";

function Monitoring() {
    const [logs, setLogs] = useState([]);

    useEffect(() => {
        // Connect to the monitoring service
        const socket = io(
            process.env.REACT_APP_MONITORING_URL || "http://localhost:8003",
            {
                transports: ["websocket", "polling"], // Ensure WebSocket fallback works
            }
        );

        // Handle successful connection
        socket.on("connect", () => {
            console.log("Connected to monitoring service");
        });

        // Handle disconnection
        socket.on("disconnect", () => {
            console.log("Disconnected from monitoring service");
        });

        // Listen for new logs
        socket.on("new_log", (data) => {
            console.log("New log received:", data);
            setLogs((prevLogs) => [data, ...prevLogs]); // Add new logs to the top
        });

        // Cleanup the socket connection on unmount
        return () => {
            socket.disconnect();
        };
    }, []);

    useEffect(() => {
        const fetchLogs = async () => {
            try {
                const response = await fetch(
                    `${process.env.REACT_APP_MONITORING_URL || "http://localhost:8003"}/logs`
                );
                if (response.ok) {
                    const data = await response.json();
                    console.log("Fetched logs:", data);
                    setLogs(data);
                } else {
                    console.error("Failed to fetch logs:", response.statusText);
                }
            } catch (error) {
                console.error("Error fetching logs:", error);
            }
        };

        fetchLogs();
    }, []);

    return (
        <div className="container monitoring">
            <h1>Real-Time Monitoring</h1>
            <Link to="/">Back to Home</Link>
            {logs.length === 0 ? (
                <p>No logs to display yet.</p>
            ) : (
                <ul className="logs-list">
                    {logs.map((log, index) => (
                        <li key={index}>
                            <strong>IP:</strong> {log.ip_address} |{" "}
                            <strong>Method:</strong> {log.method} |{" "}
                            <strong>URL:</strong> {log.url} |{" "}
                            <strong>Status:</strong> {log.status}
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
}

export default Monitoring;

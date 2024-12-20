import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";

function ViewRules() {
    const [rules, setRules] = useState([]);

    useEffect(() => {
        async function fetchRules() {
            try{
                const response = await fetch("http://localhost:8002/rules");
                const data = await response.json();
                setRules(data);
            } catch (error) {
                console.error("Error fetching rules:", error);
            }

        }
        fetchRules();
    }, []);

    async function fetchRule(id) {
        try {
            const response = await fetch(`http://localhost:8002/rules/${id}`);
            if (!response.ok) {
                throw new Error("Failed to fetch the rule.");
            }
            const data = await response.json();
            // Navigate to the edit page with rule data (or set state)
            console.log(data);
            window.location.href = `/edit-rule/${id}`;
        } catch (error) {
            console.error("Error fetching rule:", error);
        }
    }

    async function deleteRule(id) {
        try {
            await fetch(`http://localhost:8002/rules/${id}`, { method: "DELETE" });
            if (response.ok) {
                setRules(rules.filter((rule) => rule.id !== id));
            } else {
                alert("Failed to delete rule.")
            }
        } catch (error) {
            console.error("Error deleting rule:", error);
        }
    }


    return (
        <div className="container">
            <h1>View Rules</h1>
            <Link to="/">Back to Home</Link>
            <table>
                <thead>
                    <tr>
                        <th>Pattern</th>
                        <th>Type</th>
                        <th>Description</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {rules.map((rule) => (
                        <tr key={rule.id}>
                            <td>{rule.pattern}</td>
                            <td>{rule.rule_type}</td>
                            <td>{rule.description}</td>
                            <td>
                                <button onClick={() => fetchRule(rule.id)}>Edit</button>
                                <button onClick={() => deleteRule(rule.id)}>Delete</button>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}

export default ViewRules;

import React, { useState } from "react";
import { Link } from "react-router-dom";

function AddRule() {
    const [formData, setFormData] = useState({
        pattern: "",
        rule_type: "",
        description: "",
    });

    function handleChange(event) {
        const { name, value } = event.target;
        setFormData((prevData) => ({
            ...prevData,
            [name]: value,
        }));
    }

    async function handleSubmit(event) {
        event.preventDefault();
        try {
            const response = await fetch("http://localhost:8002/rules", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(formData),
            });
            if (response.ok) {
                alert("Rule added successfully!");
            } else {
                alert("Failed to add rule.");
            }
        } catch (error) {
            console.error("Error adding rule:", error);
        }
    };

    return (
        <div className="container">
            <h1>Add Rule</h1>
            <form onSubmit={handleSubmit}>
                <label>
                    Pattern:
                    <input type="text" name="pattern" value={formData.pattern} onChange={handleChange} required />
                </label>
                <label>
                    Rule Type:
                    <input type="text" name="rule_type" value={formData.rule_type} onChange={handleChange} required />
                </label>
                <label>
                    Description:
                    <input type="text" name="description" value={formData.description} onChange={handleChange} />
                </label>
                <button type="submit">Add Rule</button>
            </form>
            <Link to="/">Back to Home</Link>
        </div>
    );
}

export default AddRule;

import React, { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";

function EditRule() {
    const { id } = useParams(); // Retrieve the rule ID from the URL
    const [formData, setFormData] = useState({
        pattern: "",
        rule_type: "",
        description: "",
    });

    // Fetch the current rule's data when the component loads
    useEffect(() => {
        async function fetchRule() {
            try {
                const response = await fetch(`http://localhost:8002/rules/${id}`);
                if (response.ok) {
                    const data = await response.json();
                    setFormData(data); // Populate formData with the current rule's values
                } else {
                    alert("Failed to fetch rule data.");
                }
            } catch (error) {
                console.error("Error fetching rule:", error);
            }
        }
        fetchRule();
    }, [id]);

    // Update the formData when the input fields are modified
    function handleChange(event) {
        const { name, value } = event.target;
        setFormData((prevData) => ({
            ...prevData,
            [name]: value,
        }));
    }

    // Submit the updated rule
    async function handleSubmit(event) {
        event.preventDefault();
        try {
            const response = await fetch(`http://localhost:8002/rules/${id}`, {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(formData),
            });
            if (response.ok) {
                alert("Rule updated successfully");
                window.location.href = "/view-rules"; // Redirect to View Rules page
            } else {
                alert("Failed to update rule.");
            }
        } catch (error) {
            console.error("Error updating rule:", error);
        }
    }

    return (
        <div className="container">
            <h1>Edit Rule</h1>
            <form onSubmit={handleSubmit}>
                <label>
                    Pattern:
                    <input
                        type="text"
                        name="pattern"
                        value={formData.pattern}
                        onChange={handleChange}
                        required
                    />
                </label>
                <label>
                    Rule Type:
                    <input
                        type="text"
                        name="rule_type"
                        value={formData.rule_type}
                        onChange={handleChange}
                        required
                    />
                </label>
                <label>
                    Description:
                    <input
                        type="text"
                        name="description"
                        value={formData.description}
                        onChange={handleChange}
                    />
                </label>
                <button type="submit">Update Rule</button>
            </form>
            <Link to="/">Back to Home</Link>
        </div>
    );
}

export default EditRule;

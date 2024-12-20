from flask import Flask, request, jsonify
import re
import requests

app = Flask(__name__)

# Fetch rules from the Policy Management Service
POLICY_MANAGEMENT_URL = "http://policy_management:8002/rules"

def fetch_rules():
    """Fetch rules from the Policy Management Service."""
    try:
        response = requests.get(POLICY_MANAGEMENT_URL)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch rules: {response.status_code}")
            return []
    except requests.exceptions.RequestException as e:
        print(f"Error fetching rules: {str(e)}")
        return []

@app.route("/analyze", methods=["POST"])
def analyze_traffic():
    """Analyze incoming traffic against fetched rules."""
    try:
        data = request.json
        rules = fetch_rules()

        for rule in rules:
            pattern = rule["pattern"]
            if re.search(pattern, str(data.get("url", "")), re.IGNORECASE):
                return jsonify({
                    "status": "Blocked",
                    "rule": {
                        "id": rule["id"],
                        "pattern": rule["pattern"],
                        "rule_type": rule["rule_type"],
                        "description": rule["description"]
                    }
                }), 403

        return jsonify({"status": "Allowed"}), 200
    except Exception as e:
        print(f"Error processing request: {str(e)}")
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001, debug=True)

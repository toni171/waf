from flask import Flask, request, jsonify
from models import db, Rule, seed_rules
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///policy_management.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


with app.app_context():
    db.create_all()
    if not Rule.query.first():  # Seed only if no rules exist
        seed_rules()

@app.route("/rules", methods=["GET", "POST"])
def manage_rules():
    """Manage WAF rules: Fetch all rules or add a new rule."""
    if request.method == "GET":
        rules = Rule.query.all()
        rules_data = [
            {"id": rule.id, "pattern": rule.pattern, "rule_type": rule.rule_type, "description": rule.description}
            for rule in rules
        ]
        return jsonify(rules_data), 200

    if request.method == "POST":
        data = request.json
        try:
            new_rule = Rule(
                pattern=data["pattern"],
                rule_type=data["rule_type"],
                description=data["description"]
            )
            db.session.add(new_rule)
            db.session.commit()
            return jsonify({"message": "Rule added successfully"}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 400

@app.route("/rules/<int:rule_id>", methods=["PUT", "DELETE"])
def update_or_delete_rule(rule_id):
    """Update or delete a rule by ID."""
    rule = Rule.query.get(rule_id)
    if not rule:
        return jsonify({"error": "Rule not found"}), 404

    if request.method == "PUT":
        data = request.json
        try:
            rule.pattern = data.get("pattern", rule.pattern)
            rule.rule_type = data.get("rule_type", rule.rule_type)
            rule.description = data.get("description", rule.description)
            db.session.commit()
            return jsonify({"message": "Rule updated successfully"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    if request.method == "DELETE":
        db.session.delete(rule)
        db.session.commit()
        return jsonify({"message": "Rule deleted successfully"}), 200
    
@app.route("/rules/<int:rule_id>", methods=["GET"])
def get_rule(rule_id):
    """Retrieve a specific rule by its ID."""
    from models import Rule  # Import the Rule model

    try:
        rule = Rule.query.get(rule_id)  # Query the rule by ID
        if rule:
            rule_data = {
                "id": rule.id,
                "pattern": rule.pattern,
                "rule_type": rule.rule_type,
                "description": rule.description,
            }
            return jsonify(rule_data), 200
        else:
            return jsonify({"error": "Rule not found"}), 404
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Initialize database
    app.run(host="0.0.0.0", port=8002, debug=True)

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Rule(db.Model):
    __tablename__ = 'rules'

    id = db.Column(db.Integer, primary_key=True)
    pattern = db.Column(db.String(255), nullable=False)
    rule_type = db.Column(db.String(50), nullable=False)  # Example: XSS, SQLi
    description = db.Column(db.String(500), nullable=True)

def seed_rules():
    """Seed the database with predefined rules."""
    predefined_rules = [
        {"pattern": "<script.*?>.*?</script>", "rule_type": "XSS", "description": "Detects <script> tags."},
        {"pattern": "on\\w+\\s*=", "rule_type": "XSS", "description": "Detects JavaScript event handlers."},
        {"pattern": "(?i)\\bSELECT\\b", "rule_type": "SQLi", "description": "Detects SQL SELECT queries."},
        {"pattern": "(?i)\\bINSERT\\b", "rule_type": "SQLi", "description": "Detects SQL INSERT queries."},
        {"pattern": "(?i)\\bDROP\\b", "rule_type": "SQLi", "description": "Detects SQL DROP queries."},
        {"pattern": "(?i)\\bDELETE\\b", "rule_type": "SQLi", "description": "Detects SQL DELETE queries."},
        {"pattern": "(?i)\\bUNION\\b", "rule_type": "SQLi", "description": "Detects SQL UNION queries."},
        {"pattern": "--", "rule_type": "SQLi", "description": "Detects SQL comments."},
    ]

    for rule_data in predefined_rules:
        rule = Rule(**rule_data)
        db.session.add(rule)
    db.session.commit()

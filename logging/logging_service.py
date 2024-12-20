from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, RequestLog

app = Flask(__name__)
CORS(app)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///logging.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route("/log", methods=["POST"])
def log_request():
    """Logs incoming traffic data."""
    data = request.json
    try:
        new_log = RequestLog(
            ip_address=data["ip_address"],
            method=data["method"],
            url=data["url"],
            status=data["status"]
        )
        db.session.add(new_log)
        db.session.commit()
        return jsonify({"message": "Log added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/logs", methods=["GET"])
def get_logs():
    """Retrieve all logs."""
    logs = RequestLog.query.order_by(RequestLog.timestamp.desc()).all()
    logs_data = [
        {
            "id": log.id,
            "ip_address": log.ip_address,
            "method": log.method,
            "url": log.url,
            "status": log.status,
            "timestamp": log.timestamp.isoformat()
        }
        for log in logs
    ]
    return jsonify(logs_data), 200

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Initialize database
    app.run(host="0.0.0.0", port=8004, debug=True)

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO

app = Flask(__name__)
""" CORS(app, resources={r"/*": {"origins": "*"}}) """
socketio = SocketIO(app, cors_allowed_origins="*")

logs = []

# API to send real-time traffic updates
@app.route("/monitor", methods=["POST"])
def monitor():
    """Receive traffic data and emit real-time updates."""
    data = request.json
    print(f"Received monitoring data: {data}")  # Debug log
    if data:
        logs.append(data)  # Store the log (optional)
        socketio.emit("new_log", data)  # Broadcast to connected clients
        return jsonify({"message": "Log received and broadcasted"}), 200
    else:
        return jsonify({"error": "No data provided"}), 400

@app.route("/logs", methods=["GET"])
def get_logs():
    """Endpoint to fetch stored logs."""
    return jsonify(logs), 200

@socketio.on("connect")
def handle_connect():
    """Handle a new WebSocket connection."""
    print("A client connected")

@socketio.on("disconnect")
def handle_disconnect():
    """Handle a WebSocket disconnection."""
    print("A client disconnected")

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=8003, debug=True)

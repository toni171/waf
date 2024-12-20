from flask import Flask, request, Response, jsonify
import requests

app = Flask(__name__)

# Backend configuration
BACKEND_URL = "http://host.docker.internal:5000"  # Backend service URL
print("prova1")

def analyze_traffic(request_data):
    """Send traffic metadata to the Threat Detection Service for analysis."""
    try:
        response = requests.post("http://threat_detection:8001/analyze", json=request_data)
        return response.json(), response.status_code
    except requests.exceptions.RequestException as e:
        print(f"Error analyzing traffic: {str(e)}")
        return {"error": "Threat Detection Service Unavailable"}, 503


def send_to_monitoring(request_data, status):
    """Send traffic data to the Monitoring Service."""
    monitoring_data = {
        "ip_address": request_data.get("ip", "Unknown"),
        "method": request_data.get("method", "Unknown"),
        "url": request_data.get("url", "Unknown"),
        "status": status
    }
    print(f"Sending monitoring data: {monitoring_data}")  # Debug log
    try:
        response = requests.post("http://monitoring:8003/monitor", json=monitoring_data)
        if response.status_code != 200:
            print(f"Failed to send monitoring data: {response.status_code}, {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending monitoring data: {str(e)}")


@app.route("/", defaults={"path": ""}, methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
@app.route("/<path:path>", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
def proxy(path):
    print(f"Received request for path: {path} with method {request.method}")
    """Proxy traffic and apply threat detection."""
    # Build backend URL
    target_url = f"{BACKEND_URL}/{path}"

    # Collect request data
    request_data = {
        "ip": request.remote_addr or "Unknown",
        "method": request.method,
        "url": target_url,
        "headers": dict(request.headers),
        "args": request.args.to_dict(),
        "form": request.form.to_dict(),
    }
    print(f"Request data: {request_data}")

    # Analyze traffic through the Threat Detection Service
    detection_result, detection_status = analyze_traffic(request_data)

    if detection_status == 403:
        print("Request blocked by Threat Detection Service.")
        # Block the request and log it as "Blocked"
        log_request(request_data, "Blocked")
        send_to_monitoring(request_data, "Blocked")
        return jsonify(detection_result), 403

    if detection_status == 503:
        # If the Threat Detection Service is unavailable, allow traffic as a fallback
        print("Threat Detection Service unavailable. Allowing request as fallback.")
        log_request(request_data, "Fallback Allowed")
        send_to_monitoring(request_data, "Fallback Allowed")
        return jsonify({"status": "Fallback Allowed"}), 200

    # Forward allowed requests to the backend
    print("Forwarding request to backend...")
    try:
        if request.method == "GET":
            resp = requests.get(target_url, headers=request.headers, params=request.args)
        elif request.method == "POST":
            resp = requests.post(target_url, headers=request.headers, data=request.form)
        elif request.method in ["PUT", "DELETE", "PATCH"]:
            resp = requests.request(request.method, target_url, headers=request.headers, data=request.form)
        else:
            print("Unsupported HTTP method.")
            return Response("Unsupported method", status=405)

        # Log the request as "Allowed" and send monitoring updates
        print(f"Backend response status: {resp.status_code}")
        log_request(request_data, "Allowed")
        send_to_monitoring(request_data, "Allowed")
        response = Response(resp.content, status=resp.status_code)
        response.headers.update(resp.headers)
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error forwarding request: {str(e)}")
        log_request(request_data, "Error")
        send_to_monitoring(request_data, "Error")
        return Response(f"Error forwarding request: {str(e)}", status=500)


def log_request(request_data, status):
    """Log requests to the Logging Service."""
    log_data = {
        "ip_address": request_data.get("ip", "Unknown"),
        "method": request_data.get("method", "Unknown"),
        "url": request_data.get("url", "Unknown"),
        "status": status
    }
    try:
        response = requests.post("http://logging:8004/log", json=log_data)
        if response.status_code != 201:
            print(f"Failed to log request: {response.status_code}, {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error logging request: {str(e)}")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
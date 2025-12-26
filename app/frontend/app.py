from flask import Flask, jsonify
import requests
import os
import time

app = Flask(__name__)

# Configuration
BACKEND_SERVICE = os.getenv("BACKEND_SERVICE", "http://backend-service:5001")

@app.route("/health")
def health():
    return jsonify({"status": "healthy", "service": "frontend"})

@app.route("/")
def home():
    return jsonify({
        "message": "My Chaos Mesh Project Frontend",
        "endpoints": [
            "/health",
            "/api/data"
        ]
    })

@app.route("/api/data")
def get_data():
    """Call backend service"""
    start_time = time.time()
    try:
        response = requests.get(f"{BACKEND_SERVICE}/data", timeout=5)
        elapsed = time.time() - start_time
        return jsonify({
            "source": "frontend",
            "backend_response": response.json(),
            "latency_ms": round(elapsed * 1000, 2)
        })
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e), "service": "frontend"}), 503

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

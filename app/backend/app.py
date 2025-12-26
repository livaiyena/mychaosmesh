from flask import Flask, jsonify
import requests
import os
import time

app = Flask(__name__)

# Configuration
DATASERVICE_URL = os.getenv("DATASERVICE_URL", "http://dataservice:5002")

@app.route("/health")
def health():
    return jsonify({"status": "healthy", "service": "backend"})

@app.route("/data")
def get_data():
    """Call dataservice"""
    start_time = time.time()
    try:
        response = requests.get(f"{DATASERVICE_URL}/query", timeout=5)
        elapsed = time.time() - start_time
        return jsonify({
            "source": "backend",
            "dataservice_response": response.json(),
            "latency_ms": round(elapsed * 1000, 2)
        })
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e), "service": "backend"}), 503

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)

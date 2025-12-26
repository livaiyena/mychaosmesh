from flask import Flask, jsonify
import time
import random

app = Flask(__name__)

@app.route("/health")
def health():
    return jsonify({"status": "healthy", "service": "dataservice"})

@app.route("/query")
def query_data():
    """Simulate a database query"""
    # Simulate processing time
    process_time = random.uniform(0.05, 0.2)
    time.sleep(process_time)
    
    return jsonify({
        "data": [
            {"id": 1, "value": "A"},
            {"id": 2, "value": "B"},
            {"id": 3, "value": "C"}
        ],
        "message": "Query successful",
        "processing_time": process_time
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)

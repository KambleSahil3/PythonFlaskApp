import os
from flask import Flask, jsonify
import psutil
from datetime import datetime, timezone

app = Flask(__name__)

@app.route("/")
def index():
    return jsonify({"message": "Flask app is running", "status": "ok"})

@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        # Use timezone-aware UTC datetime to avoid naive datetime issues
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "cpu_percent": psutil.cpu_percent(),
        "memory_percent": psutil.virtual_memory().percent,
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    # BUG FIX: was host="127.0.0.1" which blocks Docker from exposing the port.
    # Fixed to host="0.0.0.0" so the app is reachable outside the container.
    # debug is read from env so it is never hardcoded
    debug = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug)

# FastApi server
import os
from flask import Flask, render_template
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

PI_IP = os.getenv("PI_IP", "192.168.1.x")
PI_PORT = os.getenv("PI_PORT", "8765")
DASHBOARD_PORT = int(os.getenv("DASHBOARD_PORT", 5000))


@app.route("/")
def index():
    return render_template(
        "index.html",
        pi_ip=PI_IP,
        pi_port=PI_PORT,
    )


if __name__ == "__main__":
    print(f"[dashboard] Open http://localhost:{DASHBOARD_PORT} in your browser")
    print(f"[dashboard] Expecting robot at ws://{PI_IP}:{PI_PORT}")
    app.run(host="0.0.0.0", port=DASHBOARD_PORT, debug=True)

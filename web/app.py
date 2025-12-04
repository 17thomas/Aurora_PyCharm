import os
import sqlite3
from flask import Flask, request, render_template, send_file

app = Flask(__name__)

# Environment variables (configured in Render dashboard)
SECRET_TOKEN = os.getenv("SECRET_TOKEN")
DB_PATH = os.getenv("DB_PATH", "subscribers.db")  # default local name
IMAGE_PATH = os.getenv("IMAGE_PATH", "static/latest.jpg")

# Ensure folders exist
os.makedirs("static", exist_ok=True)

def get_db():
    """Open connection to the DB and ensure table exists."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS subscribers (
            email TEXT PRIMARY KEY
        );
    """)
    conn.commit()
    return conn


def init_db():
    """Initialize the subscribers table."""
    conn = get_db()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS subscribers (
            email TEXT PRIMARY KEY
        );
    """)
    conn.commit()
    conn.close()


# ---------------------------------------------------------
# MAIN PAGE (GET + POST for subscription)
# ---------------------------------------------------------
@app.route("/", methods=["GET", "POST"])
def home():
    status = {
        "last_detection": "No aurora detected yet",
        "green_percentage": 0,
        "red_percentage": 0,
        "image_exists": os.path.exists(IMAGE_PATH),
        "last_image": "latest.jpg"
    }

    message = None

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        action = request.form.get("action")  # "subscribe" oder "unsubscribe"

        if email:
            conn = get_db()
            c = conn.cursor()

            if action == "subscribe":
                try:
                    c.execute("INSERT INTO subscribers (email) VALUES (?)", (email,))
                    conn.commit()
                    message = "Subscribed successfully"
                except sqlite3.IntegrityError:
                    message = "Already subscribed"
                except Exception as e:
                    message = f"DB Error: {e}"

            elif action == "unsubscribe":
                c.execute("DELETE FROM subscribers WHERE email = ?", (email,))
                conn.commit()
                message = "Unsubscribed"

            conn.close()
        else:
            message = "Please provide a valid email"

    return render_template("index.html", status=status, message=message)


# ---------------------------------------------------------
# IMAGE UPLOAD (your image pipeline / camera triggers this)
# ---------------------------------------------------------
@app.route("/upload_image", methods=["POST"])
def upload_image():
    token = request.args.get("token")
    if token != SECRET_TOKEN:
        return {"error": "Unauthorized"}, 401

    if "image" not in request.files:
        return {"error": "No image uploaded"}, 400

    img = request.files["image"]
    img.save(IMAGE_PATH)
    return {"success": True}


# ---------------------------------------------------------
# DB SYNC ENDPOINTS (secured with SECRET_TOKEN)
# ---------------------------------------------------------
@app.route("/export_db")
def export_db():
    token = request.args.get("token")
    if token != SECRET_TOKEN:
        return {"error": "Unauthorized"}, 401

    if not os.path.exists(DB_PATH):
        init_db()
    return send_file(DB_PATH, as_attachment=True)


@app.route("/import_db", methods=["POST"])
def import_db():
    token = request.args.get("token")
    if token != SECRET_TOKEN:
        return {"error": "Unauthorized"}, 401

    if "db" not in request.files:
        return {"error": "Missing file"}, 400

    file = request.files["db"]
    file.save(DB_PATH)
    return {"success": True}


# ---------------------------------------------------------
if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

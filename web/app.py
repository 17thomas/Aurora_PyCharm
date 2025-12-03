from flask import Flask, render_template, request
import sqlite3
import os

app = Flask(__name__)
DB = "subscribers.db"

# Initialize DB
def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS subscribers (
            email TEXT PRIMARY KEY
        )
    """)
    conn.commit()
    conn.close()

@app.route("/upload", methods=["POST"])
def upload():
    if "image" not in request.files:
        return {"error": "No image provided"}, 400

    image = request.files["image"]
    image.save("static/latest.jpg")

    # Optional: update status text
    global latest_status
    latest_status = request.form.get("status", "Updated")

    return {"success": True}


@app.route("/", methods=["GET", "POST"])
def index():
    message = ""

    # Example status info (you can replace with dynamic data later)
    status = {
        "last_detection": "No aurora detected yet",
        "green_percentage": 0,
        "red_percentage": 0,
        "last_image": "latest.jpg"  # this will come from static/latest.jpg
    }

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        conn = sqlite3.connect(DB)
        c = conn.cursor()

        if "subscribe" in request.form:
            try:
                c.execute("INSERT INTO subscribers (email) VALUES (?)", (email,))
                conn.commit()
                message = "Subscribed successfully!"
            except sqlite3.IntegrityError:
                message = "Already subscribed."
        elif "unsubscribe" in request.form:
            c.execute("DELETE FROM subscribers WHERE email = ?", (email,))
            conn.commit()
            message = "Unsubscribed successfully."

        conn.close()

    return render_template("index.html", message=message, status=status)

if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5001)  # port 5001 to avoid macOS conflicts

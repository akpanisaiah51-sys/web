from flask import Flask, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash
import psycopg2

app = Flask(__name__)

# --- Database config (use env vars in real apps) ---
DB_CONFIG = dict(
    host="localhost",
    dbname="face",
    user="postgres",
    password="1234",
    port=5432,
)

# ---------- Routes ----------

@app.route("/")
def form():
    """Render the registration form (templates/index.html)."""
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():
    """Handle form submit, save to DB, then redirect to dashboard."""
    email = request.form.get("email")
    password = request.form.get("password")

    # Basic validation
    if not email or not password:
        return "Missing email, or password.", 400

    # Always hash passwords before storing
    password_hash = generate_password_hash(password)

    # Insert into PostgreSQL (short‑lived connection per request)
    try:
        with psycopg2.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO staff (email, password) VALUES (%s, %s, %s)",
                    (email, password),
                )
        # Leaving the 'with conn' block commits on success
    except psycopg2.Error as e:
        # In production, log full error details; return a safe message
        return f"Database error: {e}", 500

    # After saving, go to your dashboard page at /index
    return redirect(url_for("dashboard"))


@app.route("/index")
def dashboard():
    """Render your dashboard (templates/index.html)."""
    return render_template("index.html")


# ---------- App entry point ----------
if __name__ == "__main__":
    # Expose to local network; remove debug=True in production
    app.run(host="0.0.0.0", port=5000, debug=True)

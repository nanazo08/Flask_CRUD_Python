from flask import Flask, request, redirect, url_for, session, render_template_string
from flask_mysqldb import MySQL
import hashlib
import os

app = Flask(__name__, template_folder='templates')
app.secret_key = os.urandom(24)

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "giana"
app.config["MYSQL_DB"] = "bookstore"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@app.route("/", methods=["GET", "POST"])
def login():
    msg = ''
    if request.method == "POST" and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        hashed_password = hash_password(password)

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM customers WHERE username = %s AND password = %s', (username, hashed_password,))
        account = cursor.fetchone()
        cursor.close()

        if account:
            session['loggedin'] = True
            session['id'] = account['customer_id']
            session['username'] = account['username']
            return redirect(url_for('home'))
        else:
            msg = 'Incorrect username / password!'

    return render_template_string('''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.3.0/font/bootstrap-icons.css">
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css"
        integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
    <style>
        /* Your custom CSS styles */
    </style>
</head>
<body>
    <div class="container">
        <form method="POST">
            <h2>Login</h2>
            <input type="text" name="username" placeholder="Username" required>
            <input type="password" name="password" id="password" placeholder="Password" required>
            <i class="bi bi-eye-slash" id="togglePassword"></i>
            <button type="submit">Log In</button>
            <p>{{ msg }}</p>
            <a href="/register">Create New Account</a>
            <a href="#">Forgot Password?</a>
        </form>
    </div>
    <script>
        /* Your JavaScript code */
    </script>
</body>
</html>
''', msg=msg)

@app.route("/register", methods=["GET", "POST"])
def register():
    msg = ''
    if request.method == "POST" and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        hashed_password = hash_password(password)

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM customers WHERE username = %s', (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            msg = 'Username already exists!'
        else:
            cursor.execute('INSERT INTO customers (username, password) VALUES (%s, %s)', (username, hashed_password))
            mysql.connection.commit()
            msg = 'You have successfully registered!'

    return render_template_string('''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Register</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.3.0/font/bootstrap-icons.css">
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css"
        integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
    <style>
        /* Your custom CSS styles */
    </style>
</head>
<body>
    <div class="container">
        <form method="POST">
            <h2>Register</h2>
            <input type="text" name="username" placeholder="Username" required>
            <input type="password" name="password" id="password" placeholder="Password" required>
            <i class="bi bi-eye-slash" id="togglePassword"></i>
            <button type="submit">Register</button>
            <p>{{ msg }}</p>
            <a href="/">Login</a>
        </form>
    </div>
    <script>
        /* Your JavaScript code */
    </script>
</body>
</html>
''', msg=msg)

@app.route("/home")
def home():
    if 'loggedin' in session:
        return 'Welcome, ' + session['username'] + '!'
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)

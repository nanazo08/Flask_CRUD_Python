from flask import Flask, request, redirect, url_for, session, render_template_string, Response, flash
from flask_mysqldb import MySQL
import re
import hashlib
import os
from dicttoxml import dicttoxml

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

    return render_template_string('login.html', msg=msg)

if __name__ == "__main__":
    app.run(debug=True)

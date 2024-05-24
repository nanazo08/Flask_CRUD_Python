from flask import Flask, request, redirect, url_for, session, render_template_string, jsonify, make_response
from flask_mysqldb import MySQL
import hashlib
import os
from flask_restful import Resource, Api
import MySQLdb.cursors
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom.minidom import parseString



app = Flask(__name__, template_folder='templates')
api = Api(app)
app.secret_key = os.urandom(24)

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "giana"
app.config["MYSQL_DB"] = "restaurant"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Restaurant API endpoints
class Menu(Resource):
    def get(self):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM menu')
        menu_items = cursor.fetchall()
        cursor.close()
        return jsonify(menu_items)

    def post(self):
        data = request.get_json()
        item_name = data['item_name']
        price = data['price']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO menu (item_name, price) VALUES (%s, %s)', (item_name, price))
        mysql.connection.commit()
        cursor.close()

        return {'message': 'Menu item added successfully'}, 201

class Orders(Resource):
    def get(self):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM orders')
        orders = cursor.fetchall()
        cursor.close()
        return jsonify(orders)

    def post(self):
        data = request.get_json()
        item_id = data['item_id']
        quantity = data['quantity']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO orders (item_id, quantity) VALUES (%s, %s)', (item_id, quantity))
        mysql.connection.commit()
        cursor.close()

        return {'message': 'Order placed successfully'}, 201

api.add_resource(Menu, '/menu')
api.add_resource(Orders, '/orders')

def generate_xml(data):
    root = Element("orders")
    for order in data:
        order_element = SubElement(root, "order")
        for key, value in order.items():
            if key == 'item_id':
                item_element = SubElement(order_element, "item")
                item_element.text = str(value)
            else:
                sub_element = SubElement(order_element, key)
                sub_element.text = str(value)
    
    xml_string = tostring(root, encoding='utf-8', method='xml')
    return xml_string.decode('utf-8')

def process_order(item_id, quantity):
    # Replace this with your actual order processing logic
    print(f"Processing order for Item {item_id} with quantity {quantity}")

@app.route("/place_order", methods=["GET", "POST"])
def place_order():
    if request.method == "POST":
        item_id = request.form.get('item')  # Assuming you have a select field with name 'item'
        quantity = request.form.get('quantity')

        # Store order data in the database
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO orders (item_id, quantity) VALUES (%s, %s)', (item_id, quantity))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for("order_confirmation"))
    return render_template_string('''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Place Order</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f8f9fa;
            margin: 0;
            padding: 0;
        }
        .container {
            max-width: 500px;
            margin: 50px auto;
            padding: 20px;
            background-color: #fff;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        h2 {
            text-align: center;
            margin-bottom: 30px;
        }
        label {
            font-weight: bold;
        }
        input[type="number"] {
            width: 100%;
            padding: 10px;
            margin-bottom: 20px;
            border: 1px solid #ced4da;
            border-radius: 4px;
            box-sizing: border-box;
        }
        select {
            width: 100%;
            padding: 10px;
            margin-bottom: 20px;
            border: 1px solid #ced4da;
            border-radius: 4px;
            box-sizing: border-box;
        }
        button[type="submit"] {
            background-color: #007bff;
            color: #fff;
            padding: 10px 20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        button[type="submit"]:hover {
            background-color: #0056b3;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>Place Order</h2>
        <form method="POST" action="/place_order">
            <div class="form-group">
                <label for="item">Select Item:</label>
                <select id="item" name="item" class="form-control">
                    <option value="1">Item 1</option>
                    <option value="2">Item 2</option>
                    <!-- Add more options as needed -->
                </select>
            </div>
            <div class="form-group">
                <label for="quantity">Quantity:</label>
                <input type="number" id="quantity" name="quantity" min="1" class="form-control" required>
            </div>
            <button type="submit" class="btn btn-primary">Place Order</button>
        </form>
        <a href="http://127.0.0.1:5000/home" class="btn-home">Back to Home</a>
    </div>
</body>
</html>

''')

@app.route("/order_confirmation")
def order_confirmation():
    return render_template_string('''
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Order Confirmation</title>
</head>
<body>
    <h2>Your order has been placed successfully!</h2>
    <a href="http://127.0.0.1:5000/home" class="btn btn-primary">Back to Home</a>
</body>
</html>
''')

@app.route("/", methods=["GET", "POST"])
def login():
    msg = ''
    if request.method == "POST" and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        hashed_password = hash_password(password)

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
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
        body {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            background-color: #f4f4f4;
        }
        .container {
            max-width: 400px;
            padding: 20px;
            background: #fff;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }
        h2 {
            text-align: center;
            margin-bottom: 20px;
        }
        input[type="text"],
        input[type="password"] {
            width: calc(100% - 40px);
            padding: 10px;
            margin: 10px 0;
            border: 1px solid #ccc;
            border-radius: 5px;
            display: inline-block;
        }
        #togglePassword {
            cursor: pointer;
            position: absolute;
            right: 20px;
            top: calc(35% + 10px);
            transform: translateY(-50%);
        }
        button {
            width: 100%;
            padding: 10px;
            background-color: #28a745;
            border: none;
            border-radius: 5px;
            color: #fff;
            font-size: 16px;
            cursor: pointer;
        }
        button:hover {
            background-color: #218838;
        }
        p {
            color: red;
            text-align: center;
        }
        a {
            display: block;
            text-align: center;
            margin-top: 10px;
            color: #007bff;
        }
        a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="container">
        <form method="POST">
            <h2>Login</h2>
            <div class="form-group">
                <input type="text" name="username" class="form-control" placeholder="Username" required>
            </div>
            <div class="form-group position-relative">
                <input type="password" name="password" class="form-control" id="password" placeholder="Password" required>
                <i class="bi bi-eye-slash" id="togglePassword"></i>
            </div>
            <button type="submit" class="btn btn-success">Log In</button>
            <p>{{ msg }}</p>
            <a href="/register">Create New Account</a>
        </form>
    </div>
    <script>
        document.getElementById('togglePassword').addEventListener('click', function () {
            var passwordField = document.getElementById('password');
            var type = passwordField.getAttribute('type') === 'password' ? 'text' : 'password';
            passwordField.setAttribute('type', type);
            this.classList.toggle('bi-eye');
            this.classList.toggle('bi-eye-slash');
        });
    </script>
</body>
</html>
''', msg=msg)


@app.route("/register", methods=["GET", "POST"])
def register():
    msg = ''
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        email_address = request.form['email_address']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        hashed_password = hash_password(password)

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM customers WHERE username = %s', (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            msg = 'Username already exists!'
        else:
            cursor.execute('INSERT INTO customers (username, password, email_address, first_name, last_name) VALUES (%s, %s, %s, %s, %s)', (username, hashed_password, email_address, first_name, last_name))
            mysql.connection.commit()  # Commit the transaction
            msg = 'You have successfully registered!'
            return redirect(url_for('login'))
        cursor.close()
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
        body {
            background-color: #f8f9fa;
            font-family: Arial, sans-serif;
        }
        
        .container {
            max-width: 400px;
            margin: 100px auto;
            padding: 20px;
            background-color: #fff;
            border-radius: 10px;
            box-shadow: 0px 0px 10px 0px rgba(0,0,0,0.1);
        }
        
        h2 {
            text-align: center;
            margin-bottom: 30px;
            color: #333;
        }
        
        input[type="text"],
        input[type="email"],
        input[type="password"] {
            width: 100%;
            padding: 10px;
            margin-bottom: 20px;
            border: 1px solid #ddd;
            border-radius: 5px;
            box-sizing: border-box;
        font-size: 16px;
       
        }
        
        button[type="submit"] {
            width: 100%;
            padding: 10px;
            background-color: #007bff;
            border: none;
            border-radius: 5px;
            color: #fff;
            font-size: 16px;
            cursor: pointer;
        }
        
        button[type="submit"]:hover {
            background-color: #0056b3;
        }
        
        p {
            text-align: center;
            margin-top: 20px;
            color: #555;
        }
        
        a {
            text-decoration: none;
            color: #007bff;
            display: block;
            text-align: center;
            margin-top: 20px;
        }
        
        a:hover {
            color: #0056b3;
        }
        
        #togglePassword {
            position: absolute;
            top: 67%;
            right: 10px;
            transform: translateY(-50%);
            cursor: pointer;
        }
    </style>
</head>
<body>
    <div class="container">
        <form method="POST">
            <h2>Register</h2>
            <input type="email" name="email_address" placeholder="Email Address" required>
            <input type="text" name="first_name" placeholder="First Name" required>
            <input type="text" name="last_name" placeholder="Last Name" required>
            <div style="position: relative;">
                <input type="text" name="username" placeholder="Username" required>
                <input type="password" name="password" id="password" placeholder="Password" required>
                <i class="bi bi-eye-slash" id="togglePassword"></i>
            </div>
            <button type="submit">Register</button>
            <p>{{ msg }}</p>
            <a href="/">Back to Home</a>
        </form>
    </div>
    <script>
        document.addEventListener('DOMContentLoaded', function () {
        const passwordInput = document.getElementById('password');
        const togglePasswordButton = document.getElementById('togglePassword');

        togglePasswordButton.addEventListener('click', function () {
            const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
            passwordInput.setAttribute('type', type);
            togglePasswordButton.classList.toggle('bi-eye');
            togglePasswordButton.classList.toggle('bi-eye-slash');
        });
    });
    </script>
</body>
</html>
''', msg=msg)

@app.route("/home")
def home():
    if 'loggedin' in session:
        html_content = '''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Welcome</title>
            <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css"
                integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
            <style>
                body {
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    background-color: #f8f9fa;
                }
                .container {
                    max-width: 600px;
                    padding: 20px;
                    background: #fff;
                    border-radius: 10px;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                }
                h2 {
                    text-align: center;
                    margin-bottom: 20px;
                }
                ul {
                    list-style-type: none;
                    padding: 0;
                }
                ul li {
                    margin: 10px 0;
                }
                a {
                    text-decoration: none;
                    color: #007bff;
                }
                a:hover {
                    text-decoration: underline;
                }
                .btn-home {
                    display: block;
                    width: 100%;
                    padding: 10px;
                    text-align: center;
                    margin-top: 20px;
                    background-color: #007bff;
                    color: #fff;
                    border-radius: 5px;
                    text-decoration: none;
                }
                .btn-home:hover {
                    background-color: #0056b3;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h2>Welcome, {{ username }}!</h2>
                <p>What would you like to do?</p>
                <ul>
                    <li><a href="{{ url_for('add_menu_item') }}">Add Menu Item</a></li>
                    <li><a href="{{ url_for('view_menu') }}">View Menu</a></li>
                    <li><a href="{{ url_for('place_order') }}">Place Order</a></li>
                    <li><a href="{{ url_for('orders') }}">View Orders</a></li>
                </ul>
                <a href="http://127.0.0.1:5000/home" class="btn-home">Back to Home</a>
            </div>
        </body>
        </html>
        '''
        return render_template_string(html_content, username=session['username'])
    return redirect(url_for('login'))


@app.route("/add_menu_item", methods=["GET", "POST"])
def add_menu_item():
    if request.method == "POST":
        item_name = request.form['item_name']
        price = request.form['price']
        rating = request.form['rating']
        comment = request.form['comment']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO menu (item_name, price, rating, comment) VALUES (%s, %s, %s, %s)', (item_name, price, rating, comment))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('view_menu'))

    return render_template_string('''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Add Menu Item</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css"
          integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
    <style>
        body {
            background-color: #f8f9fa;
            font-family: Arial, sans-serif;
        }
        .container {
            max-width: 500px;
            margin: 50px auto;
        }
        .form-group {
            margin-bottom: 20px;
        }
        h2 {
            text-align: center;
            margin-bottom: 30px;
        }
    </style>
</head>
<body>
<div class="container">
    <h2>Add Menu Item</h2>
    <form method="POST">
        <div class="form-group">
            <label for="item_name">Item Name:</label>
            <input type="text" class="form-control" id="item_name" name="item_name" required>
        </div>
        <div class="form-group">
            <label for="price">Price:</label>
            <input type="text" class="form-control" id="price" name="price" required>
        </div>
        <div class="form-group">
            <label for="rating">Rating:</label>
            <input type="text" class="form-control" id="rating" name="rating" required>
        </div>
        <div class="form-group">
            <label for="comment">Comment:</label>
            <textarea class="form-control" id="comment" name="comment" rows="4"></textarea>
        </div>
        <button type="submit" class="btn btn-primary">Add Menu Item</button>
    </form>
    <a href="http://127.0.0.1:5000/home" class="btn btn-secondary mt-3">Back to Home</a>
</div>
                                  
<script>
    // Automatically add new line when reaching the end of the textarea
    document.getElementById('comment').addEventListener('input', function () {
        var textarea = this;
        if (textarea.scrollHeight > textarea.clientHeight) {
            textarea.value += '\n';
        }
    });
</script>
</body>
</html>


''')

@app.route("/view_menu", methods=['GET'])
def view_menu():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT item_id, item_name, price, rating, comment FROM menu')
    menu_items = cursor.fetchall()
    cursor.close()

    return render_template_string('''<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Menu</title>
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css"
            integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
        <style>
            body {
                background-color: #f8f9fa;
                font-family: Arial, sans-serif;
            }
            .container {
                margin-top: 50px;
            }
            h2 {
                text-align: center;
                margin-bottom: 30px;
            }
            .menu-list {
                list-style-type: none;
                padding: 0;
            }
            .menu-item {
                background: #fff;
                margin: 10px 0;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            }
            .menu-item .item-details {
                margin-bottom: 10px;
            }
            .back-home {
                display: block;
                width: 100%;
                padding: 10px;
                margin-top: 20px;
                text-align: center;
                background-color: #007bff;
                color: #fff;
                border-radius: 5px;
                text-decoration: none;
            }
            .back-home:hover {
                background-color: #0056b3;
            }
            .download-links a {
                display: inline-block;
                margin: 10px 0;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Menu</h2>
            <ul class="menu-list">
                {% for item in menu_items %}
                    <li class="menu-item">
                        <div class="item-details">
                            <p><strong>Name:</strong> {{ item.item_name }}</p>
                            <p><strong>Price:</strong> ${{ item.price }}</p>
                            <p><strong>Rating:</strong> {{ item.rating }}</p>
                            <p><strong>Comment:</strong> {{ item.comment }}</p>
                        </div>
                        <form action="/edit/{{ item.item_id }}" method="post" style="display:inline;">
                            <button type="submit" class="btn btn-primary">Edit</button>
                        </form>
                        <form action="/delete_item/{{ item.item_id }}" method="post" style="display:inline;">
                            <button type="submit" class="btn btn-danger">Delete</button>
                        </form>
                    </li>
                {% endfor %}
            </ul>
            <div class="download-links">
                <a href="/download_menu/json" class="btn btn-secondary">Download JSON</a>
                <a href="/download_menu/xml" class="btn btn-secondary">Download XML</a>
            </div>
            <a href="http://127.0.0.1:5000/home" class="back-home">Back to Home</a>
        </div>
    </body>
    </html>
    ''', menu_items=menu_items)

@app.route("/edit/<int:item_id>", methods=['GET', 'POST'])
def edit(item_id):
    if request.method == 'POST':
        item_name = request.form.get('item_name')
        price = request.form.get('price')
        rating = request.form.get('rating')
        comment = request.form.get('comment')

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE menu SET item_name = %s, price = %s, rating = %s, comment = %s WHERE item_id = %s', 
                        (item_name, price, rating, comment, item_id))

        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('view_menu'))
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM menu WHERE item_id = %s', (item_id,))
    item = cursor.fetchone()
    cursor.close()

    return render_template_string('''<!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Edit Menu Item</title>
                <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
                <style>
                    /* Your CSS styles here */
                </style>
            </head>
            <body>
                <div class="container">
                    <h2>Edit Menu Item</h2>
                    <form method="POST">
                        <div class="form-group">
                            <label for="item_name">Item Name:</label>
                            <input type="text" id="item_name" name="item_name" value="{{ item.item_name }}" required>
                        </div>
                        <div class="form-group">
                            <label for="price">Price:</label>
                            <input type="text" id="price" name="price" value="{{ item.price }}" required>
                        </div>
                        <div class="form-group">
                            <label for="rating">Rating:</label>
                            <input type="text" id="rating" name="rating" value="{{ item.rating }}" required>
                        </div>
                        <div class="form-group">
                            <label for="comment">Comment:</label>
                            <textarea id="comment" name="comment" rows="4" required>{{ item.comment }}</textarea>
                        </div>
                        <button type="submit">Update Menu Item</button>
                    </form>
                    <a href="http://127.0.0.1:5000/home" class="back-home">Back to Home</a>
                </div>
            </body>
            </html>''', item=item)





@app.route("/delete_item/<int:item_id>", methods=['POST'])
def delete_item(item_id):
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM menu WHERE item_id = %s', (item_id,))
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('view_menu'))


@app.route("/orders/json")
def orders_json():
    # Retrieve orders data from the database or any other source
    orders_data = {...}  # Retrieve orders data in JSON format
    response = make_response(jsonify(orders_data))
    response.headers['Content-Disposition'] = 'attachment; filename=orders.json'
    return response

@app.route("/orders/xml")
def orders_xml():
    # Retrieve orders data from the database or any other source
    orders_data = {...}  # Retrieve orders data in XML format
    xml_string = generate_xml(orders_data)  # Implement a function to generate XML
    response = make_response(xml_string)
    response.headers['Content-Type'] = 'application/xml'
    response.headers['Content-Disposition'] = 'attachment; filename=orders.xml'
    return response


@app.route("/download_menu/<format>")
def download_menu(format):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT  item_name, price, rating, comment FROM menu')
    menu_items = cursor.fetchall()
    cursor.close()

    if format == 'json':
        menu_data = [{'item_name': item['item_name'], 'price': item['price'], 'rating': item['rating'], 'comment': item['comment']} for item in menu_items]
        response = jsonify(menu_data)
        response.headers['Content-Disposition'] = 'attachment; filename=menu.json'
        return response
    elif format == 'xml':
        root = Element('menu')
        for item in menu_items:
            item_element = SubElement(root, 'item')
            name_element = SubElement(item_element, 'item_name')
            name_element.text = item['item_name']
            price_element = SubElement(item_element, 'price')
            price_element.text = str(item['price'])
            rating_element = SubElement(item_element, 'rating')
            rating_element.text = str(item['rating'])
            comment_element = SubElement(item_element, 'comment')
            comment_element.text = item['comment']

        xml_string = parseString(tostring(root)).toprettyxml()
        response = app.response_class(
            response=xml_string,
            status=200,
            mimetype='application/xml',
            headers={'Content-Disposition': 'attachment; filename=menu.xml'}
        )
        return response

if __name__ == '__main__':
    app.run(debug=True)


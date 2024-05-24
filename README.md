- **templates/**: Contains HTML templates for the application's web pages.
- **static/**: Holds static assets like CSS stylesheets and JavaScript files.
- **app.py**: The main Python file responsible for running the application.
- **requirements.txt**: Lists the Python packages required to run the application.

## Contributing

If you wish to contribute to this project, please follow these steps:

1. **Fork the Repository**: Create your own copy of the project.
2. **Create a New Branch**: Implement your changes in a new branch.
3. **Commit Your Changes**: Once your changes are ready, commit them to your branch.
4. **Push Your Changes**: Push your branch to your forked repository on GitHub.
5. **Open a Pull Request**: Submit a pull request to merge your changes into the main project.


# Flask Bookstore Application

This Flask application implements a simple login system for a bookstore website. It allows users to log in with their username and password.

## Overview

The `app.py` file serves as the main Python script for the Flask application. It defines the routes and logic for handling user authentication and rendering the login page.

## Dependencies

- Flask: A lightweight web framework for Python.
- Flask-MySQLdb: A Flask extension for interacting with MySQL databases.
- dicttoxml: A library for converting Python dictionaries to XML format.

## Configuration

The application connects to a MySQL database named `bookstore` running on localhost with the username `root` and password `giana`. You can adjust these configurations in the `app.py` file as needed.

## Running the Application

To run the application, execute the `app.py` script:

**What is .gitignore?**

The `.gitignore` file acts as a guide for Git, instructing it on which files and directories to ignore when tracking changes in your project. It's like having a traffic cop in your repository, ensuring that only relevant files are monitored. This helps maintain a clean project history and keeps the focus on what truly matters.

**Why is it Important?**

1. **Keeping Things Tidy**: By listing files such as temporary files, logs, or build artifacts, you prevent your repository from being cluttered with unnecessary files.

2. **Protecting Sensitive Information**: Use `.gitignore` to shield sensitive data like passwords, API keys, or local configuration files from accidentally being committed to your version control history.

3. **Avoiding Versioning Build Artifacts**: Build artifacts and local environment-specific files don't need to be versioned. `.gitignore` helps you maintain a lean repository by excluding them from version control.

4. **Speeding Things Up**: Ignoring unnecessary files improves Git's performance as it doesn't waste time tracking changes in files you don't care about.

5. **Smooth Collaboration**: `.gitignore` ensures consistency among team members by specifying which files and folders are ignored, promoting collaboration and preventing conflicts.




# Restaurant Management System

This project is a web-based restaurant management system implemented using Flask, MySQL, and Bootstrap. It allows users to view registered customers, menu items, edit menu items, delete menu items, and download orders data in JSON or XML format.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Routes](#routes)
- [Database Schema](#database-schema)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/nanazo08/Flask_CRUD_Python.git


2. Install dependencies:
   pip install -r requirements.txt


## Usage

1. Start the Flask application:
    python app.py run in cmd but first locate the file.

2. Open your web browser and go to   http://127.0.0.   1:5000/ to access the application.

## Features
- View Customers: Display all registered customers with their details.

- View Menu: Show the menu items along with their prices, ratings, and comments.

- Edit Menu Items: Allow editing of menu items including name, price, rating, and comment.

- Delete Menu Items: Enable deleting menu items from the system.

- Download Orders Data: Download orders data in JSON or XML format for further analysis.

## Routes
- /view_customers: View all registered customers.
- /view_menu: View the menu items.
- /edit/<int:item_id>: Edit a menu item by its ID.
- /delete_item/<int:item_id>: Delete a menu item by its ID.
- /orders/json: Download orders data in JSON format.
- /orders/xml: Download orders data in XML format.
- /download_menu/<format>: Download menu data in either JSON or XML format.

## Database Schema
- The database schema includes the following tables:

- customers: Stores information about registered customers.

- customer_id: Unique identifier for the customer.
- first_name: First name of the customer.
- middle_initial: Middle initial of the customer.
- last_name: Last name of the customer.
- email_address: Email address of the customer.
- phone: Phone number of the customer.
- username: Username of the customer.
- password: Password of the customer.
- menu: Contains information about menu items.

- item_id: Unique identifier for the menu item.
- item_name: Name of the menu item.
- price: Price of the menu item.
- rating: Rating of the menu item.
- comment: Comment or description of the menu item.

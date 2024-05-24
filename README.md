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

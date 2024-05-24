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


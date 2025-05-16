# Studen_Task_Manager
A web-based task manager application built using Flask, SQLAlchemy, and Flask-Login. The app allows students to manage their tasks efficiently by adding, updating, and deleting tasks. Each user can register and log in to maintain their own set of tasks. Features include task categorization, setting priorities, due dates, and task completion status.

Table of Contents
Technologies Used

Features

Installation Instructions

Usage

Project Structure

License

Technologies Used
Flask: A lightweight Python web framework used to build the app.

SQLAlchemy: ORM (Object-Relational Mapping) used for database interaction.

Flask-Login: For user authentication and session management.

SQLite: A simple, file-based database for storing user and task data.

Werkzeug: A library used for securely hashing passwords.

Features
User Registration: Allows new users to register for the app by providing a username and password.

Login & Logout: Secure login and logout functionality using Flask-Login.

Task Management:

Add Tasks: Users can create tasks with details like title, description, due date, priority, and category.

View Tasks: Displays a list of tasks for the logged-in user.

Update Tasks: Users can update the title, description, due date, priority, and completion status.

Delete Tasks: Users can delete their tasks.

Task Completion Status: Mark tasks as completed or not completed.

Task Categorization: Users can assign categories to tasks.

Priority Levels: Tasks can be categorized with priorities like High, Medium, and Low.

Installation Instructions
Prerequisites
Python 3.6+

pip (Python package manager)

Steps to Install
Clone the repository:

bash
Copy
Edit
git clone https://github.com/yourusername/student-task-manager.git
cd student-task-manager
Create a virtual environment (optional but recommended):

bash
Copy
Edit
python -m venv venv
Activate the virtual environment:

On Windows:

bash
Copy
Edit
.\venv\Scripts\activate
On macOS/Linux:

bash
Copy
Edit
source venv/bin/activate
Install the required dependencies:

bash
Copy
Edit
pip install -r requirements.txt
Set up the database:
The app uses SQLite for the database. Run the following command to create the tasks.db file:

bash
Copy
Edit
python
>>> from app import db
>>> db.create_all()
Usage
Run the application:
After setting up the virtual environment and installing dependencies, you can start the application by running:

bash
Copy
Edit
python app.py
Open the app:
Navigate to http://127.0.0.1:5000 in your browser to start using the Task Manager.

Registration and Login:

Register: If you’re a new user, navigate to /register to create an account.

Login: If you already have an account, log in using the /login page.

Add and manage tasks: After logging in, you can add, update, and delete tasks from the task list.

Project Structure
plaintext
Copy
Edit
student-task-manager/
├── app.py                # Main Flask application file
├── templates/            # HTML templates for the views
│   ├── add_task.html     # Add task form
│   ├── home.html         # Home page after login
│   ├── login.html        # Login page
│   ├── register.html     # Registration page
│   └── view_tasks.html   # List of user's tasks
├── static/               # Static files like CSS, JS
│   └── style.css         # Custom styles for the app
├── requirements.txt      # List of dependencies
└── tasks.db              # SQLite database (generated automatically)

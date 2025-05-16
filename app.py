from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import (LoginManager, UserMixin, login_user, login_required,
                         logout_user, current_user)
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'  # Change to a strong secret for production
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

# User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    tasks = db.relationship('Task', backref='owner', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Task model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    due_date = db.Column(db.Date, nullable=True)
    completed = db.Column(db.Boolean, default=False)
    category = db.Column(db.String(100), nullable=True)
    priority = db.Column(db.String(20), nullable=True)  # High, Medium, Low
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"<Task {self.title}>"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
@login_required
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm = request.form.get('confirm')

        if not username or not password or not confirm:
            flash('Please fill all the fields.')
            return redirect(url_for('register'))
        if password != confirm:
            flash('Passwords do not match.')
            return redirect(url_for('register'))
        if User.query.filter_by(username=username).first():
            flash('Username already exists.')
            return redirect(url_for('register'))

        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful. Please log in.')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Logged in successfully.')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password.')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('login'))

# View tasks list
@app.route('/tasks')
@login_required
def view_tasks():
    tasks = Task.query.filter_by(owner=current_user).order_by(Task.due_date).all()
    return render_template('view_tasks.html', tasks=tasks)

# Add new task (render form)
@app.route('/tasks/add', methods=['GET', 'POST'])
@login_required
def add_task():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        due_date_str = request.form.get('due_date')
        category = request.form.get('category')
        priority = request.form.get('priority')
        completed = True if request.form.get('completed') == 'on' else False

        due_date = None
        if due_date_str:
            try:
                due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
            except ValueError:
                flash('Invalid due date format.')
                return redirect(url_for('add_task'))

        if not title:
            flash('Task title is required.')
            return redirect(url_for('add_task'))

        new_task = Task(title=title,
                        description=description,
                        due_date=due_date,
                        category=category,
                        priority=priority,
                        completed=completed,
                        owner=current_user)

        db.session.add(new_task)
        db.session.commit()
        flash('Task added successfully.')
        return redirect(url_for('view_tasks'))

    return render_template('add_task.html')

# Update existing task
@app.route('/tasks/update/<int:task_id>', methods=['GET', 'POST'])
@login_required
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.owner != current_user:
        flash('You cannot edit this task.')
        return redirect(url_for('view_tasks'))

    if request.method == 'POST':
        task.title = request.form.get('title')
        task.description = request.form.get('description')
        due_date_str = request.form.get('due_date')
        task.category = request.form.get('category')
        task.priority = request.form.get('priority')
        task.completed = True if request.form.get('completed') == 'on' else False

        if due_date_str:
            try:
                task.due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
            except ValueError:
                flash('Invalid due date format.')
                return redirect(url_for('update_task', task_id=task_id))
        else:
            task.due_date = None

        if not task.title:
            flash('Task title is required.')
            return redirect(url_for('update_task', task_id=task_id))

        db.session.commit()
        flash('Task updated successfully.')
        return redirect(url_for('view_tasks'))

    return render_template('add_task.html', task=task)

# Delete task
@app.route('/tasks/delete/<int:task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.owner != current_user:
        flash('You cannot delete this task.')
        return redirect(url_for('view_tasks'))

    db.session.delete(task)
    db.session.commit()
    flash('Task deleted.')
    return redirect(url_for('view_tasks'))


if __name__ == '__main__':
    if not os.path.exists('tasks.db'):
        with app.app_context():
            db.create_all()
    app.run(debug=True)

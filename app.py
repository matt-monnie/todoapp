from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from flask_migrate import Migrate
from dotenv import load_dotenv
from passlib.hash import pbkdf2_sha256
import json
import requests
import os

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['API_KEY'] = os.getenv('API_KEY')
app.config['CITY'] = os.getenv('CITY')

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Database Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)

    def set_password(self, password):
        self.password_hash = pbkdf2_sha256.hash(password)

    def check_password(self, password):
        return pbkdf2_sha256.verify(password, self.password_hash)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(100), nullable=False)
    done = db.Column(db.Boolean, default=False)
    priority = db.Column(db.String(50), nullable=False, default='Medium')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    directions = db.Column(db.Text, nullable=False)
    ingredients = db.relationship('Ingredient', backref='recipe', lazy=True)
    
class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.String(50), nullable=False)
    unit = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# File to store to-do items
todos_file = os.path.join(app.root_path, 'data', 'todos.json')
recipes_file = os.path.join(app.root_path, 'data', 'recipes.json')

def load_data(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)
    return []

def save_data(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file)

@app.route('/')
def index():
    return render_template('index.html', title='Landing Page')

@app.route('/todo', methods=['GET', 'POST'])
@login_required
def todo():
    if request.method == 'POST':
        new_todo = request.form.get('new_todo')
        priority = request.form.get('priority', 'Medium')
        new_task = Task(task=new_todo, done=False, priority=priority, user_id=current_user.id)
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('todo'))
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return render_template('todo.html', tasks=tasks, title='To-Do List')

@app.route('/complete/<int:task_id>', methods=['POST'])
@login_required
def complete(task_id):
    task = Task.query.get(task_id)
    if task and task.user_id == current_user.id:
        task.done = True
        db.session.commit()
    return redirect(url_for('todo'))

@app.route('/delete/<int:task_id>', methods=['POST'])
@login_required
def delete(task_id):
    task = Task.query.get(task_id)
    if task and task.user_id == current_user.id:
        db.session.delete(task)
        db.session.commit()
    return redirect(url_for('todo'))

@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
@login_required
def edit(task_id):
    task = Task.query.get(task_id)
    if request.method == 'POST':
        task.task = request.form['task']
        task.priority = request.form['priority']
        db.session.commit()
        return redirect(url_for('todo'))
    return render_template('edit.html', task=task)

@app.route('/cookbook', methods=['GET', 'POST'])
def cookbook():
    recipes = Recipe.query.all()
    if request.method == 'POST':
        recipe_name = request.form.get('recipe_name')
        directions = request.form.get('directions')

        if recipe_name and directions:
            new_recipe = Recipe(name=recipe_name, directions=directions)
            db.session.add(new_recipe)
            db.session.commit() # Commit first to get the recipe ID

            quantities = request.form.getlist('ingredient_quantity[]')
            units = request.form.getlist('ingredient_unit[]')
            names = request.form.getlist('ingredient_name[]')
        
            for quantity, unit, name in zip(quantities, units, names):
                new_ingredient = Ingredient(quantity=quantity, unit=unit, name=name, recipe_id=new_recipe.id)
                db.session.add(new_ingredient)

            db.session.commit()
        return redirect(url_for('cookbook'))
    
    return render_template('cookbook.html', recipes=recipes, title='Cookbook')

@app.route('/recipes/<int:recipe_id>', methods=['GET'])
@login_required
def recipe_detail(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    ingredients = Ingredient.query.filter_by(recipe_id=recipe.id).all()
    ingredient_list = [{'quantity': ingr.quantity, 'unit': ingr.unit, 'name': ingr.name} for ingr in ingredients]
    recipe_details = {
        'name': recipe.name,
        'ingredients': ingredient_list,
        'directions': recipe.directions
    }
    return jsonify(recipe_details)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        existing_user = User.query.filter_by(username=username).first()
        if existing_user is None:
            new_user = User(username=username)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for('dashboard'))
    return render_template('register.html', title='Register')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('dashboard'))
    return render_template('login.html', title='Login')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    completed_tasks = sum(1 for task in tasks if task.done)
    pending_tasks = len(tasks) - completed_tasks

    print(f"Completed Tasks: {completed_tasks}, Pending Tasks: {pending_tasks}") # Debug
    return render_template('dashboard.html', completed_tasks=completed_tasks, pending_tasks=pending_tasks, title='Dashboard')

@app.route('/weather')
def weather():
    weather_url = f'http://api.openweathermap.org/data/2.5/weather?q={os.getenv('CITY')}&appid={os.getenv('API_KEY')}&units=imperial'
    weather_data = requests.get(weather_url).json()

    return render_template('weather.html', weather=weather_data, title='Weather')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

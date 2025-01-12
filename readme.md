# To-Do List and Cookbook Application

## Overview
This is a web application that allows users to manage their to-do lists and store recipes. Users can create, edit, complete, and delete tasks, as well as add recipes with ingredients and directions. The application also provides user authentication, prioritization for tasks, and a dashboard showing task analytics.

## Features
- **User Authentication**: Register, login, and logout functionality.
- **To-Do List**: Add, edit, complete, and delete tasks with priority and due dates.
- **Cookbook**: Add recipes with ingredients and directions, view details, and manage recipes.
- **Dashboard**: Visual analytics of completed and pending tasks.
- **Responsive Design**: Easy to use on both desktop and mobile devices.
- **Basic Weather Data**: Simple current weather and temperatur for city

## Installation

### Prerequisites
- Python 3.8+
- Virtual Environment
- SQLite (included with Python)
- Git

### Clone the Repository
To clone the repository, use the following command:
```bash
git clone https://github.com/username/todoapp.git
cd todoapp
```

### Set Up Virtural Environment
```bash
python3 -m venv venv
source venv/bin/activate # On Windows use 'venv\Scripts\activate'
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Configuration
Create a .env file in the root directory and add the following environment variables:
For the Weather API Key, you will need an API from somewhere like https://openweathermap.org/
```bash
SECRET_KEY=your_secret_key
SQLALCHEMY_DATABASE_URI=sqlite:///site.db
WEATHER_API_KEY=your_weather_api_key
```

### Database Migration
Initialize the database and apply migrations
```bash
flask db init
flask db migrate -m "Initial migration."
flask db upgrade
```

## Usage

### Running the Application
To run the application, use the following command
```bash
python app.py
```
Open web browser and navigate to [http://127.0.0.1:5000](http://127.0.0.1:5000)

### Adding Users
To create users, navigate to the registration page and register new accounts:
* Navigate to the To-Do page and click register
* Navigate to [http://127.0.0.1:5000/register](http://127.0.0.1:5000/register)
* Fill in the required field and submit the form

### Using the To-Do List
* Add Task: Enter the task details, select priority, then click 'Add'
* Edit Task: Click the 'Edit' link next to the task, update details, and save changes
* Complete Task: Click the 'Complete' button next to the task
* Delete Task: Click the 'Delete' button next to the task

### Using the Cookbook
* Add Recipe: Click 'Enter New Recipe', fill in the recipe information and submit the form
* View Recipe Details: Click on the name of the recipe to see the full details
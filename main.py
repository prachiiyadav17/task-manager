
from flask import Flask, render_template, request, redirect
import json
import os

app = Flask(__name__)

TASK_FILE = 'tasks.json'

# Load tasks from file
def load_tasks():
    if os.path.exists(TASK_FILE):
        with open(TASK_FILE, 'r') as f:
            return json.load(f)
    return []

# Save tasks to file
def save_tasks(tasks):
    with open(TASK_FILE, 'w') as f:
        json.dump(tasks, f)

@app.route('/')
def index():
    tasks = load_tasks()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    title = request.form['title']
    category = request.form['category']
    due = request.form['due']
    priority = request.form['priority']
    if title:
        tasks = load_tasks()
        tasks.append({
            'title': title,
            'category': category,
            'due': due,
            'priority': priority,
            'completed': False
        })
        save_tasks(tasks)
    return redirect('/')

@app.route('/complete/<int:index>')
def complete(index):
    tasks = load_tasks()
    tasks[index]['completed'] = True
    save_tasks(tasks)
    return redirect('/')

@app.route('/delete/<int:index>')
def delete(index):
    tasks = load_tasks()
    tasks.pop(index)
    save_tasks(tasks)
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81)

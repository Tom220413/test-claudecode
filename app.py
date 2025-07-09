from flask import Flask, render_template, request, redirect, url_for
from todo_model import TodoModel

app = Flask(__name__)

def get_todo_model():
    db_path = app.config.get('DATABASE', 'todo.db')
    return TodoModel(db_path)

@app.route('/')
def index():
    todo_model = get_todo_model()
    items = todo_model.get_all_items()
    return render_template('index.html', items=items)

@app.route('/add', methods=['POST'])
def add_item():
    todo_model = get_todo_model()
    task = request.form.get('task', '').strip()
    if task and len(task) <= 200:
        todo_model.add_item(task)
    return redirect(url_for('index'))

@app.route('/toggle/<int:item_id>', methods=['POST'])
def toggle_item(item_id):
    todo_model = get_todo_model()
    try:
        todo_model.toggle_completion(item_id)
    except Exception:
        pass
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
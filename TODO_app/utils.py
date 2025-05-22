# utils.py
import os
import json

def load_todos(filename="todo.json"):
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_todos(todos, filename="todo.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(todos, f, ensure_ascii=False, indent=4)

def load_completed():
        if os.path.exists("completed.json"):
            with open("completed.json", "r", encoding="utf-8") as f:
                return json.load(f)
        return []

def save_completed(todos, filename="completed.json"):
    completed = [todo for todo in todos if todo['completed']]
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(completed, f, ensure_ascii=False, indent=4)

def clear_completed(todo_filename="todo.json", completed_filename="completed.json"):
    with open(completed_filename, "w", encoding="utf-8") as f:
        f.write("[]")
    with open(todo_filename, "w", encoding="utf-8") as f:
        f.write("[]")

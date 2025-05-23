import os
import json

# TODOリスト用のjsonファイルの呼び出し
def load_todos(filename="todo.json"):
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# TODOリスト用のjsonファイルの書き込み、保存
def save_todos(todos, filename="todo.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(todos, f, ensure_ascii=False, indent=4)

# Achievementリスト用のjsonファイルの呼び出し
def load_completed(filename="completed.json"):
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# Achievementリスト用のjsonファイルの書き込み、保存
def save_completed(todos, filename="completed.json"):
    completed = [todo for todo in todos if todo['completed']]
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(completed, f, ensure_ascii=False, indent=4)

# jsonファイル初期化用
def clear_completed(todo_filename="todo.json", completed_filename="completed.json"):
    with open(completed_filename, "w", encoding="utf-8") as f:
        f.write("[]")
    with open(todo_filename, "w", encoding="utf-8") as f:
        f.write("[]")

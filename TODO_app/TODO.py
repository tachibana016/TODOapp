import flet as ft
from datetime import datetime
import time
import threading
import os
import json

# TODOリストを保存する関数
def save_todos(todos):
    with open("todo.json", "w", encoding="utf-8") as f:
        json.dump(todos, f, ensure_ascii=False, indent=4)

# TODOリストを読み込む関数
def load_todos():
    if os.path.exists("todo.json"):
        with open("todo.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def main(page: ft.Page):
    # ページタイトル
    page.title = "TODOアプリ"
    
    # ウィンドウの設定
    page.window.top = 20  
    page.window.left = 100  
    page.window.width = 500
    page.window.height = 700  
    page.window.minimizable = False 
    page.window.maximizable = False
    page.window.resizable = False
    
    # ナビゲーションバーでの画面遷移
    def change_screen(e):
        if e.control.selected_index == 0:
            go_to_page(page, "todo")
        elif e.control.selected_index == 1:
            go_to_page(page, "task")
        elif e.control.selected_index == 2:
            go_to_page(page, "settings")

        page.update()

    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.CHECK_BOX, label="TODO"),
            ft.NavigationBarDestination(icon=ft.Icons.CALENDAR_MONTH, label="TASK"),
            ft.NavigationBarDestination(icon=ft.Icons.SETTINGS, label="SETTING"),
        ],
        on_change=change_screen
    )

    # 初期画面をTODO画面に設定
    go_to_page(page, "todo")  

# 時計を表示するためのテキスト
clock_text = ft.Text("", size=50, weight=ft.FontWeight.BOLD)
calendar_text = ft.Text("", size=30, weight=ft.FontWeight.BOLD)

# 時間を更新する関数
def update_clock():
    while True:
        time_now = datetime.now().strftime("%H:%M:%S")  
        date_now = datetime.today().strftime("%F")  

        clock_text.value = time_now  
        clock_text.update()
        
        calendar_text.value = date_now
        calendar_text.update()
        time.sleep(1)  

# TODO画面
def todo_screen(page: ft.Page):
    new_todo = ft.TextField(hint_text="TODOリストに追加", expand=True)

    # TODOリストを読み込む
    todos = load_todos()
    todo_view = ft.Column(
        spacing=10,
        height=300,
        width=400,
        scroll=ft.ScrollMode.ALWAYS,
    )

    for todo in todos:
        todo_view.controls.append(ft.Checkbox(label=todo))

    # クリック時処理 ラベルの追加と画面更新
    def add_clicked(e):
        if new_todo.value:  # 入力が空でない場合のみ追加
            todo_view.controls.append(ft.Checkbox(label=new_todo.value))
            todos.append(new_todo.value)  # 新しいタスクをリストに追加
            save_todos(todos)  # TODOリストを保存
            new_todo.value = ""  # 入力フィールドをクリア
            page.update()  # UIを更新

    # タスク画面
    view = ft.Column(
        controls=[
            clock_text,
            calendar_text,
            todo_view,
            ft.Row(
                controls=[
                    new_todo,
                    ft.FloatingActionButton(icon=ft.Icons.ADD, on_click=add_clicked),
                ],
            ),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    # ページ追加
    page.add(view)

    # 時計を更新するスレッドを開始
    threading.Thread(target=update_clock, daemon=True).start()

def task_screen(page: ft.Page):
    page.add(ft.Text("タスク画面"))

def settings_screen(page: ft.Page):
    page.add(ft.Text("設定画面"))

# 画面遷移用関数 引数の文字列に対応したページへ遷移
def go_to_page(page: ft.Page, page_name: str):
    # 現在の画面をクリア
    page.clean()  
    
    if page_name == "todo":
        todo_screen(page)
    elif page_name == "task":
        task_screen(page)
    elif page_name == "settings":
        settings_screen(page)

# Fletアプリを起動
ft.app(main)


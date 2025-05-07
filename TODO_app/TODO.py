import flet as ft
from datetime import datetime
import time
import threading
import os
import json

# TODOリストを読み込む関数
def load_todos():
    if os.path.exists("todo.json"):
        with open("todo.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# TODOリストを保存する関数
def save_todos(todos):
    with open("todo.json", "w", encoding="utf-8") as f:
        json.dump(todos, f, ensure_ascii=False, indent=4)

def save_completed(todos):
    completed = [todo for todo in todos if todo['completed']]
    with open("completed.json", "w", encoding="utf-8") as f:
        json.dump(completed, f, ensure_ascii=False, indent=4)

# JSONファイルをクリアする関数
def clear_completed():
    with open("completed.json", "w", encoding="utf-8") as f:
        f.write("[]")  # 空のリストで初期化

def main(page: ft.Page):
    # ページタイトル
    page.title = "TODOアプリ"
    
    # ウィンドウ設定
    page.window.top = 30  
    page.window.left = 100  
    page.window.width = 500
    page.window.height = 700  
    page.window.minimizable = False 
    page.window.maximizable = False
    page.window.resizable = False
    
    # ナビゲーションバーでの画面遷移
    def change_screen(e):
        if e.control.selected_index == 0:
            go_to_page(page,"todo")
        elif e.control.selected_index == 1:
            go_to_page(page,"achievements")
        elif e.control.selected_index == 2:
            go_to_page(page,"settings")
        page.update()

    page.navigation_bar = ft.NavigationBar(
        destinations = [
            ft.NavigationBarDestination(icon = ft.Icons.CHECK_BOX, label = "TODO"),
            ft.NavigationBarDestination(icon = ft.Icons.CALENDAR_MONTH, label = "ACHIEVEMENTS"),
            ft.NavigationBarDestination(icon = ft.Icons.SETTINGS, label = "SETTING"),
        ],
        on_change = change_screen
    )
    
    # 初期画面をTODO画面に設定
    go_to_page(page, "todo")  

# 時計を表示するためのテキスト
clock_text = ft.Text("", size = 50, weight=ft.FontWeight.BOLD)
calendar_text = ft.Text("", size = 30, weight=ft.FontWeight.BOLD)

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
        height=350,
        width=400,
        scroll=ft.ScrollMode.ALWAYS,
    )

    # 現在編集中のTODO項目を追跡するための変数
    editing_index = None

    def create_todo_item(todo, index):
        def edit_todo(e):
            nonlocal editing_index
            editing_index = index  
            new_todo.value = todo['text']  # 編集用のテキストフィールドに値をセット
            page.update()
            update_todo_view()  # 表示を更新

        def delete_todo(e):
            todos.remove(todo)  # TODOリストから削除
            save_todos(todos)  # 保存
            update_todo_view()  # 表示を更新

        def toggle_completed(e):
            todo['completed'] = not todo['completed']  # 完了状態をトグル
            if todo['completed']:
                todo['completed_date'] = datetime.now().strftime("%Y-%m-%d")  # 完了日を記録
            else:
                todo.pop('completed_date', None)  # 完了日を削除
            save_todos(todos)  # 現在のTODOリストを保存
            save_completed(todos)  # 完了したTODOリストを保存
            update_todo_view()  # 表示を更新

        # メニュー項目を条件に応じて作成
        menu_items = [ft.PopupMenuItem(text="編集", on_click=edit_todo)]
        if editing_index is None:  # 編集中でない場合のみ削除項目を追加
            menu_items.append(ft.PopupMenuItem(text="削除", on_click=delete_todo))
        else:
            menu_items = [ft.PopupMenuItem(text="編集中")]

        return ft.Row(
            controls=[
                ft.Checkbox(
                    label=todo['text'],
                    value=todo['completed'],  # 完了状態をチェックボックスに反映
                    on_change=toggle_completed  # チェックボックスの状態が変わったときの処理
                ),
                
                ft.PopupMenuButton(
                    items=menu_items,  # 条件に応じたメニュー項目を使用
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )
    
    
    def update_todo_view():
        todo_view.controls.clear()
        for index, todo in enumerate(todos):
            if not todo['completed']:  # 完了していないTODO項目のみ表示
                todo_view.controls.append(create_todo_item(todo, index))
        page.update()


    # クリック時処理 ラベルの追加と画面更新
    def add_clicked(e):
        nonlocal editing_index
        # 入力が空でない場合のみ追加または更新
        if new_todo.value:  
            if editing_index is not None:  # 編集中の場合
                todos[editing_index]['text'] = new_todo.value  # 既存のTODOを更新
                editing_index = None  # 編集を終了
            else:  # 新しいTODOを追加
                todos.append({"text": new_todo.value, "completed": False})  # 完了状態を追加
            save_todos(todos)  # TODOリストを保存
            new_todo.value = ""  # 入力フィールドをクリア
            update_todo_view()  # 表示を更新

    # TODO画面 レイアウト
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
    
    # 初期表示の更新
    update_todo_view()

def achievements_screen(page: ft.Page):

    # クリアボタンがクリックされたときの処理
    def clear_button_clicked(e):
        clear_completed()  # JSONファイルをクリア
        achievements_view.controls.clear()  # 完了したタスクの表示をクリア
        update_completed_view()  # 完了したタスクの表示を更新

    def load_completed():
        if os.path.exists("completed.json"):
            with open("completed.json", "r", encoding="utf-8") as f:
                return json.load(f)
        return []
    # クリアボタン
    clear_button = ft.Button("完了したタスクをクリア", on_click=clear_button_clicked)

    achievements_view = ft.Column(
        spacing=10,
        height=350,
        width=400,
        scroll=ft.ScrollMode.ALWAYS,
    )

    completed_view = ft.Column(
        controls=[
            clock_text,
            calendar_text,
            achievements_view,
            ft.Row(
                controls=[],
            ),   
            clear_button,
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    def update_completed_view():
        completed = load_completed()  # 完了したTODO項目を再読み込み
        achievements_view.controls.clear()  # 既存の表示をクリア
        for todo in completed:
            completed_date = todo.get('completed_date', '未設定')  # 完了日を取得
            
            # 左側にタスク名、右側に完了日を配置するための行を作成
            row = ft.Row(
                [
                    ft.Text(todo['text'], size=20, width=250),  # タスク名
                    ft.Text(completed_date, size=20, width=120 )  # 完了日
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,  # 左右にスペースを均等に配置
                
            )
            achievements_view.controls.append(row)  # 行を追加
        page.update()  # ページを更新

    # ページに追加
    page.add(completed_view)

    update_completed_view()

def settings_screen(page: ft.Page):
    # 設定画面の内容を追加することができます
    page.add(ft.Text("設定画面", size=30))

def go_to_page(page: ft.Page, page_name: str):
    page.clean()  
    if page_name == "todo":
        todo_screen(page)
    elif page_name == "achievements":
        achievements_screen(page)  # 完了したTODO項目を表示する画面
    elif page_name == "settings":
        settings_screen(page)

ft.app(main)


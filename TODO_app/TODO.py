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

# 完了済みのタスクを保存
def save_completed(todos):
    completed = [todo for todo in todos if todo['completed']]
    with open("completed.json", "w", encoding="utf-8") as f:
        json.dump(completed, f, ensure_ascii=False, indent=4)

# JSONファイルをクリアする関数
def clear_completed():
    with open("completed.json", "w", encoding="utf-8") as f:

        # 空のリストで初期化
        f.write("[]")
    with open("todo.json", "w", encoding="utf-8") as f:

        # 空のリストで初期化
        f.write("[]")


# 現在のテーマを保持する変数
Mainback_color = ft.Colors.WHITE
Cardback_color = ft.Colors.GREY_200
text_color = ft.Colors.BLACK
text_size = 20
text_font = "Arial"

clock_text = ft.Text("", size = 50, weight=ft.FontWeight.BOLD,color=ft.Colors.BLUE_GREY_600,font_family="Kanit")
calendar_text = ft.Text("", size = 30, weight=ft.FontWeight.BOLD,color=ft.Colors.BLUE_GREY_600,font_family="Consolas")


def main(page: ft.Page):

    global Mainback_color
    global text_color
    global Cardback_color

    # ページタイトル
    page.title = "TODOアプリ"

    # ウィンドウ設定
    page.window.top = 30
    page.window.left = 100
    page.window.width = 500
    page.window.height = 700
    #page.window.minimizable = False
    #page.window.maximizable = False
    #page.window.resizable = False
    page.bgcolor = Mainback_color

    # ナビゲーションバーでの画面遷移
    def change_screen(e):
        if e.control.selected_index == 0:
            go_to_page(page,"todo")
        elif e.control.selected_index == 1:
            go_to_page(page,"achievements")
        elif e.control.selected_index == 2:
            go_to_page(page,"settings")

        page.update()

    # ナビゲーションバーのアイコン名称
    page.navigation_bar = ft.NavigationBar(
        destinations = [
            ft.NavigationBarDestination(icon = ft.Icons.CHECK_BOX, label = "TODO"),
            ft.NavigationBarDestination(icon = ft.Icons.STAR, label = "ACHIEVEMENTS"),
            ft.NavigationBarDestination(icon = ft.Icons.SETTINGS, label = "SETTING"),
        ],
        on_change = change_screen,
        bgcolor=ft.Colors.BLUE_GREY_600
    )

    # 初期画面をTODO画面に設定
    go_to_page(page, "todo")

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

    global Mainback_color
    global text_color
    global Cardback_color
    global text_font

    new_todo = ft.TextField(
        hint_text="TODOリストに追加",
        color=text_color,
        expand=True,
        bgcolor=Cardback_color,
        border_color=text_color,
        cursor_color=text_color,
    )

    # TODOリストを読み込む
    todos = load_todos()

    todo_list = ft.Column(
        spacing=10,
        height=320,
        width=400,
        scroll=ft.ScrollMode.ALWAYS,
    )

    # 現在編集中のTODO項目を追跡するための変数
    editing_index = None

    def create_todo_item(todo, index):
        # 編集処理
        def edit_todo(e):
            nonlocal editing_index
            editing_index = index

            # 編集用のテキストフィールドに値をセット
            new_todo.value = todo['text']

            # 表示を更新
            page.update()
            update_todo_view()

        # 削除処理
        def delete_todo(e):
            # TODOリストから削除
            todos.remove(todo)

            # 保存
            save_todos(todos)

            # 表示を更新
            update_todo_view()

        def toggle_completed(e):

            # 完了状態を確認
            todo['completed'] = not todo['completed']
            if todo['completed']:
                # 完了日を記録
                todo['completed_date'] = datetime.now().strftime("%Y-%m-%d")
            else:
                # 完了日を削除
                todo.pop('completed_date', None)

            # 現在のTODOリストを保存
            save_todos(todos)

            # 完了したTODOリストを保存
            save_completed(todos)

        # メニュー項目を条件に応じて作成
        menu_items = [ft.PopupMenuItem(text="編集", on_click=edit_todo)]

        # 編集中でない場合のみ削除項目を追加
        if editing_index is None:
            menu_items.append(ft.PopupMenuItem(text="削除", on_click=delete_todo))
        else:
            menu_items = [ft.PopupMenuItem(text="編集中")]

        return ft.Row(
            controls=[
                ft.Checkbox(

                    # 完了状態をチェックボックスに反映
                    value=todo['completed'],

                    # チェックボックスの状態が変わったときの処理
                    on_change=toggle_completed,
                ),
                ft.Text(
                    todo['text'],
                    color=text_color,
                    size=text_size,
                    font_family=text_font,
                ),
                ft.PopupMenuButton(
                    # 条件に応じたメニュー項目を使用
                    items=menu_items,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

    # リスト更新
    def update_todo_view():
        todo_list.controls.clear()

        # 完了していないTODO項目のみ表示
        for index, todo in enumerate(todos):
            if not todo['completed']:
                todo_list.controls.append(create_todo_item(todo, index))
        page.update()


    # クリック時処理 ラベルの追加と画面更新
    def add_clicked(e):
        nonlocal editing_index

        # 入力が空でない場合のみ追加または更新
        if new_todo.value:

            # 編集中の場合
            if editing_index is not None:
                # 既存のTODOを更新
                todos[editing_index]['text'] = new_todo.value
                editing_index = None

            else:
                # 新しいTODOを追加
                todos.append({"text": new_todo.value, "completed": False})
            save_todos(todos)
            new_todo.value = ""
            update_todo_view()

    # TODO画面 レイアウト
    todo_view = ft.Column(
        controls=[
            clock_text,
            calendar_text,
            ft.Card(
                color=Cardback_color,
                content=ft.Container(
                    content=ft.Column(
                        [
                            ft.ListTile(todo_list)
                        ]
                    )
                )
            ),
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
    page.add(todo_view)

    # 時計を更新するスレッドを開始
    threading.Thread(target=update_clock, daemon=True).start()

    # 初期表示の更新
    update_todo_view()

# 達成確認画面
def achievements_screen(page: ft.Page):

    global Mainback_color
    global text_color
    global Cardback_color

    def load_completed():
        if os.path.exists("completed.json"):
            with open("completed.json", "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    achievements_list = ft.Column(
        spacing=10,
        height=400,
        width=400,
        scroll=ft.ScrollMode.ALWAYS,
    )

    completed_view = ft.Column(
        controls=[
            clock_text,
            calendar_text,
            ft.Card(
                color=Cardback_color,
                content=ft.Container(
                    content=ft.Column(
                        [
                            ft.ListTile(achievements_list)
                        ]
                    )
                )
            ),
            ft.Row(
                controls=[],
            ),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    def update_completed_view():
        # 完了したTODO項目を再読み込み
        completed = load_completed()

        # 既存の表示をクリア
        achievements_list.controls.clear()

        for todo in completed:
            completed_date = todo.get('completed_date', '未設定')

            # 左側にタスク名、右側に完了日を配置するための行を作成
            row = ft.Row(
                [
                    # タスク名
                    ft.Text(
                        todo['text'],
                        size=text_size,
                        font_family=text_font,
                        color=text_color,

                        # オーバーフロー時に省略記号を表示
                        overflow=ft.TextOverflow.ELLIPSIS,

                        # 最大行数を設定
                        max_lines=2,

                        # 幅を設定してオーバーフローを発生させる
                        width=200,
                    ),
                    # 完了日
                    ft.Text(
                        completed_date,
                        size=text_size,
                        font_family=text_font,
                        color=text_color,
                        width=140,  # 幅を設定してオーバーフローを発生させる
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
            )
            achievements_list.controls.append(row)  # 行を追加
        page.update()  # ページを更新
    # ページに追加
    page.add(completed_view)
    update_completed_view()

def settings_screen(page: ft.Page):

    global Mainback_color
    global text_color
    global text_size
    global Cardback_color

    # クリアボタンがクリックされたときの処理
    def clear_button_clicked(e):
        # JSONファイルをクリア
        clear_completed()
        page.close(e.control.parent)

    def cancell_button_clicked(e):
        page.close(e.control.parent)

    # リストクリア選択時処理
    def clear_chois(e):
        page.open(
            ft.AlertDialog(
                title=ft.Text("リストの初期化"),
                content=ft.Text("TODOとACHIEVEMENTSを初期化します。\n復元できません。"),
                actions=material_actions,
            )
        )

    def change_color(e):
        global Mainback_color
        global text_color
        global Cardback_color
        global clock_text
        global calendar_text

        if Mainback_color == ft.Colors.WHITE :
            Mainback_color = ft.Colors.GREY_900
            Cardback_color = ft.Colors.GREY_700
            text_color = ft.Colors.WHITE
            page.bgcolor = Mainback_color
            go_to_page(page,"settings")

        elif Mainback_color == ft.Colors.GREY_900:
            Mainback_color = ft.Colors.WHITE
            Cardback_color = ft.Colors.GREY_200
            text_color = ft.Colors.BLACK
            page.bgcolor = Mainback_color
            go_to_page(page,"settings")

    def change_text_size(e):
        global text_size

        # ドロップダウンから選択されたサイズを取得
        selected_size = e.control.value
        # 選択されたサイズを整数に変換
        text_size = int(selected_size)

        # ページ全体のテキストサイズを変更
        for control in page.controls:
            if isinstance(control, ft.Text):
                control.size = text_size
        page.update()

    def change_text_font(e):
        global text_font

        # ドロップダウンから選択されたサイズを取得
        selected_font = e.control.value
        # 選択されたサイズを整数に変換
        text_font = selected_font

        # ページ全体のテキストサイズを変更
        for control in page.controls:
            if isinstance(control, ft.Text):
                control.font_family = text_font
        page.update()  # ページを更新

    # テーマ切り替えボタン
    toggle_button = ft.Button(
        text="モードの切り替え",
        on_click=change_color,
        color=text_color,
        bgcolor=Mainback_color,
    )

    # テキストサイズ変更用のドロップダウン
    text_size_dropdown = ft.Dropdown(
        hint_text=text_size,
        color=text_color,
        options=[
            ft.dropdown.Option("14", "14"),
            ft.dropdown.Option("16", "16"),
            ft.dropdown.Option("18", "18"),
            ft.dropdown.Option("20", "20"),
            ft.dropdown.Option("22", "22"),
            ft.dropdown.Option("24", "24"),
        ],
        on_change=change_text_size,
    )

    # テキストサイズ変更用のドロップダウン
    text_font_dropdown = ft.Dropdown(
        hint_text=text_font,
        color=text_color,
        options=[
            ft.dropdown.Option("Noto Sans JP", "Noto Sans JP"),
            ft.dropdown.Option("Yu Gothic", "Yu Gothic"),
            ft.dropdown.Option("Meiryo", "Meiryo"),
            ft.dropdown.Option("Hiragino Sans", "Hiragino Sans"),
            ft.dropdown.Option("MS Gothic", "MS Gothic"),
            ft.dropdown.Option("MS Mincho", "MS Mincho"),
        ],
        on_change=change_text_font,
    )

    material_actions = [
        ft.TextButton(text="Yes", on_click=clear_button_clicked),
        ft.TextButton(text="No",on_click=cancell_button_clicked),
    ]

    settings_list = ft.Card(
            color=Cardback_color,
            content=ft.Column(
                [
                    ft.Divider(height=20),
                    ft.ListTile(
                        title=ft.Text(
                            "アカウント",size=20,color=text_color
                        ),
                        trailing=ft.PopupMenuButton(
                            items=[
                                ft.PopupMenuItem(text="Item 1"),
                                ft.PopupMenuItem(text="Item 2"),
                            ],
                        ),
                    ),
                    ft.Divider(height=20),
                    ft.ListTile(
                        is_three_line=False,
                        title=ft.Text("テキストサイズの変更", size=20, color=text_color),
                        trailing=ft.Column(
                            [text_size_dropdown],  # ドロップダウンを追加
                            alignment=ft.MainAxisAlignment.END,
                        ),
                    ),
                    ft.Divider(height=20),
                    ft.ListTile(
                        title=ft.Text("フォントの変更", size=20, color=text_color),
                        trailing=ft.Column(
                            [text_font_dropdown],  # ドロップダウンを追加
                            alignment=ft.MainAxisAlignment.END,
                        ),
                    ),
                    ft.Divider(height=20),
                    ft.ListTile(
                        title=ft.Text("テーマ設定",size=20,color=text_color),
                        trailing=ft.Column(
                            [toggle_button],
                            alignment=ft.MainAxisAlignment.END,
                        ),
                    ),
                    ft.Divider(height=20),
                    ft.ListTile(
                        title=ft.Text(
                            "リストの並び替え",size=20,color=text_color,
                        ),
                        trailing=ft.Column(
                            [text_font_dropdown],  # ドロップダウンを追加
                            alignment=ft.MainAxisAlignment.END,
                        ),
                    ),
                    ft.Divider(height=20),
                    ft.ListTile(
                        title=ft.Text("リストの初期化",size=20,color=text_color), dense=True,
                        trailing=ft.Column(
                            [ft.TextButton("execution",on_click=clear_chois,)],
                            alignment=ft.MainAxisAlignment.END,
                        ),
                    ),
                    ft.Divider(height=20),
                ],
            ),
        )

    # 設定ビューを作成
    settings_view = ft.Column(
        controls=[
            settings_list,
        ],
    )

    page.add(settings_view)

# 画面遷移
def go_to_page(page: ft.Page, page_name: str):
    page.clean()
    if page_name == "todo":
        todo_screen(page)
    elif page_name == "achievements":
        achievements_screen(page)
    elif page_name == "settings":
        settings_screen(page)

ft.app(main)

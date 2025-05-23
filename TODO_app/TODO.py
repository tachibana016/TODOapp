import flet as ft
from datetime import datetime
import time
from utils import load_todos,save_todos,save_completed

# FletのPageオブジェクトと設定オブジェクトを受け取り
def todo_screen(page: ft.Page,app_setting):

    # 時計とカレンダーの設定
    clock = ft.Text("", size=50, weight=ft.FontWeight.BOLD,color=ft.Colors.BLUE_GREY_600,font_family="Kanit")
    calendar = ft.Text("", size=30, weight=ft.FontWeight.BOLD,color=ft.Colors.BLUE_GREY_600,font_family="Consolas")

    # app_settingから
    app_setting.clock_text = clock
    app_setting.calendar_text = calendar

    # TODOリストに追加用のテキストフィールド
    new_todo = ft.TextField(
        hint_text="TODOリストに追加",
        color=app_setting.text_color,
        expand=True,
        bgcolor=app_setting.card_bg_color,
        border_color=app_setting.text_color,
        cursor_color=app_setting.text_color,
    )


    # TODOリストを読み込む
    todos = load_todos()

    # TODOリスト用レイアウト
    todo_list = ft.Column(
        spacing=10,
        height=320,
        width=400,
        scroll=ft.ScrollMode.ALWAYS,
    )

    # 現在編集中のTODO項目を追跡するための変数
    editing_index = None

    # TODOリストの編集、削除処理用レイアウト
    def create_todo_item(todo, index):
        # 編集処理
        def edit_todo(e):
            nonlocal editing_index
            editing_index = index

            # 編集用のテキストフィールドに値をセット
            new_todo.value = todo['text']
            update_todo_view()

        # 削除処理
        def delete_todo(e):
            # TODOリストから削除
            todos.remove(todo)

            # 保存
            save_todos(todos)
            update_todo_view()

        # チェックされたときの処理
        def check_completed(e):

            # 完了状態を確認
            todo['completed'] = not todo['completed']
            if todo['completed']:
                # 完了日を記録
                todo['completed_date'] = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
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
                    on_change=check_completed,
                ),
                ft.Text(
                    todo['text'],
                    size=app_setting.text_size,
                    color=app_setting.text_color,
                    font_family=app_setting.text_font
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


    # クリック時、ラベルの追加と画面更新
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

    # TODO画面レイアウト
    todo_view = ft.Column(
        controls=[
            ft.Card(
                color=app_setting.card_bg_color,
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
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
        ],
    )
    # 初期表示更新
    update_todo_view()
    app_setting.start_clock_thread()
    app_setting.save()

    # レイアウトを返す
    return ft.Column(
        [
            clock,
            calendar,
            todo_view,
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )


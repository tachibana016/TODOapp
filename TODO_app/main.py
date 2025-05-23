import flet as ft
from todo import todo_screen
from achievement import achievement_screen
from setting import setting_screen
from app_setting import App_Setting

def main(page: ft.Page):
    app_setting = App_Setting()

    # ページタイトルとウィンドウ設定
    page.title = "TODOアプリ"
    page.window.top = 30
    page.window.left = 100
    page.window.width = 500
    page.window.height = 700
    page.bgcolor = app_setting.main_bg_color

    # 時計スレッドを一度だけ起動
    app_setting.start_clock_thread()

    # ナビゲーションバー用の画面遷移コード
    def render(index):
        page.clean()
        if index == 0:
            page.add(todo_screen(page, app_setting))
        elif index == 1:
            page.add(achievement_screen(app_setting))
        elif index == 2:
            page.add(setting_screen(page, app_setting,on_setting_changed))

    # ナビゲーションバーの番号の取得
    def on_setting_changed():
        render(page.navigation_bar.selected_index)

    # ナビゲーションバーのクリック時処理
    def change_screen(e):
        render(e.control.selected_index)

    # ナビゲーションバーのレイアウト
    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.CHECK_BOX, label="TODO"),
            ft.NavigationBarDestination(icon=ft.Icons.STAR, label="ACHIEVEMENT"),
            ft.NavigationBarDestination(icon=ft.Icons.SETTINGS, label="SETTING"),
        ],
        on_change=change_screen
    )

    # 最初の画面（TODO）を表示
    render(0)

ft.app(main)

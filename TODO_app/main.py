import flet as ft
from todo import todo_screen
from achievements import achievements_screen
from setting import setting_screen
from app_setting import AppSettings

def main(page: ft.Page):
    settings = AppSettings()

    # ページタイトルとウィンドウ設定
    page.title = "TODOアプリ"
    page.window.top = 30
    page.window.left = 100
    page.window.width = 500
    page.window.height = 700
    page.window.minimizable = False
    page.window.maximizable = False
    page.window.resizable = False
    page.bgcolor = settings.main_bg_color

    # 時計スレッドを一度だけ起動
    settings.start_clock_thread()

    def render(index):
        page.clean()
        if index == 0:
            page.add(todo_screen(page, settings))
        elif index == 1:
            page.add(achievements_screen(settings))
        elif index == 2:
            page.add(setting_screen(page, settings))

    def on_settings_changed():
        render(page.navigation_bar.selected_index)

    def change_screen(e):
        render(e.control.selected_index)

    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.CHECK_BOX, label="TODO"),
            ft.NavigationBarDestination(icon=ft.Icons.STAR, label="ACHIEVEMENTS"),
            ft.NavigationBarDestination(icon=ft.Icons.SETTINGS, label="SETTING"),
        ],
        on_change=change_screen
    )

    # 最初の画面（TODO）を表示
    render(0)

ft.app(main)

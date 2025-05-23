import flet as ft
from utils import clear_completed

def setting_screen(page: ft.Page, app_setting, on_setting_changed):

    page.bgcolor = app_setting.main_bg_color

    def change_color(e):
        app_setting.toggle_theme()
        on_setting_changed()

    def change_text_size(e):
        app_setting.text_size = int(e.control.value)
        app_setting.update_text_styles()
        on_setting_changed()

    def change_text_font(e):
        app_setting.text_font = e.control.value
        app_setting.update_text_styles()
        on_setting_changed()

    def change_sort_order(e):
        app_setting.sort_ascending = e.control.value  # True or False
        on_setting_changed()


    def clear_button_clicked(e):
        clear_completed()
        page.close(e.control.parent)

    def cancel_button_clicked(e):
        page.close(e.control.parent)

    def clear_choice(e):
        page.open(
            ft.AlertDialog(
                title=ft.Text("リストの初期化"),
                content=ft.Text("TODOとACHIEVEMENTを初期化します。\n復元できません。"),
                actions=[
                    ft.TextButton(text="Yes", on_click=clear_button_clicked),
                    ft.TextButton(text="No", on_click=cancel_button_clicked),
                ],
            )
        )
        page.update()


    text_size_dropdown = ft.Dropdown(
        label=str(app_setting.text_size),
        color=app_setting.text_color,
        options=[ft.dropdown.Option(str(s)) for s in range(14, 26, 2)],
        on_change=change_text_size,
    )

    text_font_dropdown = ft.Dropdown(
        label=app_setting.text_font,
        color=app_setting.text_color,
        options=[
            ft.dropdown.Option(f) for f in [
                "Noto Sans JP",
                "Yu Gothic",
                "Hiragino Sans",
                "MS Gothic",
                "MS Mincho"
            ]
        ],
        on_change=change_text_font,
    )


    setting_list = ft.Card(
        color=app_setting.card_bg_color,
            content=ft.Column(
                    [
                        ft.Divider(height=20),
                        ft.ListTile(
                            title=ft.Text(
                                "アカウント",size=20,color=app_setting.text_color
                            ),
                            trailing=ft.PopupMenuButton(
                                items=[
                                    ft.PopupMenuItem(text="実装予定"),
                                ],
                            ),
                        ),
                        ft.Divider(height=20),
                        ft.ListTile(
                            is_three_line=False,
                            title=ft.Text("テキストサイズの変更", size=20, color=app_setting.text_color),
                            trailing=ft.Column(
                                # ドロップダウンを追加
                                [text_size_dropdown],
                                alignment=ft.MainAxisAlignment.END,
                            ),
                        ),
                        ft.Divider(height=20),
                        ft.ListTile(
                            title=ft.Text("フォントの変更", size=20, color=app_setting.text_color),
                            trailing=ft.Column(
                                # ドロップダウンを追加
                                [text_font_dropdown],
                                alignment=ft.MainAxisAlignment.END,
                            ),
                        ),
                        ft.Divider(height=20),
                        ft.ListTile(
                            title=ft.Text("テーマ設定",size=20,color=app_setting.text_color),
                            trailing=ft.Column(
                                [ft.ElevatedButton(
                                    text="モードの切り替え",
                                    on_click=change_color,
                                    bgcolor=app_setting.card_bg_color,
                                    color=app_setting.text_color,
                                )
                                ],
                                alignment=ft.MainAxisAlignment.END,
                            ),
                        ),
                        ft.Divider(height=20),
                        ft.ListTile(
                            title=ft.Text("並び順（昇順/降順）", size=20, color=app_setting.text_color),
                            trailing=ft.Switch(
                                value=app_setting.sort_ascending,
                                on_change=change_sort_order
                            ),
                        ),
                        ft.Divider(height=20),
                        ft.ListTile(
                            title=ft.Text("リストの初期化",size=20,color=app_setting.text_color), dense=True,
                            trailing=ft.Column(
                                [ft.TextButton("execution",on_click=clear_choice)],
                                alignment=ft.MainAxisAlignment.END,
                            ),
                        ),
                        ft.Divider(height=20),
                    ],
                ),
    )

    return ft.Column([setting_list])

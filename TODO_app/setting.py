import flet as ft

def setting_screen(page: ft.Page, settings):
    def change_color(e):
        settings.toggle_theme()
        page.bgcolor = settings.main_bg_color
        page.clean()
        page.add(setting_screen(page, settings))

    def change_text_size(e):
        settings.text_size = int(e.control.value)
        page.clean()
        page.add(setting_screen(page, settings))

    def change_text_font(e):
        settings.text_font = e.control.value
        page.clean()
        page.add(setting_screen(page, settings))

    def clear_button_clicked(e):
        page.close(e.control.parent)

    def cancell_button_clicked(e):
        page.close(e.control.parent)

    def clear_chois(e):
        page.open(
            ft.AlertDialog(
                title=ft.Text("リストの初期化"),
                content=ft.Text("TODOとACHIEVEMENTSを初期化します。\n復元できません。"),
                actions=material_actions,
            )
        )

    text_size_dropdown = ft.Dropdown(
        hint_text=str(settings.text_size),
        color=settings.text_color,
        options=[ft.dropdown.Option(str(s), str(s)) for s in range(14, 26, 2)],
        on_change=change_text_size,
    )

    text_font_dropdown = ft.Dropdown(
        hint_text=settings.text_font,
        color=settings.text_color,
        options=[
            ft.dropdown.Option(f, f) for f in [
                "Noto Sans JP", "Yu Gothic", "Meiryo", "Hiragino Sans", "MS Gothic", "MS Mincho"
            ]
        ],
        on_change=change_text_font,
    )

    material_actions = [
        ft.TextButton(text="Yes", on_click=clear_button_clicked),
        ft.TextButton(text="No", on_click=cancell_button_clicked),
    ]

    setting_list = ft.Card(
        color=settings.card_bg_color,
        content=ft.Column(
            [
                ft.Divider(height=20),
                ft.ListTile(
                    title=ft.Text("アカウント", size=20, color=settings.text_color),
                    trailing=ft.PopupMenuButton(
                        items=[
                            ft.PopupMenuItem(text="Item 1"),
                            ft.PopupMenuItem(text="Item 2"),
                        ],
                    ),
                ),
                ft.Divider(height=20),
                ft.ListTile(
                    title=ft.Text("テキストサイズの変更", size=20, color=settings.text_color),
                    trailing=ft.Column([text_size_dropdown], alignment=ft.MainAxisAlignment.END),
                ),
                ft.Divider(height=20),
                ft.ListTile(
                    title=ft.Text("フォントの変更", size=20, color=settings.text_color),
                    trailing=ft.Column([text_font_dropdown], alignment=ft.MainAxisAlignment.END),
                ),
                ft.Divider(height=20),
                ft.ListTile(
                    title=ft.Text("テーマ設定", size=20, color=settings.text_color),
                    trailing=ft.Column(
                        [
                            ft.ElevatedButton(
                                text="モードの切り替え",
                                on_click=change_color,
                                bgcolor=settings.card_bg_color,
                                color=settings.text_color,
                            )
                        ],
                        alignment=ft.MainAxisAlignment.END,
                    ),
                ),
                ft.Divider(height=20),
                    ft.ListTile(
                        title=ft.Text(
                            "リストの並び替え",size=20,
                        ),
                        trailing=ft.Column(
                            [text_font_dropdown],  # ドロップダウンを追加
                            alignment=ft.MainAxisAlignment.END,
                        ),
                    ),
                ft.Divider(height=20),
                ft.ListTile(
                    title=ft.Text("リストの初期化", size=20, color=settings.text_color),
                    trailing=ft.Column(
                        [
                            ft.TextButton("execution", on_click=clear_chois),
                        ],
                        alignment=ft.MainAxisAlignment.END,
                    ),
                ),
                ft.Divider(height=20),
            ]
        )
    )


    return ft.Column([setting_list])

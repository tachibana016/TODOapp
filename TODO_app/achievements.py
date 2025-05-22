import flet as ft
from utils import load_completed

# 達成確認画面
def achievements_screen(settings):

    settings.start_clock_thread()

    # UI表示に使う既存の Text を使う
    clock = settings.clock_text
    calendar = settings.calendar_text

    achievements_list = ft.Column(
        spacing=10,
        height=400,
        width=400,
        scroll=ft.ScrollMode.ALWAYS,
    )

    completed_view = ft.Column(
        controls=[
            ft.Card(
                color=settings.card_bg_color,
                content=ft.Container(
                    content=ft.Column(
                        [ft.ListTile(achievements_list)]
                    )
                )
            ),
            ft.Row(controls=[]),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    def update_completed_view():
        # 完了したTODO項目を再読み込み
        completed = load_completed()

        achievements_list.controls.clear()

        for todo in completed:
            completed_date = todo.get('completed_date', '未設定')

            row = ft.Row(
                [
                    ft.Text(
                        todo['text'],
                        size=settings.text_size,
                        color=settings.text_color,
                        font_family=settings.text_font,
                        overflow=ft.TextOverflow.ELLIPSIS,
                        max_lines=2,
                        width=200,
                    ),
                    ft.Text(
                        completed_date,
                        size=settings.text_size,
                        color=settings.text_color,
                        font_family=settings.text_font,
                        width=140,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
            )
            achievements_list.controls.append(row)

    # 初期読み込み
    update_completed_view()

    return ft.Column(
        [
            clock,
            calendar,
            completed_view
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

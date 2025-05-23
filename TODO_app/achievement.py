import flet as ft
from utils import load_completed
from datetime import datetime

# 達成確認画面
def achievement_screen(app_setting):

    # 時計とカレンダーの設定
    clock = ft.Text("", size=50, weight=ft.FontWeight.BOLD,color=ft.Colors.BLUE_GREY_600,font_family="Kanit")
    calendar = ft.Text("", size=30, weight=ft.FontWeight.BOLD,color=ft.Colors.BLUE_GREY_600,font_family="Consolas")

    app_setting.clock_text = clock
    app_setting.calendar_text = calendar

    # Achievementリスト用のレイアウト
    achievement_list = ft.Column(
        spacing=10,
        height=400,
        width=400,
        scroll=ft.ScrollMode.ALWAYS,
    )

    # Achievement画面レイアウト
    completed_view = ft.Column(
        controls=[
            ft.Card(
                color=app_setting.card_bg_color,
                content=ft.Container(
                    content=ft.Column(
                        [ft.ListTile(achievement_list)]
                    )
                )
            ),
            ft.Row(controls=[]),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    def update_completed_view():

        # jsonファイル呼び出し
        completed = load_completed()
        # 達成日に合わせてソート
        completed.sort(key=lambda x: x.get("completed_date", ""), reverse=not app_setting.sort_ascending)
        achievement_list.controls.clear()


        for todo in completed:
            completed_date_raw = todo.get('completed_date', '')
            try:
                # 文字列をdatetimeに変換（ "%Y-%m-%d-%H-%M-%S" 形式）
                dt = datetime.strptime(completed_date_raw, "%Y-%m-%d-%H-%M-%S")
                # 日付部分だけ表示
                completed_date = dt.strftime("%Y-%m-%d")
            # エラー処理
            except ValueError:
                completed_date = "未設定"

            row = ft.Row(
                [
                    ft.Text(
                        todo['text'],
                        size=app_setting.text_size,
                        color=app_setting.text_color,
                        font_family=app_setting.text_font,

                        # オーバーフロー設定
                        overflow=ft.TextOverflow.ELLIPSIS,
                        max_lines=2,
                        width=200,
                    ),
                    ft.Text(
                        completed_date,
                        size=app_setting.text_size,
                        color=app_setting.text_color,
                        font_family=app_setting.text_font,
                        width=140,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
            )
            achievement_list.controls.append(row)

    # 初期読み込み
    update_completed_view()
    app_setting.start_clock_thread()
    app_setting.save()

    # レイアウトを返す
    return ft.Column(
        [
            clock,
            calendar,
            completed_view
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

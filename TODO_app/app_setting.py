from datetime import datetime
import time
import threading
import flet as ft

class AppSettings:
    def __init__(self):
        self.main_bg_color = "white"
        self.card_bg_color = "grey200"
        self.text_color = "black"
        self.text_size = 16
        self.text_font = "Noto Sans JP"

        # Textオブジェクトとして初期化（あとで画面に追加可能）
        self.clock_text = ft.Text("")
        self.calendar_text = ft.Text("")

    def toggle_theme(self):
        if self.main_bg_color == "white":
            self.main_bg_color = "grey900"
            self.card_bg_color = "grey700"
            self.text_color = "white"
        else:
            self.main_bg_color = "white"
            self.card_bg_color = "grey200"
            self.text_color = "black"

        self.update_text_styles()

    def update_text_styles(self):
        for t in [self.clock_text, self.calendar_text]:
            t.color = self.text_color
            t.size = self.text_size
            t.font_family = self.text_font
            t.update()  # 更新反映

    def update_clock(self):
        while True:
            now = datetime.now()
            self.clock_text.value = now.strftime("%H:%M:%S")
            self.calendar_text.value = now.strftime("%Y-%m-%d")

            try:
                self.clock_text.update()
                self.calendar_text.update()
            except Exception:
                # まだページに追加されていないならスルー
                pass

            time.sleep(1)


    def start_clock_thread(self):
        thread = threading.Thread(target=self.update_clock, daemon=True)
        thread.start()


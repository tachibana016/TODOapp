import json
import os
from datetime import datetime
import time
import threading
import flet as ft
class App_Setting:
    def __init__(self):
        # 初期設定
        self.main_bg_color = "white"
        self.card_bg_color = "grey200"
        self.text_color = "black"
        self.text_size = 16
        self.text_font = "Noto Sans JP"
        self.sort_ascending = False

        # Textオブジェクトとして初期化（あとで画面に追加）
        self.clock_text = ft.Text("")
        self.calendar_text = ft.Text("")

        # 保存ファイルパス
        self.settings_file = "setting.json"
        self.load()

    # 背景色に合わせてレイアウトカラーの切り替え
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

    # 切り替えられたレイアウトの反映
    def update_text_styles(self):
        for t in [self.clock_text, self.calendar_text]:
            t.color = self.text_color
            t.size = self.text_size
            t.font_family = self.text_font
            # 更新反映
            t.update()

    # 時計とカレンダーを1秒ごとに更新
    def update_clock(self):
        while True:
            now = datetime.now()
            self.clock_text.value = now.strftime("%H:%M:%S")
            self.calendar_text.value = now.strftime("%Y-%m-%d")

            try:
                self.clock_text.update()
                self.calendar_text.update()
            except Exception:
                pass

            time.sleep(1)

    # 時計の処理開始用
    def start_clock_thread(self):
        thread = threading.Thread(target=self.update_clock, daemon=True)
        thread.start()

    # 設定内容書き込み、保存用
    def save(self):
        data = {
            "main_bg_color": self.main_bg_color,
            "card_bg_color": self.card_bg_color,
            "text_color": self.text_color,
            "text_size": self.text_size,
            "text_font": self.text_font
        }
        with open(self.settings_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    # 設定内容呼び出し用
    def load(self):
        if os.path.exists(self.settings_file):
            with open(self.settings_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.main_bg_color = data.get("main_bg_color", self.main_bg_color)
                self.card_bg_color = data.get("card_bg_color", self.card_bg_color)
                self.text_color = data.get("text_color", self.text_color)
                self.text_size = data.get("text_size", self.text_size)
                self.text_font = data.get("text_font", self.text_font)

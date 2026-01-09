"""
タイマープラグイン
"""

from horloq.plugins.base import PluginBase
import customtkinter as ctk
from datetime import timedelta


class TimerPlugin(PluginBase):
    """カウントダウンタイマープラグイン"""
    
    def __init__(self, app_context):
        super().__init__(app_context)
        self.timer_window = None
        self.remaining_time = 0
        self.is_running = False
        self.after_id = None
    
    def initialize(self) -> bool:
        """初期化"""
        return True
    
    def create_widget(self, parent):
        """ウィジェットを作成"""
        frame = ctk.CTkFrame(parent)
        
        button = ctk.CTkButton(
            frame,
            text="⏱️ タイマーを開く",
            command=self._open_timer_window,
        )
        button.pack(pady=10, padx=20)
        
        return frame
    
    def _open_timer_window(self):
        """タイマーウィンドウを開く"""
        if self.timer_window and self.timer_window.winfo_exists():
            self.timer_window.focus()
            return
        
        self.timer_window = ctk.CTkToplevel()
        self.timer_window.title("タイマー")
        self.timer_window.geometry("350x500")
        self.timer_window.attributes("-topmost", True)  # 最前面固定
        
        # タイマー表示
        self.time_label = ctk.CTkLabel(
            self.timer_window,
            text="00:00:00",
            font=("Arial", 48, "bold"),
        )
        self.time_label.pack(pady=30)
        
        # プリセットボタン
        preset_frame = ctk.CTkFrame(self.timer_window)
        preset_frame.pack(pady=10)
        
        presets = [
            ("1分", 60),
            ("3分", 180),
            ("5分", 300),
            ("10分", 600),
        ]
        
        for label, seconds in presets:
            btn = ctk.CTkButton(
                preset_frame,
                text=label,
                command=lambda s=seconds: self._set_timer(s),
                width=60,
            )
            btn.pack(side="left", padx=5)
        
        # 自由入力セクション
        input_label = ctk.CTkLabel(
            self.timer_window,
            text="または自由入力:",
            font=("Arial", 12),
        )
        input_label.pack(pady=(10, 5))
        
        input_frame = ctk.CTkFrame(self.timer_window)
        input_frame.pack(pady=5)
        
        # 時間入力
        ctk.CTkLabel(
            input_frame,
            text="時:",
            font=("Arial", 12),
        ).pack(side="left", padx=5)
        
        self.hours_entry = ctk.CTkEntry(
            input_frame,
            width=50,
            font=("Arial", 14),
        )
        self.hours_entry.insert(0, "0")
        self.hours_entry.pack(side="left", padx=2)
        
        # 分入力
        ctk.CTkLabel(
            input_frame,
            text="分:",
            font=("Arial", 12),
        ).pack(side="left", padx=5)
        
        self.minutes_entry = ctk.CTkEntry(
            input_frame,
            width=50,
            font=("Arial", 14),
        )
        self.minutes_entry.insert(0, "0")
        self.minutes_entry.pack(side="left", padx=2)
        
        # 秒入力
        ctk.CTkLabel(
            input_frame,
            text="秒:",
            font=("Arial", 12),
        ).pack(side="left", padx=5)
        
        self.seconds_entry = ctk.CTkEntry(
            input_frame,
            width=50,
            font=("Arial", 14),
        )
        self.seconds_entry.insert(0, "0")
        self.seconds_entry.pack(side="left", padx=2)
        
        # 設定ボタン
        set_btn = ctk.CTkButton(
            input_frame,
            text="設定",
            command=self._set_custom_timer,
            width=60,
        )
        set_btn.pack(side="left", padx=5)
        
        # コントロールボタン
        control_frame = ctk.CTkFrame(self.timer_window)
        control_frame.pack(pady=20)
        
        self.start_btn = ctk.CTkButton(
            control_frame,
            text="開始",
            command=self._start_timer,
        )
        self.start_btn.pack(side="left", padx=5)
        
        self.stop_btn = ctk.CTkButton(
            control_frame,
            text="停止",
            command=self._stop_timer,
            state="disabled",
        )
        self.stop_btn.pack(side="left", padx=5)
        
        self.reset_btn = ctk.CTkButton(
            control_frame,
            text="リセット",
            command=self._reset_timer,
        )
        self.reset_btn.pack(side="left", padx=5)
    
    def _set_timer(self, seconds: int):
        """タイマーを設定"""
        self.remaining_time = seconds
        self._update_display()
    
    def _set_custom_timer(self):
        """カスタムタイマーを設定"""
        try:
            hours = int(self.hours_entry.get() or 0)
            minutes = int(self.minutes_entry.get() or 0)
            seconds = int(self.seconds_entry.get() or 0)
            
            total_seconds = hours * 3600 + minutes * 60 + seconds
            
            if total_seconds > 0:
                self._set_timer(total_seconds)
            else:
                # エラーメッセージ
                self.time_label.configure(text="時間を入力")
        except ValueError:
            # 無効な入力
            self.time_label.configure(text="無効な入力")
    
    def _start_timer(self):
        """タイマーを開始"""
        if self.remaining_time <= 0:
            return
        
        self.is_running = True
        self.start_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")
        self._tick()
    
    def _stop_timer(self):
        """タイマーを停止"""
        self.is_running = False
        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
        if self.after_id:
            self.timer_window.after_cancel(self.after_id)
    
    def _reset_timer(self):
        """タイマーをリセット"""
        self._stop_timer()
        self.remaining_time = 0
        self._update_display()
    
    def _tick(self):
        """タイマーの1秒ごとの更新"""
        if not self.is_running:
            return
        
        self.remaining_time -= 1
        self._update_display()
        
        if self.remaining_time <= 0:
            self._timer_finished()
        else:
            self.after_id = self.timer_window.after(1000, self._tick)
    
    def _timer_finished(self):
        """タイマー終了"""
        self.is_running = False
        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
        self.time_label.configure(text="終了！", text_color="green")
    
    def _update_display(self):
        """表示を更新"""
        td = timedelta(seconds=self.remaining_time)
        hours = td.seconds // 3600
        minutes = (td.seconds % 3600) // 60
        seconds = td.seconds % 60
        self.time_label.configure(
            text=f"{hours:02d}:{minutes:02d}:{seconds:02d}",
            text_color="white",
        )
    
    def shutdown(self):
        """終了処理"""
        self._stop_timer()
        if self.timer_window and self.timer_window.winfo_exists():
            self.timer_window.destroy()


# プラグインクラスをエクスポート
Plugin = TimerPlugin

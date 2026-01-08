"""
ポモドーロタイマープラグイン
"""

from horloq.plugins.base import PluginBase
import customtkinter as ctk
import time
from datetime import datetime, timedelta


class PomodoroPlugin(PluginBase):
    """ポモドーロタイマープラグイン"""
    
    def __init__(self, app_context):
        super().__init__(
            name="pomodoro",
            version="1.0.0",
            author="Nyayuta1060",
            description="ポモドーロテクニックで生産性向上",
            app_context=app_context,
        )
        self.pomodoro_window = None
        self.is_running = False
        self.is_break = False
        self.remaining_time = 25 * 60  # 25分（秒単位）
        self.work_duration = 25 * 60
        self.short_break_duration = 5 * 60
        self.long_break_duration = 15 * 60
        self.completed_pomodoros = 0
        self.after_id = None
        
    def initialize(self) -> bool:
        """初期化"""
        return True
    
    def create_widget(self, parent):
        """ウィジェットを作成"""
        frame = ctk.CTkFrame(parent)
        
        button = ctk.CTkButton(
            frame,
            text="🍅 ポモドーロタイマーを開く",
            command=self._open_pomodoro_window,
        )
        button.pack(pady=10, padx=20)
        
        return frame
    
    def _open_pomodoro_window(self):
        """ポモドーロタイマーウィンドウを開く"""
        if self.pomodoro_window and self.pomodoro_window.winfo_exists():
            self.pomodoro_window.focus()
            return
        
        self.pomodoro_window = ctk.CTkToplevel()
        self.pomodoro_window.title("ポモドーロタイマー")
        self.pomodoro_window.geometry("450x600")
        
        # メインフレーム
        main_frame = ctk.CTkFrame(self.pomodoro_window)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # タイトル
        title_label = ctk.CTkLabel(
            main_frame,
            text="🍅 ポモドーロタイマー",
            font=("Arial", 24, "bold"),
        )
        title_label.pack(pady=10)
        
        # モード表示
        self.mode_label = ctk.CTkLabel(
            main_frame,
            text="作業時間",
            font=("Arial", 18, "bold"),
            text_color="#FF6B6B",
        )
        self.mode_label.pack(pady=5)
        
        # 時間表示
        self.time_label = ctk.CTkLabel(
            main_frame,
            text="25:00",
            font=("Arial", 72, "bold"),
        )
        self.time_label.pack(pady=30)
        
        # プログレスバー
        self.progress = ctk.CTkProgressBar(
            main_frame,
            width=350,
            height=20,
        )
        self.progress.pack(pady=20)
        self.progress.set(1.0)
        
        # コントロールボタン
        control_frame = ctk.CTkFrame(main_frame)
        control_frame.pack(pady=20)
        
        self.start_btn = ctk.CTkButton(
            control_frame,
            text="開始",
            command=self._start_timer,
            width=100,
            height=40,
            font=("Arial", 14),
        )
        self.start_btn.pack(side="left", padx=5)
        
        self.reset_btn = ctk.CTkButton(
            control_frame,
            text="リセット",
            command=self._reset_timer,
            width=100,
            height=40,
            font=("Arial", 14),
        )
        self.reset_btn.pack(side="left", padx=5)
        
        self.skip_btn = ctk.CTkButton(
            control_frame,
            text="スキップ",
            command=self._skip_timer,
            width=100,
            height=40,
            font=("Arial", 14),
        )
        self.skip_btn.pack(side="left", padx=5)
        
        # 統計表示
        stats_frame = ctk.CTkFrame(main_frame)
        stats_frame.pack(pady=20, fill="x")
        
        ctk.CTkLabel(
            stats_frame,
            text="完了したポモドーロ:",
            font=("Arial", 14),
        ).pack(pady=5)
        
        self.pomodoro_count_label = ctk.CTkLabel(
            stats_frame,
            text="🍅 × 0",
            font=("Arial", 24, "bold"),
        )
        self.pomodoro_count_label.pack(pady=5)
        
        # 設定
        settings_frame = ctk.CTkFrame(main_frame)
        settings_frame.pack(pady=10, fill="x")
        
        ctk.CTkLabel(
            settings_frame,
            text="設定",
            font=("Arial", 16, "bold"),
        ).pack(pady=5)
        
        # 作業時間設定
        work_frame = ctk.CTkFrame(settings_frame)
        work_frame.pack(pady=5, fill="x", padx=10)
        
        ctk.CTkLabel(
            work_frame,
            text="作業時間 (分):",
            font=("Arial", 12),
        ).pack(side="left", padx=5)
        
        self.work_entry = ctk.CTkEntry(
            work_frame,
            width=60,
            font=("Arial", 12),
        )
        self.work_entry.insert(0, "25")
        self.work_entry.pack(side="left", padx=5)
        
        # 短い休憩設定
        short_break_frame = ctk.CTkFrame(settings_frame)
        short_break_frame.pack(pady=5, fill="x", padx=10)
        
        ctk.CTkLabel(
            short_break_frame,
            text="短い休憩 (分):",
            font=("Arial", 12),
        ).pack(side="left", padx=5)
        
        self.short_break_entry = ctk.CTkEntry(
            short_break_frame,
            width=60,
            font=("Arial", 12),
        )
        self.short_break_entry.insert(0, "5")
        self.short_break_entry.pack(side="left", padx=5)
        
        # 長い休憩設定
        long_break_frame = ctk.CTkFrame(settings_frame)
        long_break_frame.pack(pady=5, fill="x", padx=10)
        
        ctk.CTkLabel(
            long_break_frame,
            text="長い休憩 (分):",
            font=("Arial", 12),
        ).pack(side="left", padx=5)
        
        self.long_break_entry = ctk.CTkEntry(
            long_break_frame,
            width=60,
            font=("Arial", 12),
        )
        self.long_break_entry.insert(0, "15")
        self.long_break_entry.pack(side="left", padx=5)
        
        # ウィンドウクローズ時のハンドラ
        self.pomodoro_window.protocol("WM_DELETE_WINDOW", self._on_window_close)
    
    def _start_timer(self):
        """タイマーを開始"""
        if not self.is_running:
            self.is_running = True
            self.start_btn.configure(text="一時停止")
            self._update_settings()
            self._run_timer()
        else:
            self.is_running = False
            self.start_btn.configure(text="再開")
            if self.after_id:
                self.pomodoro_window.after_cancel(self.after_id)
    
    def _run_timer(self):
        """タイマーを実行"""
        if not self.is_running:
            return
        
        if self.remaining_time > 0:
            self.remaining_time -= 1
            self._update_display()
            self.after_id = self.pomodoro_window.after(1000, self._run_timer)
        else:
            self._timer_complete()
    
    def _update_display(self):
        """表示を更新"""
        minutes = self.remaining_time // 60
        seconds = self.remaining_time % 60
        self.time_label.configure(text=f"{minutes:02d}:{seconds:02d}")
        
        # プログレスバーを更新
        if self.is_break:
            if self.completed_pomodoros % 4 == 0 and self.completed_pomodoros > 0:
                total = self.long_break_duration
            else:
                total = self.short_break_duration
        else:
            total = self.work_duration
        
        progress = self.remaining_time / total
        self.progress.set(progress)
    
    def _timer_complete(self):
        """タイマー完了時の処理"""
        self.is_running = False
        self.start_btn.configure(text="開始")
        
        if not self.is_break:
            # 作業時間終了 → 休憩へ
            self.completed_pomodoros += 1
            self.pomodoro_count_label.configure(text=f"🍅 × {self.completed_pomodoros}")
            
            if self.completed_pomodoros % 4 == 0:
                # 4ポモドーロ完了 → 長い休憩
                self.remaining_time = self.long_break_duration
                self.mode_label.configure(text="長い休憩", text_color="#4ECDC4")
            else:
                # 短い休憩
                self.remaining_time = self.short_break_duration
                self.mode_label.configure(text="短い休憩", text_color="#95E1D3")
            
            self.is_break = True
        else:
            # 休憩終了 → 作業へ
            self.remaining_time = self.work_duration
            self.mode_label.configure(text="作業時間", text_color="#FF6B6B")
            self.is_break = False
        
        self._update_display()
        
        # 通知（簡易版）
        if self.pomodoro_window and self.pomodoro_window.winfo_exists():
            self.pomodoro_window.bell()
    
    def _reset_timer(self):
        """タイマーをリセット"""
        self.is_running = False
        if self.after_id:
            self.pomodoro_window.after_cancel(self.after_id)
        
        self.start_btn.configure(text="開始")
        self._update_settings()
        
        if self.is_break:
            if self.completed_pomodoros % 4 == 0 and self.completed_pomodoros > 0:
                self.remaining_time = self.long_break_duration
            else:
                self.remaining_time = self.short_break_duration
        else:
            self.remaining_time = self.work_duration
        
        self._update_display()
    
    def _skip_timer(self):
        """タイマーをスキップ"""
        self.remaining_time = 0
        self._timer_complete()
    
    def _update_settings(self):
        """設定を更新"""
        try:
            self.work_duration = int(self.work_entry.get()) * 60
            self.short_break_duration = int(self.short_break_entry.get()) * 60
            self.long_break_duration = int(self.long_break_entry.get()) * 60
        except ValueError:
            pass
    
    def _on_window_close(self):
        """ウィンドウクローズ時の処理"""
        if self.after_id:
            self.pomodoro_window.after_cancel(self.after_id)
        if self.pomodoro_window:
            self.pomodoro_window.destroy()
            self.pomodoro_window = None
    
    def cleanup(self):
        """クリーンアップ"""
        if self.after_id:
            self.pomodoro_window.after_cancel(self.after_id)
        if self.pomodoro_window and self.pomodoro_window.winfo_exists():
            self.pomodoro_window.destroy()


def create_plugin(app_context):
    """プラグインインスタンスを作成"""
    return PomodoroPlugin(app_context)

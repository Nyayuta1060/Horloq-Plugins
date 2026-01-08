"""
ストップウォッチプラグイン
"""

from horloq.plugins.base import PluginBase
import customtkinter as ctk
import time


class StopwatchPlugin(PluginBase):
    """ストップウォッチプラグイン"""
    
    def __init__(self, app_context):
        super().__init__(
            name="stopwatch",
            version="1.0.0",
            author="Nyayuta1060",
            description="ストップウォッチ",
            app_context=app_context,
        )
        self.stopwatch_window = None
        self.start_time = 0
        self.elapsed_time = 0
        self.is_running = False
        self.after_id = None
        self.laps = []
    
    def initialize(self) -> bool:
        """初期化"""
        return True
    
    def create_widget(self, parent):
        """ウィジェットを作成"""
        frame = ctk.CTkFrame(parent)
        
        button = ctk.CTkButton(
            frame,
            text="⏲️ ストップウォッチを開く",
            command=self._open_stopwatch_window,
        )
        button.pack(pady=10, padx=20)
        
        return frame
    
    def _open_stopwatch_window(self):
        """ストップウォッチウィンドウを開く"""
        if self.stopwatch_window and self.stopwatch_window.winfo_exists():
            self.stopwatch_window.focus()
            return
        
        self.stopwatch_window = ctk.CTkToplevel()
        self.stopwatch_window.title("ストップウォッチ")
        self.stopwatch_window.geometry("350x500")
        self.stopwatch_window.attributes("-topmost", True)  # 最前面固定
        
        # 時間表示
        self.time_label = ctk.CTkLabel(
            self.stopwatch_window,
            text="00:00:00.00",
            font=("Arial", 42, "bold"),
        )
        self.time_label.pack(pady=30)
        
        # コントロールボタン
        control_frame = ctk.CTkFrame(self.stopwatch_window)
        control_frame.pack(pady=10)
        
        self.start_btn = ctk.CTkButton(
            control_frame,
            text="開始",
            command=self._start_stopwatch,
            width=80,
        )
        self.start_btn.pack(side="left", padx=5)
        
        self.lap_btn = ctk.CTkButton(
            control_frame,
            text="ラップ",
            command=self._record_lap,
            state="disabled",
            width=80,
        )
        self.lap_btn.pack(side="left", padx=5)
        
        self.reset_btn = ctk.CTkButton(
            control_frame,
            text="リセット",
            command=self._reset_stopwatch,
            width=80,
        )
        self.reset_btn.pack(side="left", padx=5)
        
        # ラップタイム表示
        lap_label = ctk.CTkLabel(
            self.stopwatch_window,
            text="ラップタイム",
            font=("Arial", 14, "bold"),
        )
        lap_label.pack(pady=(20, 10))
        
        self.lap_frame = ctk.CTkScrollableFrame(
            self.stopwatch_window,
            height=200,
        )
        self.lap_frame.pack(pady=5, padx=20, fill="both", expand=True)
    
    def _start_stopwatch(self):
        """ストップウォッチを開始/停止"""
        if not self.is_running:
            # 開始
            self.is_running = True
            self.start_time = time.time() - self.elapsed_time
            self.start_btn.configure(text="停止")
            self.lap_btn.configure(state="normal")
            self._update_time()
        else:
            # 停止
            self.is_running = False
            self.start_btn.configure(text="開始")
            self.lap_btn.configure(state="disabled")
            if self.after_id:
                self.stopwatch_window.after_cancel(self.after_id)
    
    def _record_lap(self):
        """ラップタイムを記録"""
        if not self.is_running:
            return
        
        lap_time = self.elapsed_time
        self.laps.append(lap_time)
        
        # ラップ表示を追加
        lap_num = len(self.laps)
        minutes = int(lap_time // 60)
        seconds = int(lap_time % 60)
        centiseconds = int((lap_time % 1) * 100)
        
        lap_text = f"Lap {lap_num}: {minutes:02d}:{seconds:02d}.{centiseconds:02d}"
        lap_label = ctk.CTkLabel(
            self.lap_frame,
            text=lap_text,
            font=("Arial", 12),
        )
        lap_label.pack(anchor="w", pady=2)
    
    def _reset_stopwatch(self):
        """ストップウォッチをリセット"""
        if self.is_running:
            self._start_stopwatch()  # 停止
        
        self.elapsed_time = 0
        self.laps = []
        self._update_display()
        
        # ラップ表示をクリア
        for widget in self.lap_frame.winfo_children():
            widget.destroy()
    
    def _update_time(self):
        """時間を更新"""
        if not self.is_running:
            return
        
        self.elapsed_time = time.time() - self.start_time
        self._update_display()
        self.after_id = self.stopwatch_window.after(10, self._update_time)
    
    def _update_display(self):
        """表示を更新"""
        minutes = int(self.elapsed_time // 60)
        seconds = int(self.elapsed_time % 60)
        centiseconds = int((self.elapsed_time % 1) * 100)
        
        self.time_label.configure(
            text=f"{minutes:02d}:{seconds:02d}.{centiseconds:02d}"
        )
    
    def shutdown(self):
        """終了処理"""
        if self.is_running:
            self._start_stopwatch()  # 停止
        if self.stopwatch_window and self.stopwatch_window.winfo_exists():
            self.stopwatch_window.destroy()


# プラグインクラスをエクスポート
Plugin = StopwatchPlugin

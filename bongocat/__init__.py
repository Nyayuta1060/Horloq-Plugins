"""
Bongo Cat タイピングアニメーションプラグイン
"""

from horloq.plugins.base import PluginBase
import customtkinter as ctk
import threading

# pynputのインポートを試みる
try:
    from pynput import keyboard, mouse
    PYNPUT_AVAILABLE = True
except ImportError:
    PYNPUT_AVAILABLE = False
    keyboard = None
    mouse = None


class BongoCatPlugin(PluginBase):
    """Bongo Cat タイピングアニメーションプラグイン"""
    
    def __init__(self, app_context):
        super().__init__(
            name="bongocat",
            version="1.0.0",
            author="Nyayuta1060",
            description="キー入力に反応する Bongo Cat アニメーション",
            app_context=app_context,
        )
        self.bongocat_window = None
        self.keyboard_listener = None
        self.mouse_listener = None
        self.is_typing = False
        self.is_clicking = False
        self.reset_timer = None
        
    def initialize(self) -> bool:
        """初期化"""
        return True
    
    def create_widget(self, parent):
        """ウィジェットを作成"""
        frame = ctk.CTkFrame(parent)
        
        button = ctk.CTkButton(
            frame,
            text="🐱 Bongo Cat を開く",
            command=self._open_bongocat_window,
        )
        button.pack(pady=10, padx=20)
        
        return frame
    
    def _open_bongocat_window(self):
        """Bongo Cat ウィンドウを開く"""
        if self.bongocat_window and self.bongocat_window.winfo_exists():
            self.bongocat_window.focus()
            return
        
        # pynputが利用できない場合のエラー表示
        if not PYNPUT_AVAILABLE:
            self._show_dependency_error()
            return
        
        self.bongocat_window = ctk.CTkToplevel()
        self.bongocat_window.title("Bongo Cat")
        self.bongocat_window.geometry("600x400")
        
        # メインフレーム
        main_frame = ctk.CTkFrame(self.bongocat_window)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # タイトル
        title_label = ctk.CTkLabel(
            main_frame,
            text="🐱 Bongo Cat",
            font=("Arial", 24, "bold"),
        )
        title_label.pack(pady=10)
        
        # 猫のアニメーション表示エリア
        self.cat_canvas = ctk.CTkCanvas(
            main_frame,
            width=400,
            height=200,
            bg="#2B2B2B",
            highlightthickness=0,
        )
        self.cat_canvas.pack(pady=20)
        
        # 初期状態の猫を描画
        self._draw_cat_idle()
        
        # ステータス表示
        self.status_label = ctk.CTkLabel(
            main_frame,
            text="待機中...",
            font=("Arial", 14),
        )
        self.status_label.pack(pady=10)
        
        # コントロールボタン
        control_frame = ctk.CTkFrame(main_frame)
        control_frame.pack(pady=10)
        
        self.toggle_btn = ctk.CTkButton(
            control_frame,
            text="監視開始",
            command=self._toggle_monitoring,
            width=120,
        )
        self.toggle_btn.pack(side="left", padx=5)
        
        # 設定
        settings_frame = ctk.CTkFrame(main_frame)
        settings_frame.pack(pady=10)
        
        ctk.CTkLabel(
            settings_frame,
            text="感度:",
            font=("Arial", 12),
        ).pack(side="left", padx=5)
        
        self.sensitivity_slider = ctk.CTkSlider(
            settings_frame,
            from_=50,
            to=500,
            number_of_steps=45,
            width=200,
        )
        self.sensitivity_slider.set(200)
        self.sensitivity_slider.pack(side="left", padx=5)
        
        # ウィンドウクローズ時のハンドラ
        self.bongocat_window.protocol("WM_DELETE_WINDOW", self._on_window_close)
    
    def _draw_cat_idle(self):
        """待機中の猫を描画"""
        self.cat_canvas.delete("all")
        
        # 猫の体（簡略化したASCIIアート風）
        self.cat_canvas.create_text(
            200, 100,
            text="　　　∧＿∧\n"
                 "　　（´・ω・）\n"
                 "　　/　　　 ヽ\n"
                 "　（|　　　　|）\n"
                 "　　し ーーJ",
            font=("Courier", 16),
            fill="#FFFFFF",
        )
    
    def _draw_cat_typing(self):
        """タイピング中の猫を描画"""
        self.cat_canvas.delete("all")
        
        self.cat_canvas.create_text(
            200, 100,
            text="　　　∧＿∧\n"
                 "　　（ `・ω・´）\n"
                 "　　/　つ⌒ヽ\n"
                 "　（|　　　　|）\n"
                 "　　し ーーJ",
            font=("Courier", 16),
            fill="#FFFF00",
        )
    
    def _draw_cat_clicking(self):
        """クリック中の猫を描画"""
        self.cat_canvas.delete("all")
        
        self.cat_canvas.create_text(
            200, 100,
            text="　　　∧＿∧\n"
                 "　　（ °ω°）\n"
                 "　　/　　 つ━━\n"
                 "　（|　　　　|）\n"
                 "　　し ーーJ",
            font=("Courier", 16),
            fill="#FF88FF",
        )
    
    def _toggle_monitoring(self):
        """監視のオン/オフを切り替え"""
        if self.keyboard_listener is None:
            self._start_monitoring()
            self.toggle_btn.configure(text="監視停止")
            self.status_label.configure(text="監視中...")
        else:
            self._stop_monitoring()
            self.toggle_btn.configure(text="監視開始")
            self.status_label.configure(text="待機中...")
            self._draw_cat_idle()
    
    def _start_monitoring(self):
        """キーボードとマウスの監視を開始"""
        # キーボードリスナー
        self.keyboard_listener = keyboard.Listener(
            on_press=self._on_key_press
        )
        self.keyboard_listener.start()
        
        # マウスリスナー
        self.mouse_listener = mouse.Listener(
            on_click=self._on_mouse_click
        )
        self.mouse_listener.start()
    
    def _stop_monitoring(self):
        """監視を停止"""
        if self.keyboard_listener:
            self.keyboard_listener.stop()
            self.keyboard_listener = None
        
        if self.mouse_listener:
            self.mouse_listener.stop()
            self.mouse_listener = None
        
        if self.reset_timer:
            self.reset_timer.cancel()
            self.reset_timer = None
    
    def _on_key_press(self, key):
        """キー押下時のハンドラ"""
        if self.bongocat_window and self.bongocat_window.winfo_exists():
            self.bongocat_window.after(0, self._show_typing)
    
    def _on_mouse_click(self, x, y, button, pressed):
        """マウスクリック時のハンドラ"""
        if pressed and self.bongocat_window and self.bongocat_window.winfo_exists():
            self.bongocat_window.after(0, self._show_clicking)
    
    def _show_typing(self):
        """タイピングアニメーションを表示"""
        self._draw_cat_typing()
        self.is_typing = True
        
        # リセットタイマーをキャンセル
        if self.reset_timer:
            self.reset_timer.cancel()
        
        # 一定時間後に待機状態に戻す
        sensitivity = self.sensitivity_slider.get() / 1000.0
        self.reset_timer = threading.Timer(sensitivity, self._reset_to_idle)
        self.reset_timer.start()
    
    def _show_clicking(self):
        """クリックアニメーションを表示"""
        self._draw_cat_clicking()
        self.is_clicking = True
        
        # リセットタイマーをキャンセル
        if self.reset_timer:
            self.reset_timer.cancel()
        
        # 一定時間後に待機状態に戻す
        sensitivity = self.sensitivity_slider.get() / 1000.0
        self.reset_timer = threading.Timer(sensitivity, self._reset_to_idle)
        self.reset_timer.start()
    
    def _reset_to_idle(self):
        """待機状態に戻す"""
        if self.bongocat_window and self.bongocat_window.winfo_exists():
            self.bongocat_window.after(0, self._draw_cat_idle)
            self.is_typing = False
            self.is_clicking = False
    
    def _on_window_close(self):
        """ウィンドウクローズ時の処理"""
        self._stop_monitoring()
        if self.bongocat_window:
            self.bongocat_window.destroy()
            self.bongocat_window = None
    
    def _show_dependency_error(self):
        """依存関係エラーを表示"""
        error_window = ctk.CTkToplevel()
        error_window.title("依存ライブラリが必要です")
        error_window.geometry("450x300")
        
        main_frame = ctk.CTkFrame(error_window)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(
            main_frame,
            text="⚠️ 依存ライブラリが見つかりません",
            font=("Arial", 18, "bold"),
            text_color="#FF6B6B",
        ).pack(pady=10)
        
        ctk.CTkLabel(
            main_frame,
            text="このプラグインには pynput ライブラリが必要です。",
            font=("Arial", 14),
        ).pack(pady=10)
        
        # インストール手順
        install_frame = ctk.CTkFrame(main_frame)
        install_frame.pack(pady=20, fill="x")
        
        ctk.CTkLabel(
            install_frame,
            text="インストール方法:",
            font=("Arial", 12, "bold"),
        ).pack(pady=5)
        
        ctk.CTkLabel(
            install_frame,
            text="pip install pynput",
            font=("Courier", 12),
            fg_color="#2B2B2B",
        ).pack(pady=5, padx=10, fill="x")
        
        ctk.CTkLabel(
            main_frame,
            text="インストール後、Horloqを再起動してください。",
            font=("Arial", 11),
            text_color="gray",
        ).pack(pady=10)
        
        ctk.CTkButton(
            main_frame,
            text="閉じる",
            command=error_window.destroy,
            width=100,
        ).pack(pady=10)
    
    def cleanup(self):
        """クリーンアップ"""
        self._stop_monitoring()
        if self.bongocat_window and self.bongocat_window.winfo_exists():
            self.bongocat_window.destroy()


def create_plugin(app_context):
    """プラグインインスタンスを作成"""
    return BongoCatPlugin(app_context)

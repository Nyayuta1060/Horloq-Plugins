"""
デスクトップペットプラグイン
"""

from horloq.plugins.base import PluginBase
import customtkinter as ctk
import random
from datetime import datetime


class DesktopPetPlugin(PluginBase):
    """デスクトップペットプラグイン"""
    
    # ペットの種類
    PETS = {
        "cat": {
            "name": "猫",
            "idle": "🐱",
            "happy": "😸",
            "sleep": "😴",
            "play": "😺",
        },
        "dog": {
            "name": "犬",
            "idle": "🐶",
            "happy": "😊",
            "sleep": "😴",
            "play": "🐕",
        },
        "rabbit": {
            "name": "うさぎ",
            "idle": "🐰",
            "happy": "😊",
            "sleep": "😴",
            "play": "🐇",
        },
        "bear": {
            "name": "くま",
            "idle": "🐻",
            "happy": "😊",
            "sleep": "😴",
            "play": "🧸",
        },
        "panda": {
            "name": "パンダ",
            "idle": "🐼",
            "happy": "😊",
            "sleep": "😴",
            "play": "🎋",
        },
    }
    
    # 行動
    ACTIONS = {
        "idle": ["待機中...", "ぼーっとしている", "あくびをした"],
        "happy": ["嬉しそう♪", "しっぽを振っている", "ご機嫌です"],
        "sleep": ["すやすや...", "夢を見ている", "お昼寝中"],
        "play": ["遊んでる！", "元気いっぱい", "はしゃいでいる"],
    }
    
    def __init__(self, app_context):
        super().__init__(
            name="pet",
            version="1.0.0",
            author="Nyayuta1060",
            description="時計画面に居座る可愛いデスクトップペット",
            app_context=app_context,
        )
        self.pet_window = None
        self.current_pet = "cat"
        self.current_action = "idle"
        self.happiness = 50
        self.energy = 100
        self.after_id = None
        self.last_interaction = datetime.now()
        
    def initialize(self) -> bool:
        """初期化"""
        return True
    
    def shutdown(self):
        """プラグインを終了"""
        if self.after_id and self.pet_window:
            self.pet_window.after_cancel(self.after_id)
        if self.pet_window and self.pet_window.winfo_exists():
            self.pet_window.destroy()
    
    def create_widget(self, parent):
        """ウィジェットを作成"""
        frame = ctk.CTkFrame(parent)
        
        button = ctk.CTkButton(
            frame,
            text="🐾 デスクトップペットを開く",
            command=self._open_pet_window,
        )
        button.pack(pady=10, padx=20)
        
        return frame
    
    def _open_pet_window(self):
        """ペットウィンドウを開く"""
        if self.pet_window and self.pet_window.winfo_exists():
            self.pet_window.focus()
            return
        
        self.pet_window = ctk.CTkToplevel()
        self.pet_window.title("デスクトップペット")
        self.pet_window.geometry("500x600")
        
        # メインフレーム
        main_frame = ctk.CTkFrame(self.pet_window)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # タイトル
        title_label = ctk.CTkLabel(
            main_frame,
            text="🐾 デスクトップペット",
            font=("Arial", 24, "bold"),
        )
        title_label.pack(pady=10)
        
        # ペット表示エリア
        pet_display_frame = ctk.CTkFrame(main_frame)
        pet_display_frame.pack(pady=20, fill="x")
        
        self.pet_icon_label = ctk.CTkLabel(
            pet_display_frame,
            text="🐱",
            font=("Arial", 100),
        )
        self.pet_icon_label.pack(pady=20)
        
        self.pet_action_label = ctk.CTkLabel(
            pet_display_frame,
            text="待機中...",
            font=("Arial", 16),
        )
        self.pet_action_label.pack(pady=5)
        
        # ステータスバー
        status_frame = ctk.CTkFrame(main_frame)
        status_frame.pack(pady=10, fill="x")
        
        # 幸福度
        happiness_frame = ctk.CTkFrame(status_frame)
        happiness_frame.pack(pady=5, fill="x", padx=10)
        
        ctk.CTkLabel(
            happiness_frame,
            text="❤️ 幸福度:",
            font=("Arial", 14),
        ).pack(side="left", padx=5)
        
        self.happiness_bar = ctk.CTkProgressBar(
            happiness_frame,
            width=300,
        )
        self.happiness_bar.pack(side="left", padx=5)
        self.happiness_bar.set(0.5)
        
        self.happiness_label = ctk.CTkLabel(
            happiness_frame,
            text="50%",
            font=("Arial", 14),
        )
        self.happiness_label.pack(side="left", padx=5)
        
        # エネルギー
        energy_frame = ctk.CTkFrame(status_frame)
        energy_frame.pack(pady=5, fill="x", padx=10)
        
        ctk.CTkLabel(
            energy_frame,
            text="⚡ エネルギー:",
            font=("Arial", 14),
        ).pack(side="left", padx=5)
        
        self.energy_bar = ctk.CTkProgressBar(
            energy_frame,
            width=300,
        )
        self.energy_bar.pack(side="left", padx=5)
        self.energy_bar.set(1.0)
        
        self.energy_label = ctk.CTkLabel(
            energy_frame,
            text="100%",
            font=("Arial", 14),
        )
        self.energy_label.pack(side="left", padx=5)
        
        # インタラクションボタン
        interaction_frame = ctk.CTkFrame(main_frame)
        interaction_frame.pack(pady=20)
        
        ctk.CTkButton(
            interaction_frame,
            text="🎾 遊ぶ",
            command=self._play_with_pet,
            width=100,
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            interaction_frame,
            text="🍖 餌をあげる",
            command=self._feed_pet,
            width=100,
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            interaction_frame,
            text="✋ なでる",
            command=self._pet_pet,
            width=100,
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            interaction_frame,
            text="🛌 寝かせる",
            command=self._sleep_pet,
            width=100,
        ).pack(side="left", padx=5)
        
        # ペット選択
        pet_selection_frame = ctk.CTkFrame(main_frame)
        pet_selection_frame.pack(pady=20, fill="x")
        
        ctk.CTkLabel(
            pet_selection_frame,
            text="ペットを選択:",
            font=("Arial", 14),
        ).pack(pady=5)
        
        pets_buttons_frame = ctk.CTkFrame(pet_selection_frame)
        pets_buttons_frame.pack(pady=5)
        
        for pet_id, pet_info in self.PETS.items():
            btn = ctk.CTkButton(
                pets_buttons_frame,
                text=f"{pet_info['idle']} {pet_info['name']}",
                command=lambda p=pet_id: self._change_pet(p),
                width=80,
            )
            btn.pack(side="left", padx=3)
        
        # 自動行動の開始
        self._start_auto_behavior()
        
        # ウィンドウクローズ時のハンドラ
        self.pet_window.protocol("WM_DELETE_WINDOW", self._on_window_close)
    
    def _change_pet(self, pet_id):
        """ペットを変更"""
        self.current_pet = pet_id
        self._update_pet_display()
    
    def _update_pet_display(self):
        """ペット表示を更新"""
        pet_info = self.PETS[self.current_pet]
        icon = pet_info[self.current_action]
        self.pet_icon_label.configure(text=icon)
        
        # 行動メッセージ
        action_messages = self.ACTIONS[self.current_action]
        message = random.choice(action_messages)
        self.pet_action_label.configure(text=message)
        
        # ステータスバー更新
        self.happiness_bar.set(self.happiness / 100)
        self.happiness_label.configure(text=f"{self.happiness}%")
        
        self.energy_bar.set(self.energy / 100)
        self.energy_label.configure(text=f"{self.energy}%")
    
    def _play_with_pet(self):
        """ペットと遊ぶ"""
        if self.energy >= 20:
            self.current_action = "play"
            self.happiness = min(100, self.happiness + 15)
            self.energy = max(0, self.energy - 20)
            self.last_interaction = datetime.now()
            self._update_pet_display()
            
            # 数秒後に待機状態に戻す
            self.pet_window.after(3000, self._return_to_idle)
    
    def _feed_pet(self):
        """餌をあげる"""
        self.current_action = "happy"
        self.happiness = min(100, self.happiness + 10)
        self.energy = min(100, self.energy + 30)
        self.last_interaction = datetime.now()
        self._update_pet_display()
        
        # 数秒後に待機状態に戻す
        self.pet_window.after(3000, self._return_to_idle)
    
    def _pet_pet(self):
        """なでる"""
        self.current_action = "happy"
        self.happiness = min(100, self.happiness + 20)
        self.last_interaction = datetime.now()
        self._update_pet_display()
        
        # 数秒後に待機状態に戻す
        self.pet_window.after(3000, self._return_to_idle)
    
    def _sleep_pet(self):
        """寝かせる"""
        self.current_action = "sleep"
        self.energy = min(100, self.energy + 5)
        self.last_interaction = datetime.now()
        self._update_pet_display()
    
    def _return_to_idle(self):
        """待機状態に戻す"""
        if self.current_action != "sleep":
            self.current_action = "idle"
            self._update_pet_display()
    
    def _start_auto_behavior(self):
        """自動行動を開始"""
        self._auto_behavior()
    
    def _auto_behavior(self):
        """自動行動"""
        if not self.pet_window or not self.pet_window.winfo_exists():
            return
        
        # 時間経過でステータス変化
        now = datetime.now()
        time_diff = (now - self.last_interaction).total_seconds()
        
        # 幸福度とエネルギーが徐々に減少
        if time_diff > 60:  # 1分以上放置
            self.happiness = max(0, self.happiness - 1)
            self.energy = max(0, self.energy - 1)
        
        # 夜は自動的に寝る
        hour = now.hour
        if 22 <= hour or hour < 6:
            if self.current_action != "sleep":
                self.current_action = "sleep"
                self._update_pet_display()
        elif self.current_action == "sleep" and self.energy > 80:
            self._return_to_idle()
        
        # ランダムな行動
        if random.random() < 0.1 and self.current_action == "idle":
            actions = ["happy", "play"]
            self.current_action = random.choice(actions)
            self._update_pet_display()
            self.pet_window.after(2000, self._return_to_idle)
        
        self._update_pet_display()
        
        # 10秒ごとに自動行動を実行
        self.after_id = self.pet_window.after(10000, self._auto_behavior)
    
    def _on_window_close(self):
        """ウィンドウクローズ時の処理"""
        if self.after_id:
            self.pet_window.after_cancel(self.after_id)
        if self.pet_window:
            self.pet_window.destroy()
            self.pet_window = None
    
    def cleanup(self):
        """クリーンアップ"""
        if self.after_id:
            self.pet_window.after_cancel(self.after_id)
        if self.pet_window and self.pet_window.winfo_exists():
            self.pet_window.destroy()


def create_plugin(app_context):
    """プラグインインスタンスを作成"""
    return DesktopPetPlugin(app_context)

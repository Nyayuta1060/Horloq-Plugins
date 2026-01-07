"""
Helloプラグイン - サンプルプラグイン
"""

from horloq.plugins.base import PluginBase
import customtkinter as ctk


class HelloPlugin(PluginBase):
    """シンプルなHello Worldプラグイン"""
    
    def __init__(self, app_context):
        super().__init__(
            name="hello",
            version="1.0.0",
            author="Nyayuta1060",
            description="シンプルなHello Worldプラグイン",
            app_context=app_context,
        )
    
    def initialize(self) -> bool:
        """初期化"""
        print("Hello plugin initialized!")
        return True
    
    def create_widget(self, parent):
        """ウィジェットを作成"""
        frame = ctk.CTkFrame(parent)
        
        label = ctk.CTkLabel(
            frame,
            text="👋 Hello, Horloq!",
            font=("Arial", 16),
        )
        label.pack(pady=10, padx=20)
        
        return frame
    
    def shutdown(self):
        """終了処理"""
        print("Hello plugin shutdown")


# プラグインクラスをエクスポート
Plugin = HelloPlugin

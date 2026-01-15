"""
天気予報プラグイン
"""

from horloq.plugins.base import PluginBase
import customtkinter as ctk
import json
from datetime import datetime

# requestsのインポートを試みる
try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    requests = None


class WeatherPlugin(PluginBase):
    """天気予報プラグイン"""
    
    # 天気アイコンマッピング
    WEATHER_ICONS = {
        "Clear": "☀️",
        "Clouds": "☁️",
        "Rain": "🌧️",
        "Drizzle": "🌦️",
        "Thunderstorm": "⛈️",
        "Snow": "🌨️",
        "Mist": "🌫️",
        "Smoke": "🌫️",
        "Haze": "🌫️",
        "Dust": "🌫️",
        "Fog": "🌫️",
        "Sand": "🌫️",
        "Ash": "🌫️",
        "Squall": "💨",
        "Tornado": "🌪️",
    }
    
    def __init__(self, app_context):
        super().__init__(app_context)
        self.weather_window = None
        # OpenWeatherMap API（無料版）
        # 注: 実際に使用する場合は、https://openweathermap.org/ でAPIキーを取得してください
        self.api_key = self.get_config("api_key", "")
        self.city = self.get_config("city", "Tokyo")
        self.weather_data = None
        
    def initialize(self) -> bool:
        """初期化"""
        return True
    
    def shutdown(self):
        """プラグインを終了"""
        if self.weather_window and self.weather_window.winfo_exists():
            self.weather_window.destroy()
    
    def create_widget(self, parent):
        """ウィジェットを作成"""
        frame = ctk.CTkFrame(parent)
        
        button = ctk.CTkButton(
            frame,
            text="☀️ 天気予報を開く",
            command=self._open_weather_window,
        )
        button.pack(pady=10, padx=20)
        
        return frame
    
    def _open_weather_window(self):
        """天気予報ウィンドウを開く"""
        if self.weather_window and self.weather_window.winfo_exists():
            self.weather_window.focus()
            return
        
        self.weather_window = ctk.CTkToplevel()
        self.weather_window.title("天気予報")
        self.weather_window.geometry("500x650")
        self.weather_window.attributes("-topmost", True)  # 最前面固定
        
        # メインフレーム
        main_frame = ctk.CTkFrame(self.weather_window)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # タイトル
        title_label = ctk.CTkLabel(
            main_frame,
            text="🌤️ 天気予報",
            font=("Arial", 24, "bold"),
        )
        title_label.pack(pady=10)
        
        # 都市選択
        city_frame = ctk.CTkFrame(main_frame)
        city_frame.pack(pady=10, fill="x")
        
        ctk.CTkLabel(
            city_frame,
            text="都市:",
            font=("Arial", 14),
        ).pack(side="left", padx=5)
        
        self.city_entry = ctk.CTkEntry(
            city_frame,
            width=200,
            font=("Arial", 14),
        )
        self.city_entry.insert(0, self.city)
        self.city_entry.pack(side="left", padx=5)
        
        fetch_btn = ctk.CTkButton(
            city_frame,
            text="取得",
            command=self._fetch_weather,
            width=80,
        )
        fetch_btn.pack(side="left", padx=5)
        
        # 現在の天気表示エリア
        self.current_weather_frame = ctk.CTkFrame(main_frame)
        self.current_weather_frame.pack(pady=20, fill="x")
        
        # 天気アイコン
        self.weather_icon_label = ctk.CTkLabel(
            self.current_weather_frame,
            text="☁️",
            font=("Arial", 72),
        )
        self.weather_icon_label.pack(pady=10)
        
        # 温度
        self.temp_label = ctk.CTkLabel(
            self.current_weather_frame,
            text="--°C",
            font=("Arial", 48, "bold"),
        )
        self.temp_label.pack(pady=5)
        
        # 天気説明
        self.description_label = ctk.CTkLabel(
            self.current_weather_frame,
            text="天気情報を取得してください",
            font=("Arial", 16),
        )
        self.description_label.pack(pady=5)
        
        # 詳細情報
        details_frame = ctk.CTkFrame(main_frame)
        details_frame.pack(pady=10, fill="x")
        
        # 湿度
        humidity_frame = ctk.CTkFrame(details_frame)
        humidity_frame.pack(side="left", expand=True, fill="both", padx=5)
        
        ctk.CTkLabel(
            humidity_frame,
            text="💧 湿度",
            font=("Arial", 12),
        ).pack(pady=5)
        
        self.humidity_label = ctk.CTkLabel(
            humidity_frame,
            text="---%",
            font=("Arial", 18, "bold"),
        )
        self.humidity_label.pack(pady=5)
        
        # 風速
        wind_frame = ctk.CTkFrame(details_frame)
        wind_frame.pack(side="left", expand=True, fill="both", padx=5)
        
        ctk.CTkLabel(
            wind_frame,
            text="💨 風速",
            font=("Arial", 12),
        ).pack(pady=5)
        
        self.wind_label = ctk.CTkLabel(
            wind_frame,
            text="-- m/s",
            font=("Arial", 18, "bold"),
        )
        self.wind_label.pack(pady=5)
        
        # 気圧
        pressure_frame = ctk.CTkFrame(details_frame)
        pressure_frame.pack(side="left", expand=True, fill="both", padx=5)
        
        ctk.CTkLabel(
            pressure_frame,
            text="🌡️ 気圧",
            font=("Arial", 12),
        ).pack(pady=5)
        
        self.pressure_label = ctk.CTkLabel(
            pressure_frame,
            text="-- hPa",
            font=("Arial", 18, "bold"),
        )
        self.pressure_label.pack(pady=5)
        
        # 体感温度と最高/最低気温
        temp_details_frame = ctk.CTkFrame(main_frame)
        temp_details_frame.pack(pady=10, fill="x")
        
        self.feels_like_label = ctk.CTkLabel(
            temp_details_frame,
            text="体感温度: --°C",
            font=("Arial", 14),
        )
        self.feels_like_label.pack(pady=5)
        
        self.temp_range_label = ctk.CTkLabel(
            temp_details_frame,
            text="最高: --°C / 最低: --°C",
            font=("Arial", 14),
        )
        self.temp_range_label.pack(pady=5)
        
        # 更新時刻
        self.update_time_label = ctk.CTkLabel(
            main_frame,
            text="",
            font=("Arial", 10),
            text_color="gray",
        )
        self.update_time_label.pack(pady=10)
        
        # APIキー設定
        api_frame = ctk.CTkFrame(main_frame)
        api_frame.pack(pady=10, fill="x")
        
        ctk.CTkLabel(
            api_frame,
            text="APIキー:",
            font=("Arial", 12),
        ).pack(side="left", padx=5)
        
        self.api_key_entry = ctk.CTkEntry(
            api_frame,
            width=300,
            font=("Arial", 12),
            show="*",
        )
        self.api_key_entry.insert(0, self.api_key)
        self.api_key_entry.pack(side="left", padx=5)
        
        # 保存ボタン
        save_btn = ctk.CTkButton(
            api_frame,
            text="保存",
            command=self._save_settings,
            width=60,
        )
        save_btn.pack(side="left", padx=5)
        
        # 注意書き
        note_label = ctk.CTkLabel(
            main_frame,
            text="※ OpenWeatherMap の無料APIキーが必要です",
            font=("Arial", 10),
            text_color="gray",
        )
        note_label.pack(pady=5)
        
        # デモモードボタン
        demo_btn = ctk.CTkButton(
            main_frame,
            text="📊 デモデータを表示",
            command=self._show_demo_data,
            width=200,
        )
        demo_btn.pack(pady=10)
    
    def _fetch_weather(self):
        """天気情報を取得"""
        # requestsが利用できない場合のエラー表示
        if not REQUESTS_AVAILABLE:
            self.description_label.configure(
                text="エラー: requests ライブラリが必要です\n\n"
                     "インストール方法:\n"
                     "pip install requests\n\n"
                     "（デモデータは表示できます）"
            )
            return
        
        city = self.city_entry.get().strip()
        api_key = self.api_key_entry.get().strip()
        
        # 設定を保存（取得前に保存することで次回以降も使える）
        self.api_key = api_key
        self.city = city
        self.set_config("api_key", self.api_key)
        self.set_config("city", self.city)
        
        if not api_key:
            self.description_label.configure(
                text="APIキーを設定してください\n（またはデモデータを表示）"
            )
            return
        
        if not city:
            self.description_label.configure(
                text="都市名を入力してください"
            )
            return
        
        try:
            # OpenWeatherMap API呼び出し
            url = f"https://api.openweathermap.org/data/2.5/weather"
            params = {
                "q": city,
                "appid": api_key,
                "units": "metric",  # 摂氏
                "lang": "ja",
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            # エラーレスポンスの詳細表示
            if response.status_code == 401:
                self.description_label.configure(
                    text="エラー: APIキーが無効です\n"
                         "OpenWeatherMapでAPIキーを確認してください\n"
                         "https://openweathermap.org/api"
                )
                return
            elif response.status_code == 404:
                self.description_label.configure(
                    text=f"エラー: 都市 '{city}' が見つかりません\n"
                         "都市名を英語で入力してください"
                )
                return
            
            response.raise_for_status()
            
            self.weather_data = response.json()
            self._update_weather_display()
            
        except requests.exceptions.RequestException as e:
            error_msg = str(e)
            if "401" in error_msg:
                self.description_label.configure(
                    text="エラー: APIキーが無効です\n正しいAPIキーを入力してください"
                )
            else:
                self.description_label.configure(
                    text=f"エラー: {error_msg}\n（デモデータを表示することもできます）"
                )
    
    def _show_demo_data(self):
        """デモデータを表示"""
        # サンプルデータ
        self.weather_data = {
            "weather": [
                {
                    "main": "Clear",
                    "description": "快晴",
                }
            ],
            "main": {
                "temp": 22.5,
                "feels_like": 21.8,
                "temp_min": 20.0,
                "temp_max": 25.0,
                "pressure": 1013,
                "humidity": 60,
            },
            "wind": {
                "speed": 3.5,
            },
            "name": "Tokyo",
        }
        self._update_weather_display()
    
    def _update_weather_display(self):
        """天気表示を更新"""
        if not self.weather_data:
            return
        
        # 天気アイコン
        weather_main = self.weather_data["weather"][0]["main"]
        icon = self.WEATHER_ICONS.get(weather_main, "🌤️")
        self.weather_icon_label.configure(text=icon)
        
        # 温度
        temp = self.weather_data["main"]["temp"]
        self.temp_label.configure(text=f"{temp:.1f}°C")
        
        # 説明
        description = self.weather_data["weather"][0]["description"]
        city_name = self.weather_data.get("name", self.city_entry.get())
        self.description_label.configure(text=f"{city_name} - {description}")
        
        # 湿度
        humidity = self.weather_data["main"]["humidity"]
        self.humidity_label.configure(text=f"{humidity}%")
        
        # 風速
        wind_speed = self.weather_data["wind"]["speed"]
        self.wind_label.configure(text=f"{wind_speed:.1f} m/s")
        
        # 気圧
        pressure = self.weather_data["main"]["pressure"]
        self.pressure_label.configure(text=f"{pressure} hPa")
        
        # 体感温度
        feels_like = self.weather_data["main"]["feels_like"]
        self.feels_like_label.configure(text=f"体感温度: {feels_like:.1f}°C")
        
        # 最高/最低気温
        temp_min = self.weather_data["main"]["temp_min"]
        temp_max = self.weather_data["main"]["temp_max"]
        self.temp_range_label.configure(
            text=f"最高: {temp_max:.1f}°C / 最低: {temp_min:.1f}°C"
        )
        
        # 更新時刻
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.update_time_label.configure(text=f"最終更新: {now}")
    
    def _save_settings(self):
        """設定を保存"""
        self.api_key = self.api_key_entry.get()
        self.city = self.city_entry.get()
        
        # 設定を永続化
        self.set_config("api_key", self.api_key)
        self.set_config("city", self.city)
        
        # 保存完了メッセージ（簡易版）
        if self.weather_window and self.weather_window.winfo_exists():
            # 一時的にメッセージを表示
            original_text = self.description_label.cget("text")
            self.description_label.configure(text="設定を保存しました！")
            self.weather_window.after(2000, lambda: self.description_label.configure(text=original_text))
    
    def cleanup(self):
        """クリーンアップ"""
        if self.weather_window and self.weather_window.winfo_exists():
            self.weather_window.destroy()


def create_plugin(app_context):
    """プラグインインスタンスを作成"""
    return WeatherPlugin(app_context)

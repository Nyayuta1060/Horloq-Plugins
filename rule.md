# Horloq プラグイン開発ルール

## 🌿 開発フロー

- プラグインそれぞれにブランチを立てる
- ブランチ名: `plugin/<plugin-name>` (例: `plugin/weather`, `plugin/bongocat`)
- 完成後、mainブランチにマージ(ただしPullRequestを出すこと)

## 📋 必須要件

### 1. ファイル構造

各プラグインは以下のファイルを含む必要があります：

```
plugin-name/
├── plugin.yaml       # 必須: プラグインメタデータ
├── __init__.py       # 必須: プラグイン実装
└── requirements.txt  # 任意: 外部依存関係
```

### 2. plugin.yaml の必須フィールド

```yaml
name: plugin-name          # プラグイン識別子（小文字、ハイフン区切り）
version: 1.0.0            # セマンティックバージョニング
author: Your Name         # 作者名
description: 説明文       # 簡潔な説明（50文字以内推奨）
min_horloq_version: 0.1.0 # 最小対応バージョン
```

### 3. プラグインクラスの実装

すべてのプラグインは `PluginBase` を継承し、以下の抽象メソッドを実装する必要があります：

```python
from horloq.plugins.base import PluginBase
import customtkinter as ctk

class YourPlugin(PluginBase):
    def __init__(self, app_context):
        # plugin.yamlから自動的にメタデータを読み込みます
        # name, version, author, description の指定は不要です
        super().__init__(app_context)
    
    def initialize(self) -> bool:
        """
        プラグイン初期化
        Returns: 成功時True、失敗時False
        """
        return True
    
    def shutdown(self):
        """
        プラグイン終了時のクリーンアップ
        - リソースの解放
        - ウィンドウの破棄
        - タイマーのキャンセル
        """
        pass
    
    def create_widget(self, parent):
        """
        メインウィンドウに表示するウィジェットを作成
        Returns: CTkFrame または None
        """
        frame = ctk.CTkFrame(parent)
        # ウィジェットの実装
        return frame

# プラグインクラスをエクスポート（必須）
Plugin = YourPlugin
```

**⚠️ 重要な変更点**:
- `__init__`では`super().__init__(app_context)`のみ呼び出す
- `name`、`version`、`author`、`description`は**plugin.yamlから自動読み込み**
- Pythonコード内でのメタデータのハードコーディングは不要
- `plugin.yaml`が唯一の情報源（Single Source of Truth）

## 🎨 UI/UXガイドライン

### ウィンドウの作成

```python
def _open_window(self):
    """プラグイン専用ウィンドウを開く"""
    # 既存ウィンドウのチェック
    if self.window and self.window.winfo_exists():
        self.window.focus()
        return
    
    self.window = ctk.CTkToplevel()
    self.window.title("プラグイン名")
    self.window.geometry("600x400")
    
    # 最前面固定（全プラグインで推奨）
    self.window.attributes("-topmost", True)
    
    # クローズハンドラの設定
    self.window.protocol("WM_DELETE_WINDOW", self._on_window_close)
```

### 推奨サイズとレイアウト

- **小さいウィンドウ**: 400x300 〜 600x400
- **中くらいのウィンドウ**: 600x400 〜 800x600
- **大きいウィンドウ**: 800x600 〜 1000x800
- **パディング**: pady=10, padx=20 を標準とする
- **フォント**: ("Arial", サイズ) を使用

### カラースキーム

customtkinterのテーマに従い、カスタムカラーは控えめに使用：

```python
# 推奨カラー
text_color="#FF6B6B"  # エラー・警告
text_color="#4ECDC4"  # 成功・情報
text_color="gray"     # 補足情報
```

## 🔌 依存関係の管理

### requirements.txt の作成

外部ライブラリが必要な場合、`requirements.txt` を作成：

```txt
# バージョン指定推奨
pynput>=1.7.6
requests>=2.31.0
```

### フォールバック処理の実装

依存ライブラリが見つからない場合の処理を実装：

```python
try:
    import some_library
    LIBRARY_AVAILABLE = True
except ImportError:
    LIBRARY_AVAILABLE = False
    some_library = None

class YourPlugin(PluginBase):
    def _open_window(self):
        if not LIBRARY_AVAILABLE:
            self._show_dependency_error()
            return
        # 通常の処理

    def _show_dependency_error(self):
        """依存関係エラーの表示"""
        error_window = ctk.CTkToplevel()
        error_window.title("依存ライブラリが必要です")
        error_window.geometry("450x300")
        
        # エラーメッセージとインストール手順を表示
```

## 💾 設定の保存と読み込み

プラグイン設定の永続化には `get_config` と `set_config` を使用：

```python
def __init__(self, app_context):
    super().__init__(...)
    
    # 設定の読み込み
    self.api_key = self.get_config("api_key", "")
    self.user_name = self.get_config("user_name", "Default")

def _save_settings(self):
    """設定を保存"""
    # 設定の保存
    self.set_config("api_key", self.api_key_entry.get())
    self.set_config("user_name", self.user_name_entry.get())
```

## 🎯 パフォーマンスとリソース管理

### タイマーとスケジューリング

```python
# Tkinterのafterを使用（推奨）
self.window.after(1000, self._update)  # 1秒後

# threading.Timerは避ける（GUIスレッドの問題が発生しやすい）
```

### クリーンアップの徹底

```python
def shutdown(self):
    """必ずリソースを解放"""
    # タイマーのキャンセル
    if self.after_id:
        self.window.after_cancel(self.after_id)
    
    # リスナーの停止
    if self.listener:
        self.listener.stop()
    
    # ウィンドウの破棄
    if self.window and self.window.winfo_exists():
        self.window.destroy()
```

## 🔒 セキュリティ

### APIキーの扱い

- APIキーは `set_config()` で保存
- UIでは `show="*"` で隠す
- デフォルト値に実際のキーを含めない

```python
# 良い例
self.api_key = self.get_config("api_key", "")

# 悪い例
self.api_key = "YOUR_ACTUAL_API_KEY_HERE"
```

## 🐛 エラーハンドリング

### 例外処理

```python
def _fetch_data(self):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        self._show_error("タイムアウトしました")
    except requests.exceptions.RequestException as e:
        self._show_error(f"エラー: {str(e)}")
    except Exception as e:
        self._show_error(f"予期しないエラー: {str(e)}")
```

### ユーザーフレンドリーなエラーメッセージ

- 技術的な詳細は最小限に
- 解決方法を提示
- デモモードや代替機能の提供を検討

## 📝 コーディングスタイル

### 命名規則

- **クラス名**: PascalCase (`MyPlugin`)
- **関数/メソッド名**: snake_case (`_open_window`)
- **定数**: UPPER_SNAKE_CASE (`API_KEY`)
- **プライベートメソッド**: アンダースコア接頭辞 (`_internal_method`)

### Docstring

```python
def method_name(self, param: str) -> bool:
    """
    メソッドの説明
    
    Args:
        param: パラメータの説明
    
    Returns:
        戻り値の説明
    """
    pass
```

## 🧪 テストとデバッグ

### デモモード

実際のAPIや外部リソースなしでテストできるデモモードを推奨：

```python
def _show_demo_data(self):
    """デモデータで動作確認"""
    self.data = {
        "sample": "data"
    }
    self._update_display()
```

### ログ出力

```python
# デバッグ時のみ
if __debug__:
    print(f"[{self.name}] Debug message")
```

## 🚀 公開前チェックリスト

- [ ] `plugin.yaml` にすべての必須フィールドがある
- [ ] `initialize()` と `shutdown()` が実装されている
- [ ] `create_plugin()` 関数が存在する
- [ ] 外部依存がある場合、`requirements.txt` がある
- [ ] 依存ライブラリのフォールバック処理がある
- [ ] リソースのクリーンアップが適切に行われる
- [ ] エラーメッセージがユーザーフレンドリー
- [ ] ウィンドウの重複チェックがある
- [ ] 設定が適切に保存/読み込みされる
- [ ] コードにハードコードされた秘密情報がない


## 📚 参考実装

公式プラグイン集の以下のプラグインが参考になります：

- **hello**: 最小限の実装例
- **timer**: 基本的なタイマー実装
- **stopwatch**: ラップ機能とリスト表示
- **bongocat**: 外部ライブラリ使用とフォールバック処理
- **pomodoro**: 複雑な状態管理とUI
- **weather**: API連携と設定保存

## 🔗 関連リンク

- [Horloq 本体](https://github.com/Nyayuta1060/Horloq)
- [プラグイン開発ガイド](https://github.com/Nyayuta1060/Horloq/blob/main/docs/PLUGIN_DEVELOPMENT.md)
- [公式プラグイン集](https://github.com/Nyayuta1060/Horloq-Plugins)

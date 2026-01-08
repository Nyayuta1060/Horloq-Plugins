# Horloq 公式プラグイン集

Horloq用の公式プラグイン集です。このリポジトリはモノレポ形式で複数のプラグインを管理しています。

## 📦 プラグイン一覧

| プラグイン      | 説明                                         | バージョン | 依存関係 |
| --------------- | -------------------------------------------- | ---------- | -------- |
| 👋 **Hello**     | シンプルなHello Worldプラグイン              | 1.0.0      | なし     |
| ⏱️ **Timer**     | カウントダウンタイマー（プリセット機能付き） | 1.0.0      | なし     |
| ⏲️ **Stopwatch** | 精密時間計測（ラップタイム機能付き）         | 1.0.0      | なし     |
| 🐱 **Bongo Cat** | キー入力に反応するアニメーション             | 1.0.0      | pynput   |
| 🍅 **Pomodoro**  | ポモドーロテクニックで生産性向上             | 1.0.0      | なし     |
| ☀️ **Weather**   | リアルタイム天気予報表示                     | 1.0.0      | requests |
| 🐾 **Pet**       | 時計画面に居座る可愛いデスクトップペット     | 1.0.0      | なし     |

## 🚀 インストール方法

### GUIから（推奨）

1. Horloqを起動
2. 右クリックメニューから「プラグイン管理」を選択
3. 「カタログから選択」ボタンをクリック
4. `Nyayuta1060/Horloq-Plugins`を入力
5. プラグイン一覧から必要なものを選択してインストール

### CLIから

```bash
# Hello プラグインをインストール
python -m horloq plugin install Nyayuta1060/Horloq-Plugins:hello

# Timer プラグインをインストール
python -m horloq plugin install Nyayuta1060/Horloq-Plugins:timer

# Stopwatch プラグインをインストール
python -m horloq plugin install Nyayuta1060/Horloq-Plugins:stopwatch

# Bongo Cat プラグインをインストール
python -m horloq plugin install Nyayuta1060/Horloq-Plugins:bongocat

# Pomodoro プラグインをインストール
python -m horloq plugin install Nyayuta1060/Horloq-Plugins:pomodoro

# Weather プラグインをインストール
python -m horloq plugin install Nyayuta1060/Horloq-Plugins:weather

# Pet プラグインをインストール
python -m horloq plugin install Nyayuta1060/Horloq-Plugins:pet

# アンインストール
python -m horloq plugin uninstall hello

# インストール済みプラグイン一覧
python -m horloq plugin list
```

> **📦 依存関係について**
> 
> 一部のプラグイン（Bongo Cat、Weather）は外部ライブラリが必要です。
> プラグインをインストールすると、必要なライブラリが自動的にインストールされます。
> 
> **バイナリ版の場合**: 
> - 依存関係は自動的にインストールされます
> - インストールに失敗した場合、プラグインは制限付きで利用可能です
> - エラーメッセージに従って手動でインストールすることもできます
> 
> **Python版の場合**:
> - `pip install pynput requests` で一括インストール可能
> - または各プラグインのインストール時に自動インストール

## 📝 プラグイン詳細

### Hello

シンプルなHello Worldプラグイン。プラグイン開発の参考用サンプルです。

**機能:**
- メインウィンドウに"Hello, Horloq!"メッセージを表示

### Timer

カウントダウンタイマープラグイン。

**機能:**
- 1分、3分、5分、10分のプリセットタイマー
- カスタム時間設定
- 開始/停止/リセット機能
- タイマー終了時の通知

### Stopwatch

高精度ストップウォッチプラグイン。

**機能:**
- 1/100秒単位の時間計測
- ラップタイム記録
- 開始/停止/リセット機能
- ラップタイム一覧表示

### Bongo Cat

キーボード入力やマウスクリックに反応するBongo Catアニメーションプラグイン。

**機能:**
- キーボード入力検知でタイピングアニメーション
- マウスクリック検知でクリックアニメーション
- アニメーション感度調整スライダー
- 監視のオン/オフ切り替え    # プラグインカタログ
├── hello/
│   ├── plugin.yaml
│   └── __init__.py
├── timer/
│   ├── plugin.yaml
│   └── __init__.py
├── stopwatch/
│   ├── plugin.yaml
│   └── __init__.py
├── bongocat/
│   ├── plugin.yaml
│   ├── __init__.py
│   └── requirements.txt   # 依存ライブラリ
├── pomodoro/
│   ├── plugin.yaml
│   └── __init__.py
├── weather/
│   ├── plugin.yaml
│   ├── __init__.py
│   └── requirements.txt   # 依存ライブラリ
└── pet/
    ├── plugin.yaml
    └── __init__.py
```

### 新しいプラグインの追加

1. 新しいディレクトリを作成
2. `plugin.yaml`と`__init__.py`を作成
3. 外部ライブラリが必要な場合は`requirements.txt`を作成
4. `plugins.yaml`にエントリを追加

### 依存関係の管理

プラグインが外部ライブラリを必要とする場合、プラグインディレクトリ内に `requirements.txt` を配置してください。ユーザーがプラグインをインストールする際に、自動的に依存関係がインストールされます。

**requirements.txtの例:**
```
pynput>=1.7.6
requests>=2.31.0
```
OpenWeatherMap APIを使用したリアルタイム天気予報表示プラグイン。

**機能:**
- 現在の気温、湿度、風速、気圧表示
- 体感温度と最高/最低気温
- 天気アイコン表示
- 都市選択機能
- デモモード搭載（APIキーなしでも動作確認可能）

**依存関係:** requests

**注意:** 実際の天気データを取得するには、[OpenWeatherMap](https://openweathermap.org/)で無料のAPIキーを取得する必要があります。

### Pet

時計画面に居座る可愛いデスクトップペットプラグイン。

**機能:**
- 5種類のペット選択（猫、犬、うさぎ、くま、パンダ）
- 幸福度とエネルギーのステータス管理
- インタラクション（遊ぶ、餌をあげる、なでる、寝かせる）
- 時間帯による自動行動（夜は自動的に寝る）
- ランダムな自発的行動

## 🔧 開発者向け

このリポジトリはモノレポ形式でプラグインを管理しています。

### 構造

```
Horloq-Plugins/
├── plugins.yaml       # プラグインカタログ
├── hello/
│   ├── plugin.yaml
│   └── __init__.py
├── timer/
│   ├── plugin.yaml
│   └── __init__.py
└── stopwatch/
    ├── plugin.yaml
    └── __init__.py
```

### 新しいプラグインの追加

1. 新しいディレクトリを作成
2. `plugin.yaml`と`__init__.py`を作成
3. `plugins.yaml`にエントリを追加

詳細は [Horloq プラグイン開発ガイド](https://github.com/Nyayuta1060/Horloq/blob/main/docs/PLUGIN_DEVELOPMENT.md) を参照してください。

### 依存関係のベストプラクティス

プラグインで外部ライブラリを使用する場合：

1. **requirements.txtを作成**
   ```txt
   pynput>=1.7.6
   requests>=2.31.0
   ```

2. **フォールバック処理を実装**
   ```python
   try:
       import pynput
       PYNPUT_AVAILABLE = True
   except ImportError:
       PYNPUT_AVAILABLE = False
   
   # 使用前にチェック
   if not PYNPUT_AVAILABLE:
       # エラーメッセージを表示
       pass
   ```

3. **ユーザーフレンドリーなエラーメッセージ**
   - ライブラリが見つからない場合の明確な説明
   - インストール方法の提示
   - 可能であればデモモードや制限機能の提供

これにより：
- バイナリ版でも動的にライブラリをインストール可能
- インストール失敗時もプラグイン自体は利用可能
- 開発者の自由度を維持

## 📄 ライセンス

MIT License - 詳細は [LICENSE](LICENSE) ファイルを参照してください。

## 🤝 コントリビューション

プルリクエストを歓迎します！新しいプラグインの提案や既存プラグインの改善など、お気軽にご提案ください。

## 🔗 関連リンク

- [Horloq 本体](https://github.com/Nyayuta1060/Horloq)
- [プラグイン開発ガイド](https://github.com/Nyayuta1060/Horloq/blob/main/docs/PLUGIN_DEVELOPMENT.md)
- [サンプルプラグイン集](https://github.com/Nyayuta1060/Horloq/blob/main/docs/EXAMPLE_PLUGINS.md)

# Horloq 公式プラグイン集

Horloq用の公式プラグイン集です。このリポジトリはモノレポ形式で複数のプラグインを管理しています。

## 📦 プラグイン一覧

| プラグイン             | 説明                                         | バージョン |
| ---------------------- | -------------------------------------------- | ---------- |
| 👋 **Hello**            | シンプルなHello Worldプラグイン              | 1.0.0      |
| ⏱️ **Timer**            | カウントダウンタイマー（プリセット機能付き） | 1.0.0      |
| ⏲️ **Stopwatch**        | 精密時間計測（ラップタイム機能付き）         | 1.0.0      |

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

# アンインストール
python -m horloq plugin uninstall hello

# インストール済みプラグイン一覧
python -m horloq plugin list
```

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

## 📄 ライセンス

MIT License - 詳細は [LICENSE](LICENSE) ファイルを参照してください。

## 🤝 コントリビューション

プルリクエストを歓迎します！新しいプラグインの提案や既存プラグインの改善など、お気軽にご提案ください。

## 🔗 関連リンク

- [Horloq 本体](https://github.com/Nyayuta1060/Horloq)
- [プラグイン開発ガイド](https://github.com/Nyayuta1060/Horloq/blob/main/docs/PLUGIN_DEVELOPMENT.md)
- [サンプルプラグイン集](https://github.com/Nyayuta1060/Horloq/blob/main/docs/EXAMPLE_PLUGINS.md)

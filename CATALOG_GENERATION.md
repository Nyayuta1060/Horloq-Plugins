# プラグインカタログの自動生成について

## 概要

このリポジトリでは、プラグインのメタデータ管理を簡素化するため、`plugins.yaml`を自動生成する仕組みを導入しています。

## 問題点（変更前）

以前は、プラグイン情報が2箇所に分散していました：

1. **各プラグインの`plugin.yaml`** - 個別のメタデータ
2. **トップレベルの`plugins.yaml`** - プラグインカタログ

これにより、以下の問題がありました：
- バージョン番号の不整合
- 説明文の不一致
- 手動での二重管理が必要

## 解決策（変更後）

### Single Source of Truth

各プラグインディレクトリの`plugin.yaml`がメタデータの**唯一の情報源**となります。

```
bongocat/
├── plugin.yaml    ← ここだけ編集すればOK
├── __init__.py
└── requirements.txt
```

### 自動生成の仕組み

1. **`generate_catalog.py`スクリプト**
   - 全プラグインディレクトリをスキャン
   - 各`plugin.yaml`を読み込み
   - `plugins.yaml`を自動生成

2. **GitHub Actions**
   - `plugin.yaml`の変更を検知
   - 自動的に`generate_catalog.py`を実行
   - 生成された`plugins.yaml`をコミット＆プッシュ

## 使い方

### プラグイン情報の更新

1. プラグインディレクトリの`plugin.yaml`を編集
   ```yaml
   name: bongocat
   version: 1.0.2  # バージョンアップ
   author: Nyayuta1060
   description: キー入力に反応する Bongo Cat アニメーション
   min_horloq_version: 0.1.1
   ```

2. コミット＆プッシュ
   ```bash
   git add bongocat/plugin.yaml
   git commit -m "Bump bongocat version to 1.0.2"
   git push
   ```

3. GitHub Actionsが自動的に`plugins.yaml`を更新

### ローカルでの確認

プッシュ前に生成結果を確認したい場合：

```bash
python generate_catalog.py
```

### 新しいプラグインの追加

1. プラグインディレクトリを作成
2. `plugin.yaml`を作成
   ```yaml
   name: myPlugin
   version: 1.0.0
   author: YourName
   description: プラグインの説明
   min_horloq_version: 0.1.0
   ```
3. `__init__.py`を実装
4. 変更をコミット＆プッシュ
5. 自動的に`plugins.yaml`に追加されます

## 注意事項

### ⚠️ `plugins.yaml`を直接編集しないでください

`plugins.yaml`は自動生成ファイルです。このファイルへの変更は、次回の自動生成時に上書きされます。

プラグイン情報を更新する場合は、必ず各プラグインの`plugin.yaml`を編集してください。

### plugin.yamlの必須フィールド

以下のフィールドは必須です：

- `name`: プラグイン名
- `version`: バージョン番号（SemVer推奨）
- `author`: 作者名
- `description`: プラグインの説明

オプションフィールド：
- `min_horloq_version`: 最小必要Horloqバージョン

## メリット

✅ **情報の一元管理** - `plugin.yaml`だけ編集すればOK
✅ **不整合の防止** - 自動生成により常に一致
✅ **開発効率の向上** - 手動での二重管理が不要
✅ **エラーの削減** - 人的ミスを防止
✅ **CI/CDとの統合** - 自動化により作業負担を軽減

## トラブルシューティング

### 生成されたカタログにプラグインが表示されない

1. `plugin.yaml`が正しい場所にあるか確認
2. 必須フィールド（name, version, author, description）が全て入っているか確認
3. YAMLの構文エラーがないか確認

### GitHub Actionsが実行されない

1. `.github/workflows/generate-catalog.yml`が存在するか確認
2. GitHubのActions設定が有効になっているか確認
3. プッシュしたコミットに`**/plugin.yaml`の変更が含まれているか確認

## 関連ファイル

- `generate_catalog.py` - カタログ生成スクリプト
- `.github/workflows/generate-catalog.yml` - GitHub Actionsワークフロー
- `plugins.yaml` - 自動生成されるプラグインカタログ
- `*/plugin.yaml` - 各プラグインのメタデータ（編集対象）

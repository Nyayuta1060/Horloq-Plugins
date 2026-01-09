#!/usr/bin/env python3
"""
プラグインカタログ自動生成スクリプト

各プラグインディレクトリのplugin.yamlを読み込んで、
トップレベルのplugins.yamlを自動生成します。
"""

import yaml
from pathlib import Path


def generate_catalog():
    """plugin.yamlからplugins.yamlを生成"""
    
    # リポジトリのルートディレクトリ
    root_dir = Path(__file__).parent
    
    # プラグイン情報を収集
    plugins = []
    
    # すべてのディレクトリをスキャン
    for item in root_dir.iterdir():
        if not item.is_dir():
            continue
        
        # 特殊なディレクトリをスキップ
        if item.name.startswith('.') or item.name in ['__pycache__', 'venv', 'env']:
            continue
        
        # plugin.yamlを探す
        plugin_yaml = item / 'plugin.yaml'
        if not plugin_yaml.exists():
            continue
        
        # plugin.yamlを読み込む
        try:
            with open(plugin_yaml, 'r', encoding='utf-8') as f:
                metadata = yaml.safe_load(f)
            
            # 必須フィールドをチェック
            if not all(key in metadata for key in ['name', 'version', 'author', 'description']):
                print(f"警告: {item.name}/plugin.yaml に必須フィールドが不足しています")
                continue
            
            # カタログエントリを作成
            plugin_entry = {
                'name': metadata['name'],
                'path': item.name,  # ディレクトリ名
                'description': metadata['description'],
                'version': metadata['version'],
                'author': metadata['author']
            }
            
            plugins.append(plugin_entry)
            print(f"✓ {metadata['name']} (v{metadata['version']})")
        
        except Exception as e:
            print(f"エラー: {item.name}/plugin.yaml の読み込みに失敗: {e}")
            continue
    
    # plugins.yamlを生成
    catalog = {
        'repository': 'Nyayuta1060/Horloq-Plugins',
        'plugins': sorted(plugins, key=lambda x: x['name'])
    }
    
    catalog_path = root_dir / 'plugins.yaml'
    with open(catalog_path, 'w', encoding='utf-8') as f:
        # ヘッダーコメントを追加
        f.write('# このファイルは自動生成されます - 直接編集しないでください\n')
        f.write('# プラグイン情報を更新する場合は、各プラグインディレクトリのplugin.yamlを編集してください\n')
        f.write('# 生成コマンド: python generate_catalog.py\n\n')
        yaml.dump(catalog, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
    
    print(f"\n✅ plugins.yaml を生成しました ({len(plugins)} 個のプラグイン)")
    return len(plugins)


if __name__ == '__main__':
    generate_catalog()

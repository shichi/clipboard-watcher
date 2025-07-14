# クリップボード監視ツール

クリップボードの変更を監視し、内容を自動的に連番のHTMLファイルに保存するPythonユーティリティです。

## 機能

- **リアルタイムクリップボード監視**: 0.5秒間隔でクリップボードの変更を監視
- **自動HTML出力**: クリップボードの内容をスタイル付きHTMLファイルに保存
- **連番ファイル命名**: `01.html`、`02.html`、`03.html`等として順次作成
- **クリップボードクリア**: 起動時にクリップボードをクリアし、既存内容の取得を回避
- **クロスプラットフォーム対応**: Linux/WSL環境で動作
- **スタイル付きHTML出力**: 生成されるHTMLファイルにタイムスタンプと整ったフォーマットを含む

## 必要要件

- Python 3.x
- `xclip` または `xsel` (Linux/WSLでのクリップボードアクセス用)

## インストール

1. このリポジトリをクローン:
```bash
git clone https://github.com/your-username/clipboard-watcher.git
cd clipboard-watcher
```

2. 必要なシステム依存関係をインストール:
```bash
# Ubuntu/Debian
sudo apt-get install xclip

# 代替: xsel
sudo apt-get install xsel
```

## 使用方法

クリップボード監視を開始:
```bash
python3 clipboard_watcher.py
```

プログラムは以下の動作を行います:
1. 現在のクリップボード内容をクリア
2. 新しいクリップボード変更の監視を開始
3. 各新しいクリップボード内容を連番HTMLファイルに保存
4. ターミナルにステータスメッセージを表示

プログラムを停止するには、`Ctrl+C`を押してください。

## 出力形式

各HTMLファイルには以下が含まれます:
- 清潔でレスポンシブなレイアウト
- 内容が取得された時刻のタイムスタンプ
- 適切にエスケープされたHTMLコンテンツ
- 読みやすさを重視したプロフェッショナルなスタイリング

出力ファイルの例 (`01.html`):
```html
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>Clipboard Content - 01.html</title>
    <!-- スタイル付きCSS含む -->
</head>
<body>
    <h1>Clipboard Content</h1>
    <div class="timestamp">Created: 2025-07-14 10:30:45</div>
    <div class="content">あなたのクリップボード内容がここに...</div>
</body>
</html>
```

## 動作原理

1. **起動**: 既存のクリップボード内容をクリアし、新しいコピーのみが取得されることを保証
2. **監視**: 0.5秒毎にクリップボード内容を継続的にチェック
3. **変更検出**: 現在のクリップボードと前回の状態を比較
4. **ファイル作成**: 変更が検出された時、インクリメントされた番号で新しいHTMLファイルを作成
5. **内容処理**: HTML特殊文字をエスケープし、フォーマットを適用

## 設定

監視間隔とファイル命名は、ソースコードを修正することでカスタマイズできます:

- **チェック間隔**: `watch_clipboard()`メソッド内の`time.sleep(0.5)`を変更
- **ファイル命名**: 異なる命名スキームのために`get_next_filename()`メソッドを修正

## トラブルシューティング

**"No module named 'tkinter'"**: このプログラムは、より良いLinux/WSL互換性のためにtkinterの代わりに`xclip`/`xsel`を使用します。

**クリップボードが検出されない**: `xclip`または`xsel`がインストールされていることを確認:
```bash
which xclip
# または
which xsel
```

**権限の問題**: スクリプトに実行権限があることを確認:
```bash
chmod +x clipboard_watcher.py
```

## ライセンス

このプロジェクトはオープンソースで、[MIT License](LICENSE)の下で利用可能です。

## 貢献

貢献を歓迎します！プルリクエストをお気軽に提出してください。
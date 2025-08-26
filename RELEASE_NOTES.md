# Release Notes

## Version 1.0.0 (2024-08-27)

### 🎉 初期リリース

AI Dev Tool（ai-dev）の最初の公式リリースです。GeminiおよびClaude CLIを活用して、システム開発ドキュメントを自動生成します。

### ✨ 主な機能

#### ✅ 安定版機能
- **ドキュメント生成**
  - 要件定義書の自動生成
  - テストケースの作成
  - タスクリストの生成
  - Q&Aドキュメントの生成
  - テスト概念書の作成

- **ファイル解析**
  - テキストファイル（.txt）の解析
  - Markdownファイル（.md）の解析
  - テキスト抽出と統計情報の取得

- **AI統合**
  - Gemini CLI対応
  - Claude Code CLI対応
  - モデル切り替え機能

- **出力形式**
  - Markdown形式
  - CSV形式
  - JSON形式
  - プレーンテキスト

#### 🚧 開発中/テスト中の機能
以下の機能は現在開発中であり、動作が不安定な場合があります：

- **Excel/CSV解析**
  - データ統計情報の抽出
  - 列情報とデータ型の解析
  - サンプルデータのプレビュー

- **PowerPoint解析**
  - スライド内容の抽出
  - アウトラインの生成
  - テーブルとチャートの検出

- **PDF解析**
  - ページ情報の取得
  - メタデータの抽出
  - 目次の取得

### 📋 必要な環境
- Ubuntu/Debian系Linux（WSL2対応）
- Python 3.8以上
- Gemini CLIまたはClaude Code CLI

### ⚠️ 既知の問題
- Excel/CSV、PowerPoint、PDF解析機能は開発中のため、エラーが発生する可能性があります
- 大容量ファイル（>100MB）の処理が遅い場合があります
- 日本語環境では`-e utf-8`オプションの使用を推奨

### 🔧 インストール
```bash
# セットアップスクリプトを実行
chmod +x setup.sh
./setup.sh

# または手動インストール
pip install -r requirements.txt
pip install -e .
```

### 📝 使用例
```bash
# テキストファイルから要件定義書を生成
ai-dev generate requirements input.txt -e utf-8

# ファイルを解析して統計情報を表示
ai-dev analyze file document.txt

# Claude CLIを使用して生成
ai-dev --ai claude generate test-cases input.txt -e utf-8
```

### 🚀 今後の予定
- Excel/CSV、PowerPoint、PDF解析機能の安定化
- 画像ファイルの内容解析
- より高度な統計分析機能
- バッチ処理の最適化

### 📚 ドキュメント
- [README.md](README.md) - プロジェクト概要
- [USAGE.md](USAGE.md) - 詳細な使用方法
- [FILE_ANALYSIS.md](FILE_ANALYSIS.md) - ファイル解析機能
- [CLAUDE_SETUP.md](CLAUDE_SETUP.md) - Claude CLI設定ガイド
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - トラブルシューティング

### 🙏 謝辞
このプロジェクトは、Anthropic社のClaude Code CLIとGoogle社のGemini CLIを活用しています。

---

**注意**: このバージョンは初期リリースです。Excel/CSV、PowerPoint、PDF解析機能は開発中のため、プロダクション環境での使用は推奨されません。安定した動作が必要な場合は、テキストファイルの使用をお勧めします。
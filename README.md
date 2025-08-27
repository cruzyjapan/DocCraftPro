# AI Dev Tool

AI Dev Tool（ai-dev）は、Gemini CLIやClaude Code CLIを活用して、システム開発に必要な各種ドキュメントを自動生成するコマンドラインツールです。

📦 **GitHub Repository**: https://github.com/cruzyjapan/DocCraftPro

## ✨ 主な機能

### ドキュメント生成
- 📝 **要件定義書の自動生成** - プロジェクトの説明から詳細な要件を生成
- ✅ **テストケースの作成** - 機能要件に基づいたテストケースを自動作成
- 📋 **タスクリストの生成** - 開発タスクを優先度付きで整理
- ❓ **Q&Aドキュメント** - よくある質問と回答を自動生成
- 🎯 **テスト概念書** - テスト戦略とアプローチを文書化

### ファイル解析
- 📝 **テキスト/Markdown解析** - 構造とセクションの分析（✅ 利用可能）
- 📊 **Excel/CSV分析** - データの統計情報と構造を解析（🚧 開発中/テスト中）
- 📑 **PowerPoint解析** - スライド内容とテーブルの抽出（🚧 開発中/テスト中）
- 📄 **PDF解析** - テキストとメタデータの抽出（🚧 開発中/テスト中）

## 📋 必要な環境

- Ubuntu/Debian系のLinux (WSL2も可)
- Python 3.10以上（推奨: Python 3.12）
- sudoの実行権限（python3-venvインストール用）
- Node.js 18以上（AI CLIツール用）
- 以下のいずれか：
  - Gemini CLI（Google AI）
  - Claude CLI（Anthropic）

## 🚀 クイックスタート（初めての方向け）

### ステップ1: 必要なパッケージをインストール

```bash
# Pythonの仮想環境パッケージをインストール（sudoパスワードが必要）
sudo apt update
sudo apt install -y python3.12-venv

# もしPython 3.12がない場合は、お使いのPythonバージョンに合わせて変更
# 例: sudo apt install -y python3.11-venv
```

### ステップ2: 自動セットアップを実行

```bash
# 自動セットアップスクリプトを実行
bash .init.sh

# 途中で「Do you want to recreate it? (y/N):」と聞かれたら、Nを押してEnter
# 最後に「Do you want to activate the virtual environment now? (Y/n):」と聞かれたら、Yを押してEnter
```

### ステップ3: 動作確認

```bash
# ツールが正しくインストールされたか確認
ai-dev --help

# ツールの状態を確認
ai-dev status
```

これで準備完了です！🎉

## 📦 詳細なインストール方法

### リポジトリのクローン

```bash
# GitHubからクローン
git clone https://github.com/cruzyjapan/DocCraftPro.git
cd DocCraftPro
```

### 方法1: 自動セットアップ（推奨）

```bash
# 1. python3-venvをインストール
sudo apt update
sudo apt install -y python3.12-venv

# 2. 自動セットアップスクリプトを実行
bash .init.sh

# このスクリプトは以下を自動で行います：
# - Python仮想環境の作成
# - 必要なパッケージのインストール
# - 設定ファイルの初期化
# - サンプルファイルの作成
# - 便利なスクリプトの生成
```

### 方法2: Makefileを使用

```bash
# 1. python3-venvをインストール
sudo apt install -y python3.12-venv

# 2. Makeコマンドで初期化
make init
```

### 方法3: 手動インストール

```bash
# 1. python3-venvをインストール
sudo apt install -y python3.12-venv

# 2. Python仮想環境を作成
python3 -m venv venv

# 3. 仮想環境を有効化
source venv/bin/activate

# 4. pipをアップグレード
pip install --upgrade pip

# 5. 必要なパッケージをインストール
pip install -r requirements.txt

# 6. ツールをインストール
pip install -e .

# 7. 初期設定
ai-dev init
```

### 方法4: sudoを使わない方法

```bash
# virtualenvを使った方法（sudoが不要）
bash setup_nosudo.sh
```

## 🔧 トラブルシューティング

### ⏱️ タイムアウトエラーが発生する場合
→ [TIMEOUT_GUIDE.md](TIMEOUT_GUIDE.md) を参照

**クイックフィックス**:
```bash
# カスタムタイムアウト設定（10分）
ai-dev --timeout 600 generate requirements input.txt -e utf-8
```

### エラー: "python3-venv is not installed"

このエラーが出た場合：

```bash
# Python 3.12の場合
sudo apt install python3.12-venv

# Python 3.11の場合
sudo apt install python3.11-venv

# Python 3.10の場合
sudo apt install python3.10-venv
```

### エラー: "init.sh: command not found"

```bash
# bashで実行
bash .init.sh

# または実行権限を付与してから実行
chmod +x .init.sh
./.init.sh
```

### エラー: "ai-dev: command not found"

```bash
# 仮想環境が有効になっているか確認
source venv/bin/activate

# または、仮想環境内で再インストール
pip install -e .
```

### Pythonバージョンの確認

```bash
# Pythonのバージョンを確認
python3 --version

# 3.10以上であることを確認してください
```

## 🎯 基本的な使い方

### 1. 仮想環境の有効化

```bash
# 毎回、ツールを使う前に実行
source venv/bin/activate

# または便利スクリプトを使用
./activate.sh
```

### 2. サンプルドキュメントの生成

```bash
# サンプル入力ファイルはすでに作成されています
ls sample_input*.txt

# 要件定義書を生成
ai-dev generate requirements sample_input.txt

# テストケースを生成
ai-dev generate test-cases sample_input.txt

# 生成されたファイルを確認
ls output/
```

### 3. 自分のドキュメントを生成

```bash
# 1. 入力テキストファイルを作成
echo "ユーザー認証システムの開発" > my_project.txt

# 2. 要件定義書を生成（UTF-8推奨）
ai-dev generate requirements my_project.txt -o my_requirements.md -e utf-8

# 3. 他の形式でも出力可能
ai-dev generate requirements my_project.txt -f json -e utf-8
ai-dev generate requirements my_project.txt -f csv -e utf-8
ai-dev generate requirements my_project.txt -f html -e utf-8
```

**重要**: 日本語環境では `-e utf-8` オプションの使用を推奨します。

## 📝 コマンド一覧

### 基本コマンド

| コマンド | 説明 |
|---------|------|
| `ai-dev --help` | ヘルプを表示 |
| `ai-dev status` | 現在の設定状態を表示 |
| `ai-dev init` | 初期設定を作成 |

### ファイル解析コマンド

| コマンド | 説明 | 例 | 対応状況 |
|---------|------|-----|---------|
| `analyze file` | テキストファイルを解析 | `ai-dev analyze file input.txt` | ✅ 利用可能 |
| `analyze file` | Excel/CSVを解析 | `ai-dev analyze file data.csv` | 🚧 開発中 |
| `analyze file` | PowerPointを解析 | `ai-dev analyze file slides.pptx` | 🚧 開発中 |
| `analyze file` | PDFを解析 | `ai-dev analyze file doc.pdf` | 🚧 開発中 |
| `--extract-text` | テキストのみ抽出 | `ai-dev analyze file input.txt --extract-text` | ✅ 利用可能 |

### ドキュメント生成コマンド

| コマンド | 説明 | 例 |
|---------|------|-----|
| `generate requirements` | 要件定義書を生成 | `ai-dev generate requirements input.txt` |
| `generate qa` | QAドキュメントを生成 | `ai-dev generate qa input.txt` |
| `generate tasks` | タスクリストを生成 | `ai-dev generate tasks input.txt` |
| `generate test-concept` | テスト概念書を生成 | `ai-dev generate test-concept input.txt` |
| `generate test-cases` | テストケースを生成 | `ai-dev generate test-cases input.txt` |

### オプション

| オプション | 説明 | 例 |
|-----------|------|-----|
| `-o, --output` | 出力ファイル名を指定 | `-o output.md` |
| `-f, --format` | 出力形式を指定 | `-f json` |
| `-e, --encoding` | 文字エンコーディングを指定 | `-e utf-8` |

### 出力形式

- `md` または `markdown` - Markdown形式（デフォルト）
- `json` - JSON形式
- `csv` - CSV形式
- `html` - HTML形式

## 🔄 AIモデルの切り替え

### サポートされているAIモデル

| モデル | 提供元 | 特徴 | インストールコマンド |
|--------|--------|------|-------------------|
| Gemini | Google | 高速、日本語対応良好 | `npm install -g @google/generative-ai-cli` |
| Claude | Anthropic | 高品質、詳細な出力 | `npm install -g @anthropic/claude-cli` |

### モデルの切り替え

```bash
# 現在のAIモデルを確認
ai-dev status

# Geminiに切り替え
ai-dev use gemini

# Claudeに切り替え
ai-dev use claude

# 一時的に特定のモデルを使用
ai-dev --ai claude generate requirements input.txt -e utf-8
```

### セットアップ

```bash
# Gemini CLIのセットアップ
gemini --version

# Claude CLIのセットアップ
claude login  # ブラウザで認証
```

詳細は[Claude Setup Guide](CLAUDE_SETUP.md)を参照してください。

## 🛠️ 開発者向けコマンド

### Makefileコマンド

```bash
make help          # ヘルプを表示
make init          # 完全初期化
make install       # 依存関係のインストール
make install-dev   # 開発用依存関係もインストール
make test          # テストを実行
make format        # コードをフォーマット
make lint          # リントチェック
make clean         # 一時ファイルを削除
make clean-all     # 全てクリーンアップ（venv含む）
```

## 📁 プロジェクト構成

```
DocCraftPro/
├── .init.sh           # 自動セットアップスクリプト
├── requirements.txt   # Pythonパッケージ一覧
├── setup.py          # パッケージ設定
├── Makefile          # Make コマンド定義
├── src/
│   └── ai_dev/       # メインソースコード
│       ├── cli.py    # CLIコマンド
│       ├── generators/   # ドキュメント生成器
│       ├── ai_models/    # AIモデルラッパー
│       └── utils/        # ユーティリティ
├── config/
│   └── default.yaml  # デフォルト設定
├── output/           # 生成されたドキュメント（自動作成）
└── venv/            # Python仮想環境（自動作成）
```

## ⚠️ 既知の問題と対処法

### Gemini CLIのインストール

Gemini CLIは別途インストールが必要です：
```bash
# Node.jsが必要
npm install -g @google/generative-ai-cli
```

### エンコーディングについて

日本語を含むドキュメントを生成する場合は、必ず `-e utf-8` オプションを使用してください：
```bash
# 正しい使い方
ai-dev generate requirements input.txt -e utf-8

# デフォルト（Shift-JIS）では文字化けする可能性があります
```

## ❓ よくある質問

### Q: 「Items: 0」と表示される

A: Gemini CLIが正しくインストールされているか確認してください。また、入力ファイルの内容が短すぎる可能性があります。

### Q: sudoパスワードを入力したくない

A: `bash setup_nosudo.sh`を使用してください。virtualenvを使った方法でインストールできます。

### Q: Windows で使いたい

A: WSL2（Windows Subsystem for Linux）を使用してください。WSL2のUbuntu環境で上記の手順を実行できます。

### Q: 仮想環境を有効化し忘れる

A: `.bashrc`に以下を追加すると、ディレクトリに入った時に自動で有効化されます：

```bash
# .bashrcに追加
cd() {
    builtin cd "$@"
    if [ -f venv/bin/activate ]; then
        source venv/bin/activate
    fi
}
```

### Q: 生成されたドキュメントの文字化け

A: **必ず** `-e utf-8` オプションを使用してください：

```bash
# 推奨: UTF-8で出力
ai-dev generate requirements input.txt -e utf-8

# Shift-JISは特殊な場合のみ使用
ai-dev generate requirements input.txt -e shift-jis
```

## 📄 ライセンス

MIT License

## 🤝 貢献

プルリクエストを歓迎します。大きな変更の場合は、まずissueを開いて変更内容について議論してください。

## 📞 サポート

問題や質問がある場合は、[GitHub Issues](https://github.com/yourusername/ai-dev-tool/issues)ページを使用してください。
# AI Dev Tool の使い方

## 1️⃣ まず最初にセットアップ

```bash
# 必要なパッケージをインストール（sudoパスワード必要）
sudo apt update
sudo apt install -y python3.12-venv

# セットアップスクリプトを実行
bash .init.sh
```

## 2️⃣ 仮想環境を有効化（毎回必要）

```bash
# 仮想環境を有効化
source venv/bin/activate

# これで (venv) というプレフィックスが表示されます
```

## 3️⃣ 動作確認

```bash
# ヘルプを表示
ai-dev --help

# 現在の状態を確認
ai-dev status
```

## 📝 実際に使ってみる

### サンプルで試す

```bash
# サンプルファイルを確認
cat sample_input.txt

# 要件定義書を生成（UTF-8エンコーディング推奨）
ai-dev generate requirements sample_input.txt -e utf-8

# 生成されたファイルを確認
ls output/
cat output/requirements_*.md
```

⚠️ **重要**: 日本語を含むドキュメントは必ず `-e utf-8` オプションを使用してください。

### 自分のプロジェクトで使う

#### 例1: ECサイトの要件定義書を作成

```bash
# 1. 入力ファイルを作成
cat > myproject.txt << EOF
ECサイトの開発

必要な機能：
- 商品検索
- カート機能  
- 決済処理
- ユーザー管理
EOF

# 2. 要件定義書を生成（UTF-8で出力）
ai-dev generate requirements myproject.txt -e utf-8

# 3. 結果を確認
ls output/
```

#### 例2: テストケースを生成

```bash
# テストケースをCSV形式で生成（UTF-8）
ai-dev generate test-cases myproject.txt -f csv -e utf-8

# 結果を確認
cat output/test_cases_*.csv
```

#### 例3: タスクリストを生成

```bash
# タスクリストをJSON形式で生成（UTF-8）
ai-dev generate tasks myproject.txt -f json -e utf-8

# 結果を確認
cat output/tasks_*.json
```

## 🎯 生成できるドキュメントの種類

| コマンド | 生成内容 | 使用例 |
|---------|---------|--------|
| `requirements` | 要件定義書 | 機能要件、非機能要件の一覧 |
| `qa` | Q&Aドキュメント | よくある質問と回答 |
| `tasks` | タスクリスト | 開発タスクの一覧 |
| `test-concept` | テスト概念書 | テスト方針と戦略 |
| `test-cases` | テストケース | 具体的なテスト手順 |

## 📄 出力形式の選択

```bash
# Markdown形式（デフォルト）- UTF-8推奨
ai-dev generate requirements input.txt -e utf-8

# JSON形式
ai-dev generate requirements input.txt -f json -e utf-8

# CSV形式（Excelで開ける）
ai-dev generate requirements input.txt -f csv -e utf-8

# HTML形式（ブラウザで表示）
ai-dev generate requirements input.txt -f html -e utf-8
```

💡 **ヒント**: 全てのコマンドで `-e utf-8` を付けることで文字化けを防げます。

## 💡 便利な使い方

### 出力ファイル名を指定

```bash
# 特定のファイル名で保存
ai-dev generate requirements input.txt -o my_requirements.md
ai-dev generate test-cases input.txt -o test_plan.csv -f csv
```

### 日本語環境での文字化け対策

```bash
# UTF-8で出力（Linux/Mac向け）
ai-dev generate requirements input.txt -e utf-8

# Shift-JISで出力（Windows向け）
ai-dev generate requirements input.txt -e shift-jis
```

### 設定の確認と変更

```bash
# 現在の設定を確認
ai-dev config show

# デフォルトの出力形式を変更
ai-dev config set output.default_format json

# デフォルトのエンコーディングを変更
ai-dev config set output.encoding utf-8
```

## ⚠️ 注意事項

1. **Gemini/Claude CLIは別途必要**
   - このツールはGemini CLIやClaude CLIのラッパーです
   - 実際にAI生成を行うには、これらのCLIツールが必要です
   - インストールされていない場合、生成時にエラーが表示されます

2. **仮想環境の有効化を忘れない**
   ```bash
   # 毎回、使用前に実行
   source venv/bin/activate
   ```

3. **入力ファイルは日本語OK**
   - UTF-8形式で日本語の入力ファイルが使えます

## 🔍 もっと詳しく知りたい場合

```bash
# 各コマンドのヘルプを見る
ai-dev generate --help
ai-dev generate requirements --help

# 設定ファイルを編集
nano config/default.yaml

# ログを詳しく見る
ai-dev --verbose generate requirements input.txt
```

## 🚀 クイックスタートまとめ

最小限の手順で始めるには：

```bash
# 1. セットアップ（初回のみ）
sudo apt install -y python3.12-venv
bash .init.sh

# 2. 仮想環境を有効化
source venv/bin/activate

# 3. 使用開始
ai-dev generate requirements sample_input.txt
```

## 📊 実践例

### プロジェクト全体のドキュメントを一括生成

```bash
# プロジェクト説明ファイルを作成
cat > project.txt << EOF
オンラインショッピングサイトの構築

機能要件：
- ユーザー登録・認証
- 商品カタログ
- ショッピングカート
- 注文管理
- 決済処理

非機能要件：
- レスポンシブデザイン
- SSL対応
- 負荷分散
EOF

# 各種ドキュメントを生成
ai-dev generate requirements project.txt -o docs/requirements.md
ai-dev generate test-cases project.txt -o docs/test_cases.csv -f csv
ai-dev generate tasks project.txt -o docs/tasks.json -f json
ai-dev generate qa project.txt -o docs/qa.md
ai-dev generate test-concept project.txt -o docs/test_concept.md

# 生成されたドキュメントを確認
ls -la docs/
```

### バッチ処理スクリプトの例

```bash
#!/bin/bash
# generate_all.sh

# 仮想環境を有効化
source venv/bin/activate

# 入力ファイル
INPUT="project_spec.txt"

# 出力ディレクトリ
OUTPUT_DIR="generated_docs"
mkdir -p $OUTPUT_DIR

# 全ドキュメントを生成
echo "Generating all documents..."

ai-dev generate requirements $INPUT -o $OUTPUT_DIR/requirements.md
echo "✓ Requirements generated"

ai-dev generate test-cases $INPUT -o $OUTPUT_DIR/test_cases.csv -f csv
echo "✓ Test cases generated"

ai-dev generate tasks $INPUT -o $OUTPUT_DIR/tasks.json -f json
echo "✓ Tasks generated"

ai-dev generate qa $INPUT -o $OUTPUT_DIR/qa.md
echo "✓ QA document generated"

ai-dev generate test-concept $INPUT -o $OUTPUT_DIR/test_concept.md
echo "✓ Test concept generated"

echo "All documents generated in $OUTPUT_DIR/"
```

## 🆘 トラブルシューティング

### よくある問題と解決方法

| 問題 | 解決方法 |
|------|---------|
| `ai-dev: command not found` | `source venv/bin/activate`を実行 |
| `python3-venv is not installed` | `sudo apt install python3.12-venv`を実行 |
| 文字化け | `-e utf-8`オプションを追加 |
| 権限エラー | ファイルのパーミッションを確認 |
| タイムアウト | 設定ファイルでtimeout値を増やす |

### デバッグモード

```bash
# 詳細なログを表示
ai-dev --verbose generate requirements input.txt

# Python のデバッグ情報を表示
python -m ai_dev.cli --verbose generate requirements input.txt
```

## 📚 関連ドキュメント

- `README.md` - プロジェクト概要とインストール方法
- `config/default.yaml` - 設定ファイル
- `docs/gemini-dev-tool-spec.md` - 詳細な開発仕様書

## 💬 サポート

問題が解決しない場合は、以下の情報を添えて報告してください：

1. エラーメッセージの全文
2. 使用したコマンド
3. Python バージョン (`python3 --version`)
4. OS情報 (`uname -a`)
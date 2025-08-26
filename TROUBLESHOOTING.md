# トラブルシューティングガイド

## 🔧 よくある問題と解決方法

### 1. 生成コマンドが動作しない

#### 症状
```bash
ai-dev generate test-cases sample_input.txt -e utf-8
# エラーまたは Items: 0 と表示される
```

#### 原因と解決方法

1. **Gemini CLIが未インストール**
   ```bash
   # Gemini CLIの確認
   which gemini
   
   # インストールされていない場合
   npm install -g @google/generative-ai-cli
   ```

2. **仮想環境が有効化されていない**
   ```bash
   # 仮想環境を有効化
   source venv/bin/activate
   
   # (venv) というプレフィックスが表示されることを確認
   ```

3. **入力ファイルが存在しない**
   ```bash
   # ファイルの存在確認
   ls -la sample_input.txt
   
   # サンプルファイルを作成
   bash .init.sh
   ```

### 2. 文字化けする

#### 症状
生成されたファイルが文字化けして読めない

#### 解決方法
**必ず** `-e utf-8` オプションを使用してください：

```bash
# 正しい使い方
ai-dev generate requirements input.txt -e utf-8

# 間違った使い方（デフォルトはShift-JIS）
ai-dev generate requirements input.txt  # ❌ 文字化けする可能性
```

### 3. "Items: 0" と表示される

#### 症状
```bash
✓ Requirements generated: output/requirements_*.md
   Encoding: utf-8
   Items: 0
```

#### 原因と解決方法

1. **Gemini CLIの応答が空**
   ```bash
   # Gemini CLIを直接テスト
   gemini --prompt "Hello, respond with: Hello World"
   
   # 何も返ってこない場合は、Gemini CLIの再インストールが必要
   ```

2. **入力ファイルが短すぎる**
   ```bash
   # より詳細な入力を作成
   cat > detailed_input.txt << EOF
   オンラインショッピングサイトの開発
   
   必要な機能：
   - ユーザー登録とログイン
   - 商品検索と一覧表示
   - ショッピングカート
   - 決済処理
   - 注文履歴
   EOF
   
   ai-dev generate requirements detailed_input.txt -e utf-8
   ```

### 4. プロンプトエラー

#### 症状
```
Error: Command failed: gemini --prompt ...
```

#### 解決方法

1. **タイムアウトを延長**
   ```bash
   # config/default.yamlを編集
   nano config/default.yaml
   
   # timeoutを120に変更
   ai_models:
     gemini:
       timeout: 120
   ```

2. **より簡単なプロンプトでテスト**
   ```bash
   # シンプルな入力でテスト
   echo "ユーザー登録機能を作る" > simple.txt
   ai-dev generate requirements simple.txt -e utf-8
   ```

### 5. Python関連のエラー

#### 症状
```
ModuleNotFoundError: No module named 'ai_dev'
```

#### 解決方法

```bash
# 仮想環境を確認
which python
# /path/to/venv/bin/python であることを確認

# 再インストール
pip install -e .

# 確認
python -c "from ai_dev.cli import cli; print('OK')"
```

### 6. 各ジェネレーターの修正が必要

他のジェネレーター（qa, tasks, test-cases）も同様の修正が必要な可能性があります。

#### 一時的な回避策

要件定義書の生成は動作するので、まずはそれを使用してください：

```bash
# 動作確認済み
ai-dev generate requirements sample_input.txt -e utf-8

# 他のコマンドは今後の修正で対応予定
# ai-dev generate test-cases sample_input.txt -e utf-8
# ai-dev generate tasks sample_input.txt -e utf-8
# ai-dev generate qa sample_input.txt -e utf-8
```

## 📊 デバッグ方法

### 詳細ログを表示

```bash
# Verboseモードで実行
ai-dev --verbose generate requirements input.txt -e utf-8

# Pythonデバッグ
python -m ai_dev.cli generate requirements input.txt -e utf-8
```

### テストスクリプトを実行

```bash
# テストスクリプトで動作確認
python test_gemini.py
```

### 設定を確認

```bash
# 現在の設定を表示
ai-dev config show

# ステータスを確認
ai-dev status
```

## 🆘 それでも解決しない場合

以下の情報を添えて報告してください：

1. **エラーメッセージの全文**
   ```bash
   ai-dev generate requirements input.txt -e utf-8 2>&1 | tee error.log
   ```

2. **環境情報**
   ```bash
   python3 --version
   pip list | grep -E "click|tabulate|pydantic"
   which gemini
   ```

3. **設定ファイル**
   ```bash
   cat config/default.yaml | head -30
   ```

## 🔄 クリーンインストール

問題が解決しない場合は、クリーンインストールを試してください：

```bash
# 1. 既存の環境を削除
deactivate
rm -rf venv

# 2. 再インストール
bash .init.sh

# 3. 仮想環境を有効化
source venv/bin/activate

# 4. テスト
ai-dev generate requirements sample_input.txt -e utf-8
```
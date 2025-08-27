# タイムアウト対策ガイド

AI Dev Toolでタイムアウトエラーが発生する場合の対処法です。

## 🚀 クイックフィックス

### 1. カスタムタイムアウトを設定

```bash
# 10分（600秒）のタイムアウトを設定
ai-dev --timeout 600 generate requirements input.txt -e utf-8

# 20分（1200秒）のタイムアウトを設定（大きなプロジェクト用）
ai-dev --timeout 1200 generate test-cases large_spec.txt -e utf-8
```

### 2. 詳細ログで確認

```bash
# --verbose オプションで詳細情報を表示
ai-dev --verbose --timeout 900 generate requirements input.txt
```

## ⚡ タイムアウト自動延長機能

AI Dev Toolには自動タイムアウト延長機能が組み込まれています：

### 仕組み
1. **初回**: 5分（300秒）でタイムアウト
2. **2回目**: 自動的に10分（600秒）に延長してリトライ
3. **3回目**: 自動的に20分（1200秒）に延長してリトライ

### 表示メッセージ
```
⏱️  Gemini CLI timed out after 300s.
    Extending timeout to 600s and retrying... (Attempt 2/3)
    💡 Tip: Use --timeout option to set a custom timeout
```

## 📊 推奨タイムアウト設定

| 使用ケース | 推奨タイムアウト | コマンド例 |
|-----------|-----------------|------------|
| 小規模（〜100行） | デフォルト（300秒） | `ai-dev generate requirements input.txt` |
| 中規模（100〜500行） | 600秒 | `ai-dev --timeout 600 generate requirements input.txt` |
| 大規模（500行〜） | 1200秒 | `ai-dev --timeout 1200 generate requirements input.txt` |
| 複雑な処理 | 1800秒 | `ai-dev --timeout 1800 generate test-cases complex.txt` |

## 🔧 永続的な設定変更

毎回タイムアウトを指定するのが面倒な場合は、設定ファイルを編集します：

### config/default.yaml を編集

```yaml
ai_models:
  gemini:
    timeout: 600  # 10分に変更
  claude:
    timeout: 600  # 10分に変更
```

## 💡 タイムアウトを減らすコツ

### 1. 入力ファイルを分割
```bash
# 大きなファイルを分割して処理
split -l 200 large_spec.txt spec_part_
for file in spec_part_*; do
  ai-dev generate requirements "$file" -o "req_$file.md"
done
```

### 2. シンプルなプロンプトを使用
- 複雑な要求を避ける
- 明確で簡潔な指示を書く
- 不要な詳細を省く

### 3. 高速モデルを使用
```bash
# Gemini Flash（高速版）を使用
ai-dev --ai gemini generate requirements input.txt
```

## 🆘 それでもタイムアウトする場合

### 1. ネットワーク確認
```bash
# API接続をテスト
gemini --prompt "Hello"
claude --print "Hello"
```

### 2. 最大タイムアウトで実行
```bash
# 30分（1800秒）のタイムアウト
ai-dev --timeout 1800 generate requirements input.txt
```

### 3. バックグラウンド実行
```bash
# nohupでバックグラウンド実行
nohup ai-dev --timeout 3600 generate requirements input.txt > output.log 2>&1 &
```

## 📝 トラブルシューティング

### エラー: "Command timed out after 3 attempts"
→ `--timeout` オプションでより長いタイムアウトを設定

### エラー: "API key" or "authentication"
→ AI CLIの認証を確認
```bash
gemini auth login
claude login
```

### プロセスが固まる
→ Ctrl+C で中断して、より短い入力で再試行

## 🔍 デバッグモード

問題の詳細を確認：
```bash
# 詳細ログを有効化
export AI_DEV_DEBUG=1
ai-dev --verbose --timeout 600 generate requirements input.txt
```

---

**注意**: タイムアウトは処理時間の目安です。実際の処理時間は、AIサービスの負荷、ネットワーク状況、プロンプトの複雑さによって変動します。
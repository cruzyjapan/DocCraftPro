# Claude CLI Setup Guide

## 📋 Prerequisites

- Node.js 18 or higher
- npm or yarn
- Anthropic API access

## 🚀 Installation

### 1. Install Claude CLI

```bash
# Install Claude CLI globally
npm install -g @anthropic/claude-cli

# Verify installation
claude --version
```

### 2. Login to Claude

```bash
# Login with your Anthropic credentials
claude login

# Follow the browser authentication flow
```

## 🔧 Configuration

Claude is pre-configured in `config/default.yaml`:

```yaml
ai_models:
  claude:
    command: "claude"
    model: "claude-3-5-sonnet-latest"
    options: []
    timeout: 90
```

## 📝 Usage with AI Dev Tool

### Switch to Claude Model

```bash
# Switch default model to Claude
ai-dev use claude

# Or use Claude for a single command
ai-dev --ai claude generate requirements input.txt -e utf-8
```

### Generate Documents with Claude

```bash
# Generate requirements
ai-dev generate requirements sample_input.txt -e utf-8

# Generate test cases
ai-dev generate test-cases sample_input.txt -e utf-8

# Generate tasks
ai-dev generate tasks sample_input.txt -e utf-8

# Generate Q&A
ai-dev generate qa sample_input.txt -e utf-8
```

## 🔄 Switching Between Models

```bash
# Check current model
ai-dev status

# Switch to Claude
ai-dev use claude

# Switch back to Gemini
ai-dev use gemini
```

## ⚡ Performance Comparison

| Model | Speed | Quality | Japanese Support |
|-------|-------|---------|------------------|
| Gemini | Fast | Good | Excellent |
| Claude | Moderate | Excellent | Excellent |

## 🐛 Troubleshooting

### Authentication Issues

```bash
# If you get authentication errors
claude logout
claude login
```

### Timeout Issues

Claude may take longer to generate responses. If you experience timeouts:

1. Edit `config/default.yaml`
2. Increase the timeout value:
   ```yaml
   claude:
     timeout: 120  # Increase from 90 to 120 seconds
   ```

### Connection Test

```bash
# Test Claude connection
python test_claude.py

# Or use the CLI directly
claude --print "Hello, please respond with: OK"
```

## 🎯 Best Practices

1. **Use UTF-8 encoding** for Japanese text
   ```bash
   ai-dev generate requirements input.txt -e utf-8
   ```

2. **Model Selection**:
   - Use **Gemini** for quick drafts and iterations
   - Use **Claude** for final, high-quality documents

3. **Batch Processing**:
   ```bash
   # Generate all documents with Claude
   for type in requirements test-cases tasks qa; do
     ai-dev --ai claude generate $type input.txt -e utf-8
   done
   ```

## 📊 Example Output

Claude generates detailed, well-structured documents:

```markdown
| id      | category | priority | description | acceptance_criteria |
|---------|----------|----------|-------------|-------------------|
| REQ-001 | 機能要件  | 高       | ユーザー登録機能 | ・メールアドレス検証<br>・パスワード強度チェック |
```

## 🔗 Links

- [Claude CLI Documentation](https://docs.anthropic.com/claude/docs/claude-cli)
- [Anthropic API](https://www.anthropic.com/)
- [AI Dev Tool README](README.md)
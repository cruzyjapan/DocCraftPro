# File Analysis Features

AI Dev Tool can analyze various file formats and extract structured information for documentation generation.

## 📄 Supported File Formats

| Format | Extensions | Features | Status |
|--------|-----------|----------|--------|
| **Text** | .txt, .md | Content extraction, sections, lists, statistics | ✅ **利用可能** |
| **Spreadsheet** | .xlsx, .xls, .csv | Data analysis, statistics, formulas, charts | 🚧 **開発中/テスト中** |
| **PowerPoint** | .pptx | Slide content, tables, images count, outline | 🚧 **開発中/テスト中** |
| **PDF** | .pdf | Text extraction, metadata, bookmarks | 🚧 **開発中/テスト中** |

> **注意**: 初期バージョン（v1.0.0）では、テキストファイル（.txt, .md）の解析のみが安定して動作します。  
> Excel/CSV、PowerPoint、PDFの解析機能は開発中のため、動作が不安定な場合があります。

## 🚀 Usage

### Basic File Analysis

#### ✅ 利用可能（安定版）
```bash
# テキストファイルを解析
ai-dev analyze file input.txt

# Markdownファイルを解析
ai-dev analyze file README.md

# テキスト抽出と保存
ai-dev analyze file document.txt --extract-text -o extracted.txt
```

#### 🚧 開発中/テスト中
```bash
# CSV/Excelファイルを解析（開発中）
ai-dev analyze file data.csv

# PowerPointを解析（開発中）
ai-dev analyze file presentation.pptx

# PDFを解析（開発中）
ai-dev analyze file document.pdf --extract-text
```

### Output Formats

```bash
# Markdown format (default)
ai-dev analyze file data.xlsx -f md

# JSON format (detailed)
ai-dev analyze file report.pdf -f json -o analysis.json

# Plain text format
ai-dev analyze file notes.txt -f text
```

## 📊 Analysis Examples

### ✅ Text File Analysis（利用可能）
```bash
ai-dev analyze file requirements.txt
```

Output includes:
- File size and encoding
- Line count and word count
- Character statistics
- Section structure (for Markdown)
- Lists and code blocks detection

### 🚧 開発中の機能

以下の機能は現在開発中/テスト中です。動作が不安定な場合があります。

#### CSV/Excel Analysis（開発中）
```bash
ai-dev analyze file sales_data.csv  # 開発中
```

予定される出力内容:
- データの行列数
- 列名とデータ型
- 統計サマリー（平均、標準偏差、最小/最大）
- 欠損値の検出
- サンプルデータプレビュー

#### PowerPoint Analysis（開発中）
```bash
ai-dev analyze file presentation.pptx  # 開発中
```

予定される出力内容:
- スライド数とタイトル
- 各スライドのテキスト内容
- テーブルと画像数
- プレゼンテーションのアウトライン

#### PDF Analysis（開発中）
```bash
ai-dev analyze file document.pdf  # 開発中
```

予定される出力内容:
- ページ数
- メタデータ（著者、タイトル、作成日）
- テキスト内容
- 目次（利用可能な場合）

## 🔄 Integration with Document Generation

### ✅ 現在利用可能なワークフロー

```bash
# Step 1: テキストファイルから情報を抽出
ai-dev analyze file requirements.txt --extract-text -o extracted.txt

# Step 2: 抽出内容から要件定義書を生成
ai-dev generate requirements extracted.txt -e utf-8

# Step 3: テストケースを生成
ai-dev generate test-cases extracted.txt -e utf-8
```

### 🚧 開発中のワークフロー

```bash
# PowerPointからの抽出（開発中）
ai-dev analyze file presentation.pptx --extract-text -o extracted.txt

# Excelデータからの生成（開発中）
ai-dev analyze file data.xlsx --extract-text | ai-dev generate requirements -
```

## 🛠️ Advanced Usage

### Batch Processing

```bash
# Analyze multiple files
for file in *.pdf; do
  ai-dev analyze file "$file" -o "analysis/${file%.pdf}_analysis.json" -f json
done
```

### Pipeline with AI Generation

```bash
# Extract → Analyze → Generate
ai-dev analyze file spec.pptx --extract-text | \
ai-dev generate requirements - -e utf-8 | \
ai-dev generate test-cases - -e utf-8
```

## 📈 Statistics and Insights

### ✅ テキストファイル（利用可能）
- 文字数カウント
- 単語数カウント
- 行数カウント
- 段落数カウント
- セクション構造（Markdownの場合）

### 🚧 開発中の統計機能

#### スプレッドシート（開発中）
- 数値列: カウント、平均、標準偏差、最小/最大、四分位数
- テキスト列: ユニーク値、最頻値、欠損値
- 日付列: 日付範囲、欠損値

#### プレゼンテーション（開発中）
- レイアウトタイプ別スライド数
- スライドあたりの平均単語数
- テーブルとチャート数
- 画像使用状況

## 🔍 Text Extraction

Use `--extract-text` for simple text extraction:

```bash
# Extract all text from PDF
ai-dev analyze file manual.pdf --extract-text -o manual.txt

# Extract from Excel (all sheets)
ai-dev analyze file data.xlsx --extract-text

# Extract from PowerPoint (all slides)
ai-dev analyze file slides.pptx --extract-text
```

## 📝 Tips

1. **Large Files**: For large files, use `--extract-text` first to get a quick overview
2. **Encoding**: CSV files are auto-detected for encoding (UTF-8, Shift-JIS, etc.)
3. **Complex Excel**: Multi-sheet Excel files are fully analyzed with per-sheet statistics
4. **PDF Quality**: Text extraction quality depends on PDF structure (scanned PDFs may have issues)

## 🚧 Limitations

### ✅ 現在のバージョン（v1.0.0）
- **安定動作**: テキストファイル（.txt, .md）のみ
- **基本機能**: テキスト抽出、統計情報、構造解析

### 🚧 開発中の機能の制限事項
- **PowerPoint**: `.pptx`形式のみ対応（`.ppt`は未対応）
- **Excel**: 大容量ファイル（>100MB）は処理が遅い可能性
- **PDF**: OCRなしのスキャンPDFはテキスト抽出不可
- **画像**: 画像解析は枚数カウントのみ（内容解析は未実装）

> **注意**: Excel/CSV、PowerPoint、PDF解析機能は開発中のため、エラーが発生する可能性があります。  
> 安定した動作が必要な場合は、テキストファイルの使用を推奨します。

## 📋 Next Steps

After analyzing files, you can:

1. Generate requirements based on specifications
2. Create test cases from functional descriptions  
3. Build task lists from project plans
4. Generate Q&A from documentation

Example workflow:
```bash
# Complete documentation pipeline
ai-dev analyze file project_spec.pptx --extract-text -o spec.txt
ai-dev --ai claude generate requirements spec.txt -e utf-8
ai-dev --ai claude generate test-cases spec.txt -e utf-8
ai-dev --ai claude generate tasks spec.txt -e utf-8
```
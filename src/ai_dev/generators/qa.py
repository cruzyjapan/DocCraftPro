"""QA document generator"""

from typing import List, Dict, Any, Optional
import json
from .base import GeneratorBase


class QAGenerator(GeneratorBase):
    """Generate QA documents"""
    
    def generate(self, 
                input_text: str, 
                context: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Generate QA based on input text"""
        
        # Build prompt
        prompt = self._build_prompt(input_text, context)
        
        # Get current AI model and generate
        model = self.model_manager.get_current_model()
        if not model:
            raise RuntimeError("No AI model configured")
        
        response = model.generate(
            prompt, 
            output_format='json',
            encoding=self.config.get('output.encoding', 'shift-jis')
        )
        
        # Format output
        qa_items = self._format_output(response)
        
        return qa_items
    
    def _build_prompt(self, input_text: str, context: Optional[Dict[str, Any]]) -> str:
        """Build prompt for QA generation"""
        
        # Get configuration
        qa_config = self.config.get("generation.qa", {})
        columns = qa_config.get('columns', [])
        
        # Build column description
        column_desc = []
        for col in columns:
            if isinstance(col, dict):
                for key, value in col.items():
                    column_desc.append(f"- {key}: {value}")
        
        prompt = f"""
あなたはシステム開発のQ&Aドキュメント作成の専門家です。
以下の内容から、品質保証（QA）に関する質問と回答を生成してください。

==== 入力内容 ====
{input_text}

==== 出力形式 ====
必ず以下のカラムを持つJSON配列形式で出力してください：
{chr(10).join(column_desc)}

==== 出力例 ====
```json
[
  {{
    "id": "QA-001",
    "category": "機能",
    "question": "このシステムの主な機能は何ですか？",
    "answer": "主な機能は...",
    "status": "回答済み"
  }}
]
```

==== 注意事項 ====
1. 想定される質問と明確な回答を作成
2. 分類は「機能」「性能」「セキュリティ」「運用」などで設定
3. ステータスは「未回答」「回答済み」「確認中」などで設定
4. 技術的な質問と運用面の質問をバランスよく含める
5. 必ず```json と ``` で囲まれた有効なJSON配列を出力すること
6. 最低5個以上のQ&Aを生成すること

JSONのみを出力し、説明文は不要です。
"""
        
        # Add context if provided
        if context:
            context_str = "\n".join([f"{k}: {v}" for k, v in context.items()])
            prompt = f"コンテキスト:\n{context_str}\n\n{prompt}"
        
        return prompt
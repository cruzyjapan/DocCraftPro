"""Test cases document generator"""

from typing import List, Dict, Any, Optional
import json
from .base import GeneratorBase


class TestCasesGenerator(GeneratorBase):
    """Generate test cases"""
    
    def generate(self, 
                input_text: str, 
                context: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Generate test cases based on input text"""
        
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
        test_cases = self._format_output(response)
        
        return test_cases
    
    def _build_prompt(self, input_text: str, context: Optional[Dict[str, Any]]) -> str:
        """Build prompt for test cases generation"""
        
        # Get configuration
        test_config = self.config.get("generation.test_cases", {})
        columns = test_config.get('columns', [])
        
        # Build column description
        column_desc = []
        for col in columns:
            if isinstance(col, dict):
                for key, value in col.items():
                    column_desc.append(f"- {key}: {value}")
        
        prompt = f"""
あなたはソフトウェアテストの専門家です。
以下の内容から、テストケースを生成してください。

==== 入力内容 ====
{input_text}

==== 出力形式 ====
必ず以下のカラムを持つJSON配列形式で出力してください：
{chr(10).join(column_desc)}

==== 出力例 ====
```json
[
  {{
    "id": "TC-001",
    "category": "正常系",
    "precondition": "ユーザーがログインしている状態",
    "steps": "1. メニューを開く 2. 設定を選択 3. 保存をクリック",
    "expected": "設定が正しく保存される",
    "priority": "高"
  }}
]
```

==== 注意事項 ====
1. 前提条件は明確で再現可能な状態を記載
2. 手順は具体的で番号付きのステップにする
3. 期待結果は検証可能な内容にする
4. 優先度は「高」「中」「低」の3段階で設定
5. 分類は「正常系」「異常系」「境界値」などで設定
6. 網羅的なテストケースを作成する
7. 必ず```json と ``` で囲まれた有効なJSON配列を出力すること
8. 最低5個以上のテストケースを生成すること

JSONのみを出力し、説明文は不要です。
"""
        
        # Add context if provided
        if context:
            context_str = "\n".join([f"{k}: {v}" for k, v in context.items()])
            prompt = f"コンテキスト:\n{context_str}\n\n{prompt}"
        
        return prompt
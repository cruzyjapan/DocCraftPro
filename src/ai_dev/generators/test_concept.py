"""Test concept document generator"""

from typing import List, Dict, Any, Optional
import json
from .base import GeneratorBase


class TestConceptGenerator(GeneratorBase):
    """Generate test concept documents"""
    
    def generate(self, 
                input_text: str, 
                context: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Generate test concept based on input text"""
        
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
        test_concepts = self._format_output(response)
        
        return test_concepts
    
    def _build_prompt(self, input_text: str, context: Optional[Dict[str, Any]]) -> str:
        """Build prompt for test concept generation"""
        
        prompt = f"""
以下の内容から、テスト概念書を生成してください。

入力内容:
{input_text}

出力形式:
以下の構成でJSON配列形式で出力してください：
- test_id: テストID
- test_type: テストタイプ（単体/結合/システム/受入）
- scope: テスト範囲
- objective: テスト目的
- approach: テストアプローチ
- environment: テスト環境
- schedule: スケジュール
- risks: リスクと対策

以下の点に注意してください：
1. 各テストフェーズの目的と範囲を明確にする
2. テストアプローチは具体的な手法を記載
3. 必要な環境とツールを明記
4. リスクと対策は現実的な内容にする
5. スケジュールは工数を考慮した内容にする

必ず有効なJSON形式で出力してください。
"""
        
        # Add context if provided
        if context:
            context_str = "\n".join([f"{k}: {v}" for k, v in context.items()])
            prompt = f"コンテキスト:\n{context_str}\n\n{prompt}"
        
        return prompt
"""Requirements document generator"""

from typing import List, Dict, Any, Optional
import json
from .base import GeneratorBase


class RequirementsGenerator(GeneratorBase):
    """Generate requirements documents"""
    
    def generate(self, 
                input_text: str, 
                context: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Generate requirements based on input text"""
        
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
        requirements = self._format_output(response)
        
        return requirements
    
    def _build_prompt(self, input_text: str, context: Optional[Dict[str, Any]]) -> str:
        """Build prompt for requirements generation"""
        
        # Get configuration
        req_config = self.config.get("generation.requirements", {})
        columns = req_config.get('columns', [])
        criteria = req_config.get('criteria', [])
        
        # Build column description
        column_desc = []
        for col in columns:
            if isinstance(col, dict):
                for key, value in col.items():
                    column_desc.append(f"- {key}: {value}")
        
        # Build criteria description
        criteria_desc_list = []
        if criteria:
            for crit in criteria:
                if isinstance(crit, dict):
                    for key, value in crit.items():
                        criteria_desc_list.append(value)
                else:
                    criteria_desc_list.append(str(crit))
        criteria_desc = ", ".join(criteria_desc_list) if criteria_desc_list else "セキュリティ、パフォーマンス、使いやすさ"
        
        prompt = f"""
あなたはシステム要件定義のエキスパートです。
以下の内容から、システムの要件定義を生成してください。

==== 入力内容 ====
{input_text}

==== 重視する観点 ====
{criteria_desc}

==== 出力形式 ====
必ず以下のカラムを持つJSON配列形式で出力してください：
{chr(10).join(column_desc)}

==== 出力例 ====
```json
[
  {{
    "id": "REQ-001",
    "category": "機能要件",
    "priority": "高",
    "description": "要件の詳細説明",
    "acceptance_criteria": "受入基準の詳細"
  }}
]
```

==== 注意事項 ====
1. 各要件は具体的で測定可能な内容にする
2. 優先度は「高」「中」「低」の3段階で設定
3. 受入基準は明確で検証可能な条件を記載
4. カテゴリは機能要件/非機能要件/ビジネス要件などで分類
5. 必ず```json と ``` で囲まれた有効なJSON配列を出力すること
6. 最低5個以上の要件を生成すること

JSONのみを出力し、説明文は不要です。
"""
        
        # Add context if provided
        if context:
            context_str = "\n".join([f"{k}: {v}" for k, v in context.items()])
            prompt = f"コンテキスト:\n{context_str}\n\n{prompt}"
        
        return prompt
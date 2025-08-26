"""Tasks document generator"""

from typing import List, Dict, Any, Optional
import json
from .base import GeneratorBase


class TasksGenerator(GeneratorBase):
    """Generate task lists"""
    
    def generate(self, 
                input_text: str, 
                context: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Generate tasks based on input text"""
        
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
        tasks = self._format_output(response)
        
        return tasks
    
    def _build_prompt(self, input_text: str, context: Optional[Dict[str, Any]]) -> str:
        """Build prompt for tasks generation"""
        
        # Get configuration
        tasks_config = self.config.get("generation.tasks", {})
        columns = tasks_config.get('columns', [])
        
        # Build column description
        column_desc = []
        for col in columns:
            if isinstance(col, dict):
                for key, value in col.items():
                    column_desc.append(f"- {key}: {value}")
        
        prompt = f"""
あなたはプロジェクト管理の専門家です。
以下の内容から、プロジェクトのタスクリストを生成してください。

==== 入力内容 ====
{input_text}

==== 出力形式 ====
必ず以下のカラムを持つJSON配列形式で出力してください：
{chr(10).join(column_desc)}

==== 出力例 ====
```json
[
  {{
    "id": "TASK-001",
    "title": "データベース設計",
    "assignee": "未定",
    "priority": "高",
    "estimated_hours": "8",
    "status": "未着手"
  }}
]
```

==== 注意事項 ====
1. タスクは具体的で実行可能な内容にする
2. 優先度は「高」「中」「低」の3段階で設定
3. 見積時間は実現可能な範囲で設定（単位：時間）
4. ステータスは「未着手」「進行中」「完了」「保留」などで設定
5. タスク間の依存関係を考慮した順序にする
6. 必ず```json と ``` で囲まれた有効なJSON配列を出力すること
7. 最低5個以上のタスクを生成すること

JSONのみを出力し、説明文は不要です。
"""
        
        # Add context if provided
        if context:
            context_str = "\n".join([f"{k}: {v}" for k, v in context.items()])
            prompt = f"コンテキスト:\n{context_str}\n\n{prompt}"
        
        return prompt
"""Configuration Manager"""

import yaml
import json
from pathlib import Path
from typing import Any, Dict, Optional
from .schemas import ConfigSchema


class ConfigManager:
    """Manages configuration loading and saving"""
    
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or "config/default.yaml"
        self.config_data: Dict[str, Any] = {}
        self._load_config()
    
    def _load_config(self):
        """Load configuration from file"""
        path = Path(self.config_path)
        
        if path.exists():
            with open(path, 'r', encoding='utf-8') as f:
                if path.suffix == '.yaml' or path.suffix == '.yml':
                    self.config_data = yaml.safe_load(f) or {}
                elif path.suffix == '.json':
                    self.config_data = json.load(f)
                else:
                    raise ValueError(f"Unsupported config file format: {path.suffix}")
        else:
            # Load default configuration
            self._load_defaults()
    
    def _load_defaults(self):
        """Load default configuration"""
        self.config_data = {
            "project": {
                "name": "My Project",
                "version": "1.0.0",
                "description": "Project description",
                "encoding": "shift-jis"
            },
            "ai_models": {
                "default": "gemini",
                "gemini": {
                    "command": "gemini",
                    "models": {
                        "default": "gemini-2.5-pro",
                        "available": ["gemini-2.5-pro", "gemini-2.5-flash", "gemini-2.5-flash-lite"]
                    },
                    "options": ["--model=gemini-2.5-pro", "--temperature=0.7", "--max-tokens=8192", "--format=json"],
                    "timeout": 60
                },
                "claude": {
                    "command": "claude-code",
                    "model": "claude-opus-4",
                    "options": ["--temperature=0.7", "--max-tokens=8192"],
                    "timeout": 60
                }
            },
            "cli_execution": {
                "shell": True,
                "buffer_size": 4096,
                "stream_output": True,
                "error_handling": "retry",
                "max_retries": 3,
                "retry_delay": 2
            },
            "generation": {
                "requirements": {
                    "columns": [
                        {"id": "要件ID"},
                        {"category": "カテゴリ"},
                        {"priority": "優先度"},
                        {"description": "説明"},
                        {"acceptance_criteria": "受入基準"}
                    ],
                    "criteria": ["security", "performance", "usability", "scalability"]
                },
                "qa": {
                    "columns": [
                        {"id": "QA-ID"},
                        {"category": "分類"},
                        {"question": "質問"},
                        {"answer": "回答"},
                        {"status": "ステータス"}
                    ]
                },
                "tasks": {
                    "columns": [
                        {"id": "タスクID"},
                        {"title": "タイトル"},
                        {"assignee": "担当者"},
                        {"priority": "優先度"},
                        {"estimated_hours": "見積時間"},
                        {"status": "ステータス"}
                    ]
                },
                "test_cases": {
                    "columns": [
                        {"id": "TC-ID"},
                        {"category": "分類"},
                        {"precondition": "前提条件"},
                        {"steps": "手順"},
                        {"expected": "期待結果"},
                        {"priority": "優先度"}
                    ]
                }
            },
            "output": {
                "default_format": "markdown",
                "encoding": "shift-jis",
                "bom": False,
                "line_ending": "crlf",
                "directory": "./output",
                "timestamp": True
            },
            "analysis": {
                "extract_images": True,
                "extract_tables": True,
                "max_file_size": "50MB",
                "input_encoding": "auto",
                "supported_formats": [".pptx", ".xlsx", ".csv", ".txt", ".md"]
            }
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value using dot notation"""
        keys = key.split('.')
        value = self.config_data
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any):
        """Set configuration value using dot notation"""
        keys = key.split('.')
        config = self.config_data
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def save(self, path: Optional[str] = None):
        """Save configuration to file"""
        save_path = Path(path or self.config_path)
        save_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(save_path, 'w', encoding='utf-8') as f:
            if save_path.suffix == '.yaml' or save_path.suffix == '.yml':
                yaml.dump(self.config_data, f, default_flow_style=False, allow_unicode=True)
            elif save_path.suffix == '.json':
                json.dump(self.config_data, f, ensure_ascii=False, indent=2)
    
    def get_all(self) -> Dict[str, Any]:
        """Get all configuration data"""
        return self.config_data
    
    def validate(self) -> bool:
        """Validate configuration against schema"""
        try:
            ConfigSchema(**self.config_data)
            return True
        except Exception as e:
            print(f"Configuration validation failed: {e}")
            return False
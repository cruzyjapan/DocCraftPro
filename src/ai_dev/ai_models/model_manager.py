"""AI Model Manager for switching between different AI models"""

from typing import Dict, Any, Optional
from .gemini_cli import GeminiCLI
from .claude_cli import ClaudeCLI
from .base import AIModelBase


class ModelManager:
    """Manages AI models and handles switching between them"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.models = {
            'gemini': GeminiCLI,
            'claude': ClaudeCLI
        }
        self.current_model: Optional[AIModelBase] = None
        self.current_model_name: Optional[str] = None
        self._initialize_default_model()
    
    def _initialize_default_model(self):
        """Initialize the default model from config"""
        default_model = self.config.get('ai_models', {}).get('default', 'gemini')
        self.use_model(default_model)
    
    def use_model(self, model_name: str) -> None:
        """Switch to a specified AI model"""
        if model_name not in self.models:
            raise ValueError(f"Unknown model: {model_name}. Available models: {', '.join(self.models.keys())}")
        
        model_config = self.config.get('ai_models', {}).get(model_name, {})
        if not model_config:
            # Provide default configuration if not specified
            model_config = {
                'command': model_name if model_name == 'gemini' else 'claude-code',
                'options': [],
                'timeout': 60
            }
        
        model_class = self.models[model_name]
        self.current_model = model_class(model_config)
        self.current_model_name = model_name
        
        # Validate if the command is available
        if not self.current_model.validate_command():
            print(f"⚠️  Warning: {model_name} CLI command not found. Please ensure it's installed and in PATH.")
        
        print(f"✅ Switched to {model_name} model")
    
    def get_current_model(self) -> Optional[AIModelBase]:
        """Get the current active model"""
        return self.current_model
    
    def get_current_model_name(self) -> Optional[str]:
        """Get the name of the current active model"""
        return self.current_model_name
    
    def list_available_models(self) -> list:
        """List all available models"""
        return list(self.models.keys())
    
    def validate_current_model(self) -> bool:
        """Validate if the current model CLI is available"""
        if self.current_model:
            return self.current_model.validate_command()
        return False
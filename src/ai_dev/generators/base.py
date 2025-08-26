"""Base generator class for all document generators"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from pathlib import Path
import json
from datetime import datetime

from ..config.manager import ConfigManager
from ..ai_models.model_manager import ModelManager
from ..utils.encoder import EncodingHandler
from ..utils.formatter import OutputFormatter


class GeneratorBase(ABC):
    """Base class for all document generators"""
    
    def __init__(self, config: ConfigManager, model_manager: ModelManager):
        self.config = config
        self.model_manager = model_manager
        self.encoder = EncodingHandler()
        self.formatter = OutputFormatter()
    
    @abstractmethod
    def generate(self, 
                input_text: str, 
                context: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Generate document based on input text"""
        pass
    
    @abstractmethod
    def _build_prompt(self, input_text: str, context: Optional[Dict[str, Any]]) -> str:
        """Build prompt for AI model"""
        pass
    
    def _format_output(self, response: Any) -> List[Dict[str, Any]]:
        """Format AI response into structured output"""
        if isinstance(response, list):
            return response
        elif isinstance(response, dict):
            return [response]
        elif isinstance(response, str):
            try:
                data = json.loads(response)
                return data if isinstance(data, list) else [data]
            except json.JSONDecodeError:
                return [{"content": response}]
        else:
            return []
    
    def save_to_file(self, 
                    data: List[Dict[str, Any]], 
                    output_path: str,
                    format: Optional[str] = None,
                    title: str = ""):
        """Save generated data to file"""
        
        # Get output configuration
        output_config = self.config.get('output', {})
        if format is None:
            format = output_config.get('default_format', 'markdown')
        
        encoding = output_config.get('encoding', 'shift-jis')
        encoding = self.encoder.normalize_encoding_name(encoding)
        
        add_bom = output_config.get('bom', False)
        line_ending = output_config.get('line_ending', 'crlf')
        add_timestamp = output_config.get('timestamp', True)
        
        # Add timestamp to filename if configured
        if add_timestamp:
            path = Path(output_path)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            new_name = f"{path.stem}_{timestamp}{path.suffix}"
            output_path = str(path.parent / new_name)
        
        # Format content
        content = self.formatter.format_output(data, format, title)
        
        # Create output directory if not exists
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        # Write to file with encoding
        self.encoder.write_file(
            output_path,
            content,
            encoding=encoding,
            add_bom=add_bom,
            line_ending=line_ending
        )
        
        return output_path
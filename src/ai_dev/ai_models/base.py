"""Base AI Model Class"""

from abc import ABC, abstractmethod
import subprocess
import json
from typing import Dict, Any, Optional
import codecs
import tempfile
import os
from pathlib import Path


class AIModelBase(ABC):
    """Base class for AI model wrappers"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.command = config['command']
        self.options = config.get('options', [])
        self.timeout = config.get('timeout', 60)
    
    @abstractmethod
    def format_prompt(self, prompt: str) -> str:
        """Format prompt for specific model"""
        pass
    
    def execute_command(self, 
                       prompt: str, 
                       encoding: str = 'shift-jis') -> str:
        """Execute CLI command with encoding support"""
        
        # Save prompt to temporary file with specified encoding
        with tempfile.NamedTemporaryFile(
            mode='w', 
            encoding=encoding, 
            suffix='.txt',
            delete=False
        ) as tmp:
            tmp.write(self.format_prompt(prompt))
            tmp_path = tmp.name
        
        try:
            # Build command
            cmd = [self.command] + self.options + [tmp_path]
            
            # Execute command
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=False,  # Receive as binary
                timeout=self.timeout
            )
            
            # Decode output
            output = result.stdout.decode(encoding, errors='ignore')
            
            if result.returncode != 0:
                error = result.stderr.decode(encoding, errors='ignore')
                raise RuntimeError(f"Command failed: {error}")
            
            return output
            
        finally:
            os.unlink(tmp_path)
    
    @abstractmethod
    def generate(self, 
                prompt: str, 
                output_format: str = 'json',
                encoding: str = 'shift-jis') -> Any:
        """Generate text based on prompt"""
        pass
    
    def validate_command(self) -> bool:
        """Check if CLI command is available"""
        try:
            result = subprocess.run(
                [self.command, '--version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return False
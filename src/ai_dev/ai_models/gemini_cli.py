"""Gemini CLI Wrapper"""

from .base import AIModelBase
import json
import re
import subprocess
from typing import Any, Dict


class GeminiCLI(AIModelBase):
    """Gemini CLI wrapper for text generation"""
    
    def format_prompt(self, prompt: str) -> str:
        """Format prompt for Gemini CLI"""
        return prompt
    
    def execute_command(self, prompt: str, encoding: str = 'shift-jis') -> str:
        """Execute Gemini CLI command with direct prompt"""
        
        # Gemini CLI expects --prompt parameter directly
        cmd = [self.command, "--prompt", self.format_prompt(prompt)]
        
        try:
            # Execute command
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,  # Text mode for Gemini
                timeout=self.timeout
            )
            
            if result.returncode != 0:
                raise RuntimeError(f"Command failed: {result.stderr}")
            
            # Clean output - remove "Loaded cached credentials." and other non-content lines
            output_lines = result.stdout.split('\n')
            cleaned_lines = []
            for line in output_lines:
                if not line.startswith('Loaded cached credentials') and \
                   not line.startswith('Loading'):
                    cleaned_lines.append(line)
            
            return '\n'.join(cleaned_lines)
            
        except subprocess.TimeoutExpired:
            raise RuntimeError(f"Command timed out after {self.timeout} seconds")
        except FileNotFoundError:
            raise RuntimeError(f"Command '{self.command}' not found. Please install Gemini CLI.")
    
    def generate(self, 
                prompt: str, 
                output_format: str = 'json',
                encoding: str = 'shift-jis') -> Any:
        """Generate text using Gemini CLI"""
        
        # Add format specification to prompt
        formatted_prompt = f"""
{prompt}

Output format: {output_format}
Character encoding: {encoding}
"""
        
        # Execute CLI command
        output = self.execute_command(formatted_prompt, encoding)
        
        # Parse result based on format
        if output_format == 'json':
            # Try to extract JSON from markdown code block first
            code_block_match = re.search(r'```(?:json)?\s*\n([\s\S]*?)\n```', output)
            if code_block_match:
                json_str = code_block_match.group(1)
            else:
                # Otherwise try to find raw JSON
                json_match = re.search(r'(\{[\s\S]*\}|\[[\s\S]*\])', output)
                if json_match:
                    json_str = json_match.group(1)
                else:
                    # Return empty list if no JSON found
                    return []
            
            try:
                return json.loads(json_str)
            except json.JSONDecodeError as e:
                # If JSON parsing fails, return the output as a single item
                return [{"error": "Failed to parse JSON", "raw_output": output}]
        
        return output
    
    def generate_with_context(self,
                            prompt: str,
                            context: Dict[str, Any],
                            output_format: str = 'json',
                            encoding: str = 'shift-jis') -> Any:
        """Generate with additional context"""
        
        context_str = "\n".join([f"{k}: {v}" for k, v in context.items()])
        
        full_prompt = f"""
Context:
{context_str}

Request:
{prompt}
"""
        
        return self.generate(full_prompt, output_format, encoding)
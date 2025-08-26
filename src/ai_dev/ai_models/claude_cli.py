"""Claude Code CLI Wrapper"""

from .base import AIModelBase
import json
import re
import subprocess
from typing import Any, Dict, Optional
import os


class ClaudeCLI(AIModelBase):
    """Claude Code CLI wrapper for text generation"""
    
    def format_prompt(self, prompt: str) -> str:
        """Format prompt for Claude CLI"""
        return prompt
    
    def execute_command(self, prompt: str, encoding: str = 'utf-8') -> str:
        """Execute Claude CLI command with proper options"""
        
        # Claude CLI expects the prompt as an argument with --print option for non-interactive mode
        # Use --output-format json for JSON responses
        cmd = [
            self.command,
            "--print",  # Non-interactive mode
            "--output-format", "text",  # We'll request JSON in the prompt itself
            prompt
        ]
        
        # Add any additional options from config
        if self.options:
            # Filter out options that don't apply to Claude
            for opt in self.options:
                if opt and not opt.startswith('--temperature') and not opt.startswith('--max-tokens'):
                    cmd.insert(1, opt)  # Insert after command but before prompt
        
        try:
            # Execute command
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.timeout,
                env={**os.environ, "CLAUDE_NONINTERACTIVE": "1"}  # Ensure non-interactive mode
            )
            
            if result.returncode != 0:
                # Check for specific error messages
                if "API key" in result.stderr or "authentication" in result.stderr.lower():
                    raise RuntimeError("Claude CLI authentication error. Please ensure you're logged in with 'claude login'")
                raise RuntimeError(f"Command failed: {result.stderr}")
            
            return result.stdout
            
        except subprocess.TimeoutExpired:
            raise RuntimeError(f"Command timed out after {self.timeout} seconds")
        except FileNotFoundError:
            raise RuntimeError(f"Command '{self.command}' not found. Please install Claude CLI.")
    
    def generate(self, 
                prompt: str, 
                output_format: str = 'json',
                encoding: str = 'utf-8') -> Any:
        """Generate text using Claude CLI"""
        
        # Add format specification to prompt
        formatted_prompt = f"""
{prompt}

Output format: {output_format}
Please provide the output in valid {output_format} format only, without any explanatory text.
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
                            encoding: str = 'utf-8') -> Any:
        """Generate with additional context"""
        
        context_str = "\n".join([f"{k}: {v}" for k, v in context.items()])
        
        full_prompt = f"""
Context:
{context_str}

Request:
{prompt}
"""
        
        return self.generate(full_prompt, output_format, encoding)
    
    def test_connection(self) -> bool:
        """Test if Claude CLI is properly configured and authenticated"""
        try:
            cmd = [self.command, "--print", "Say 'ok' if you can read this"]
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.returncode == 0 and len(result.stdout) > 0
        except:
            return False
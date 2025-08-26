"""CLI command executor with retry logic"""

import subprocess
import time
from typing import Optional, Tuple


class CLIExecutor:
    """Execute CLI commands with retry and error handling"""
    
    def __init__(self, max_retries: int = 3, retry_delay: int = 2):
        self.max_retries = max_retries
        self.retry_delay = retry_delay
    
    def execute(
        self, 
        command: list, 
        timeout: Optional[int] = None,
        shell: bool = False,
        capture_output: bool = True
    ) -> Tuple[int, str, str]:
        """Execute command with retry logic"""
        
        for attempt in range(self.max_retries):
            try:
                if shell:
                    # Join command for shell execution
                    cmd = ' '.join(command) if isinstance(command, list) else command
                else:
                    cmd = command
                
                result = subprocess.run(
                    cmd,
                    shell=shell,
                    capture_output=capture_output,
                    text=True,
                    timeout=timeout
                )
                
                return result.returncode, result.stdout, result.stderr
                
            except subprocess.TimeoutExpired as e:
                if attempt < self.max_retries - 1:
                    print(f"Command timed out. Retrying... (Attempt {attempt + 2}/{self.max_retries})")
                    time.sleep(self.retry_delay)
                else:
                    raise e
            except Exception as e:
                if attempt < self.max_retries - 1:
                    print(f"Command failed: {e}. Retrying... (Attempt {attempt + 2}/{self.max_retries})")
                    time.sleep(self.retry_delay)
                else:
                    raise e
        
        # Should not reach here
        return -1, "", "Maximum retries exceeded"
    
    def stream_execute(
        self,
        command: list,
        timeout: Optional[int] = None,
        shell: bool = False
    ):
        """Execute command with streaming output"""
        
        if shell:
            cmd = ' '.join(command) if isinstance(command, list) else command
        else:
            cmd = command
        
        process = subprocess.Popen(
            cmd,
            shell=shell,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        # Stream output
        for line in iter(process.stdout.readline, ''):
            if line:
                yield ('stdout', line.rstrip())
        
        # Wait for process to complete
        process.wait(timeout=timeout)
        
        # Get any remaining stderr
        stderr = process.stderr.read()
        if stderr:
            yield ('stderr', stderr.rstrip())
        
        yield ('returncode', process.returncode)
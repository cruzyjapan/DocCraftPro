"""Configuration schemas using Pydantic"""

from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field


class ColumnConfig(BaseModel):
    """Column configuration for generated documents"""
    id: str
    name: str
    required: bool = True


class GenerationTypeConfig(BaseModel):
    """Configuration for a specific generation type"""
    columns: List[Dict[str, str]]
    criteria: Optional[List[str]] = []
    template: Optional[str] = None


class GenerationConfig(BaseModel):
    """Generation settings configuration"""
    requirements: GenerationTypeConfig
    qa: GenerationTypeConfig
    tasks: GenerationTypeConfig
    test_concept: Optional[GenerationTypeConfig] = None
    test_cases: GenerationTypeConfig


class OutputConfig(BaseModel):
    """Output settings configuration"""
    default_format: str = "markdown"
    encoding: str = "shift-jis"
    bom: bool = False
    line_ending: str = "crlf"  # crlf or lf
    directory: str = "./output"
    timestamp: bool = True


class AIModelConfig(BaseModel):
    """AI Model configuration"""
    command: str
    model: Optional[str] = None
    models: Optional[Dict[str, Any]] = None
    options: List[str] = []
    timeout: int = 60


class AIModelsConfig(BaseModel):
    """AI Models configuration"""
    default: str = "gemini"
    gemini: Optional[AIModelConfig] = None
    claude: Optional[AIModelConfig] = None


class CLIExecutionConfig(BaseModel):
    """CLI Execution configuration"""
    shell: bool = True
    buffer_size: int = 4096
    stream_output: bool = True
    error_handling: str = "retry"
    max_retries: int = 3
    retry_delay: int = 2


class AnalysisConfig(BaseModel):
    """File analysis configuration"""
    extract_images: bool = True
    extract_tables: bool = True
    max_file_size: str = "50MB"
    input_encoding: str = "auto"
    supported_formats: List[str] = [".pptx", ".xlsx", ".csv", ".txt", ".md"]


class ProjectConfig(BaseModel):
    """Project configuration"""
    name: str = "My Project"
    version: str = "1.0.0"
    description: str = "Project description"
    encoding: str = "shift-jis"


class ConfigSchema(BaseModel):
    """Complete configuration schema"""
    project: ProjectConfig = ProjectConfig()
    ai_models: AIModelsConfig = AIModelsConfig()
    cli_execution: CLIExecutionConfig = CLIExecutionConfig()
    generation: GenerationConfig
    output: OutputConfig = OutputConfig()
    analysis: AnalysisConfig = AnalysisConfig()
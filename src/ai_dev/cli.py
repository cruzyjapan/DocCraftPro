"""CLI interface for AI Dev Tool"""

import click
from pathlib import Path
from typing import Dict, Any
from rich.console import Console
from rich.table import Table
from rich import print as rprint
import codecs

from .config.manager import ConfigManager
from .ai_models.model_manager import ModelManager
from .generators.requirements import RequirementsGenerator
from .generators.qa import QAGenerator
from .generators.tasks import TasksGenerator
from .generators.test_concept import TestConceptGenerator
from .generators.test_cases import TestCasesGenerator
from .utils.encoder import EncodingHandler
from .analyzers import TextAnalyzer, PPTAnalyzer, SpreadsheetAnalyzer, PDFAnalyzer

console = Console()


@click.group()
@click.option('--config', '-c', type=click.Path(), 
              help='Configuration file path')
@click.option('--ai', '-a', 
              type=click.Choice(['gemini', 'claude']),
              help='AI model to use')
@click.option('--verbose', '-v', is_flag=True,
              help='Enable verbose output')
@click.pass_context
def cli(ctx, config, ai, verbose):
    """AI Dev Tool - System Development Support Tool"""
    ctx.ensure_object(dict)
    ctx.obj['config'] = ConfigManager(config)
    ctx.obj['model_manager'] = ModelManager(ctx.obj['config'].get_all())
    ctx.obj['verbose'] = verbose
    
    # Switch AI model if specified
    if ai:
        ctx.obj['model_manager'].use_model(ai)


@cli.command('use')
@click.argument('model', type=click.Choice(['gemini', 'claude']))
@click.pass_context
def use_model(ctx, model):
    """Switch AI model"""
    model_manager = ctx.obj['model_manager']
    model_manager.use_model(model)
    
    # Save configuration
    config = ctx.obj['config']
    config.set('ai_models.default', model)
    config.save()


@cli.command('status')
@click.pass_context
def status(ctx):
    """Display current configuration status"""
    config = ctx.obj['config']
    model_manager = ctx.obj['model_manager']
    
    # Create status table
    table = Table(title="AI Dev Tool Status")
    table.add_column("Setting", style="cyan", no_wrap=True)
    table.add_column("Value", style="magenta")
    
    table.add_row("AI Model", config.get('ai_models.default', 'Not set'))
    table.add_row("Encoding", config.get('output.encoding', 'Not set'))
    table.add_row("Output Directory", config.get('output.directory', 'Not set'))
    table.add_row("Output Format", config.get('output.default_format', 'Not set'))
    table.add_row("Available Models", ', '.join(model_manager.list_available_models()))
    
    # Check if current model is available
    if model_manager.validate_current_model():
        table.add_row("Model Status", "[green]✓ Available[/green]")
    else:
        table.add_row("Model Status", "[red]✗ Not Available[/red]")
    
    console.print(table)


@cli.command('init')
@click.option('--force', '-f', is_flag=True,
              help='Force overwrite existing configuration')
@click.pass_context
def init(ctx, force):
    """Initialize project configuration"""
    config = ctx.obj['config']
    
    config_path = Path("config/default.yaml")
    
    if config_path.exists() and not force:
        if not click.confirm("Configuration file already exists. Overwrite?"):
            console.print("[yellow]Initialization cancelled[/yellow]")
            return
    
    # Save default configuration
    config.save("config/default.yaml")
    console.print("[green]✓[/green] Configuration initialized at config/default.yaml")
    
    # Create output directory
    output_dir = Path(config.get('output.directory', './output'))
    output_dir.mkdir(parents=True, exist_ok=True)
    console.print(f"[green]✓[/green] Output directory created at {output_dir}")


@cli.group()
@click.pass_context
def generate(ctx):
    """Generate documents"""
    pass


@generate.command('requirements')
@click.argument('input_file', type=click.Path(exists=True))
@click.option('--output', '-o', type=click.Path(), 
              help='Output file path')
@click.option('--format', '-f', 
              type=click.Choice(['json', 'csv', 'md', 'markdown', 'html']),
              help='Output format')
@click.option('--encoding', '-e',
              type=click.Choice(['shift-jis', 'utf-8', 'cp932']),
              help='Output encoding')
@click.pass_context
def generate_requirements(ctx, input_file, output, format, encoding):
    """Generate requirements document"""
    config = ctx.obj['config']
    model_manager = ctx.obj['model_manager']
    
    # Override encoding if specified
    if encoding:
        config.set('output.encoding', encoding)
    
    # Set output format if specified
    if format:
        config.set('output.default_format', format)
    
    generator = RequirementsGenerator(config, model_manager)
    
    # Read input file
    encoder = EncodingHandler()
    input_text, input_encoding = encoder.read_file_auto(input_file)
    
    if ctx.obj['verbose']:
        console.print(f"[dim]Input encoding detected: {input_encoding}[/dim]")
    
    with console.status(f"Generating requirements with {model_manager.get_current_model_name()}..."):
        try:
            # Generate requirements
            requirements = generator.generate(input_text)
            
            # Save to file
            if not output:
                output = f"{config.get('output.directory', './output')}/requirements.{format or 'md'}"
            
            saved_path = generator.save_to_file(requirements, output, format, "Requirements")
            
            console.print(f"[green]✓[/green] Requirements generated: {saved_path}")
            console.print(f"   Encoding: {config.get('output.encoding', 'utf-8')}")
            console.print(f"   Items: {len(requirements)}")
            
        except Exception as e:
            console.print(f"[red]✗[/red] Error: {str(e)}")
            if ctx.obj['verbose']:
                import traceback
                console.print(traceback.format_exc())


@generate.command('qa')
@click.argument('input_file', type=click.Path(exists=True))
@click.option('--output', '-o', type=click.Path(), 
              help='Output file path')
@click.option('--format', '-f', 
              type=click.Choice(['json', 'csv', 'md', 'markdown', 'html']),
              help='Output format')
@click.option('--encoding', '-e',
              type=click.Choice(['shift-jis', 'utf-8', 'cp932']),
              help='Output encoding')
@click.pass_context
def generate_qa(ctx, input_file, output, format, encoding):
    """Generate QA document"""
    config = ctx.obj['config']
    model_manager = ctx.obj['model_manager']
    
    # Override encoding if specified
    if encoding:
        config.set('output.encoding', encoding)
    
    if format:
        config.set('output.default_format', format)
    
    generator = QAGenerator(config, model_manager)
    encoder = EncodingHandler()
    input_text, _ = encoder.read_file_auto(input_file)
    
    with console.status(f"Generating QA with {model_manager.get_current_model_name()}..."):
        try:
            qa_items = generator.generate(input_text)
            
            if not output:
                output = f"{config.get('output.directory', './output')}/qa.{format or 'md'}"
            
            saved_path = generator.save_to_file(qa_items, output, format, "QA Document")
            
            console.print(f"[green]✓[/green] QA document generated: {saved_path}")
            console.print(f"   Encoding: {config.get('output.encoding', 'utf-8')}")
            console.print(f"   Items: {len(qa_items)}")
            
        except Exception as e:
            console.print(f"[red]✗[/red] Error: {str(e)}")


@generate.command('tasks')
@click.argument('input_file', type=click.Path(exists=True))
@click.option('--output', '-o', type=click.Path(), 
              help='Output file path')
@click.option('--format', '-f', 
              type=click.Choice(['json', 'csv', 'md', 'markdown', 'html']),
              help='Output format')
@click.option('--encoding', '-e',
              type=click.Choice(['shift-jis', 'utf-8', 'cp932']),
              help='Output encoding')
@click.pass_context
def generate_tasks(ctx, input_file, output, format, encoding):
    """Generate task list"""
    config = ctx.obj['config']
    model_manager = ctx.obj['model_manager']
    
    # Override encoding if specified
    if encoding:
        config.set('output.encoding', encoding)
    
    if format:
        config.set('output.default_format', format)
    
    generator = TasksGenerator(config, model_manager)
    encoder = EncodingHandler()
    input_text, _ = encoder.read_file_auto(input_file)
    
    with console.status(f"Generating tasks with {model_manager.get_current_model_name()}..."):
        try:
            tasks = generator.generate(input_text)
            
            if not output:
                output = f"{config.get('output.directory', './output')}/tasks.{format or 'md'}"
            
            saved_path = generator.save_to_file(tasks, output, format, "Task List")
            
            console.print(f"[green]✓[/green] Task list generated: {saved_path}")
            console.print(f"   Encoding: {config.get('output.encoding', 'utf-8')}")
            console.print(f"   Tasks: {len(tasks)}")
            
        except Exception as e:
            console.print(f"[red]✗[/red] Error: {str(e)}")


@generate.command('test-concept')
@click.argument('input_file', type=click.Path(exists=True))
@click.option('--output', '-o', type=click.Path(), 
              help='Output file path')
@click.option('--format', '-f', 
              type=click.Choice(['json', 'csv', 'md', 'markdown', 'html']),
              help='Output format')
@click.option('--encoding', '-e',
              type=click.Choice(['shift-jis', 'utf-8', 'cp932']),
              help='Output encoding')
@click.pass_context
def generate_test_concept(ctx, input_file, output, format, encoding):
    """Generate test concept document"""
    config = ctx.obj['config']
    model_manager = ctx.obj['model_manager']
    
    # Override encoding if specified
    if encoding:
        config.set('output.encoding', encoding)
    
    if format:
        config.set('output.default_format', format)
    
    generator = TestConceptGenerator(config, model_manager)
    encoder = EncodingHandler()
    input_text, _ = encoder.read_file_auto(input_file)
    
    with console.status(f"Generating test concept with {model_manager.get_current_model_name()}..."):
        try:
            test_concepts = generator.generate(input_text)
            
            if not output:
                output = f"{config.get('output.directory', './output')}/test_concept.{format or 'md'}"
            
            saved_path = generator.save_to_file(test_concepts, output, format, "Test Concept")
            
            console.print(f"[green]✓[/green] Test concept generated: {saved_path}")
            console.print(f"   Encoding: {config.get('output.encoding', 'utf-8')}")
            console.print(f"   Items: {len(test_concepts)}")
            
        except Exception as e:
            console.print(f"[red]✗[/red] Error: {str(e)}")


@generate.command('test-cases')
@click.argument('input_file', type=click.Path(exists=True))
@click.option('--output', '-o', type=click.Path(), 
              help='Output file path')
@click.option('--format', '-f', 
              type=click.Choice(['json', 'csv', 'md', 'markdown', 'html']),
              help='Output format')
@click.option('--encoding', '-e',
              type=click.Choice(['shift-jis', 'utf-8', 'cp932']),
              help='Output encoding')
@click.pass_context
def generate_test_cases(ctx, input_file, output, format, encoding):
    """Generate test cases"""
    config = ctx.obj['config']
    model_manager = ctx.obj['model_manager']
    
    # Override encoding if specified
    if encoding:
        config.set('output.encoding', encoding)
    
    if format:
        config.set('output.default_format', format)
    
    generator = TestCasesGenerator(config, model_manager)
    encoder = EncodingHandler()
    input_text, _ = encoder.read_file_auto(input_file)
    
    with console.status(f"Generating test cases with {model_manager.get_current_model_name()}..."):
        try:
            test_cases = generator.generate(input_text)
            
            if not output:
                output = f"{config.get('output.directory', './output')}/test_cases.{format or 'md'}"
            
            saved_path = generator.save_to_file(test_cases, output, format, "Test Cases")
            
            console.print(f"[green]✓[/green] Test cases generated: {saved_path}")
            console.print(f"   Encoding: {config.get('output.encoding', 'utf-8')}")
            console.print(f"   Cases: {len(test_cases)}")
            
        except Exception as e:
            console.print(f"[red]✗[/red] Error: {str(e)}")


@cli.group()
@click.pass_context
def config(ctx):
    """Manage configuration"""
    pass


@config.command('show')
@click.pass_context
def config_show(ctx):
    """Show current configuration"""
    config = ctx.obj['config']
    import yaml
    
    console.print("[bold cyan]Current Configuration:[/bold cyan]")
    console.print(yaml.dump(config.get_all(), default_flow_style=False, allow_unicode=True))


@config.command('set')
@click.argument('key')
@click.argument('value')
@click.pass_context
def config_set(ctx, key, value):
    """Set configuration value"""
    config = ctx.obj['config']
    
    # Convert value to appropriate type
    if value.lower() in ['true', 'false']:
        value = value.lower() == 'true'
    elif value.isdigit():
        value = int(value)
    
    config.set(key, value)
    config.save()
    
    console.print(f"[green]✓[/green] Set {key} = {value}")


@cli.group()
@click.pass_context
def analyze(ctx):
    """Analyze files and extract information"""
    pass


@analyze.command('file')
@click.argument('input_file', type=click.Path(exists=True))
@click.option('--output', '-o', type=click.Path(),
              help='Output file path for analysis results')
@click.option('--format', '-f',
              type=click.Choice(['json', 'text', 'md', 'markdown']),
              default='md',
              help='Output format')
@click.option('--extract-text', is_flag=True,
              help='Extract only text content')
@click.pass_context
def analyze_file(ctx, input_file, output, format, extract_text):
    """Analyze various file formats (txt, md, pptx, xlsx, csv, pdf)"""
    from pathlib import Path
    import json
    
    file_path = Path(input_file)
    file_ext = file_path.suffix.lower()
    
    # Select appropriate analyzer
    analyzer = None
    if file_ext in ['.txt', '.md']:
        analyzer = TextAnalyzer()
        analyzer_name = "Text"
    elif file_ext in ['.pptx']:
        analyzer = PPTAnalyzer()
        analyzer_name = "PowerPoint"
    elif file_ext in ['.xlsx', '.xls', '.csv']:
        analyzer = SpreadsheetAnalyzer()
        analyzer_name = "Spreadsheet"
    elif file_ext == '.pdf':
        analyzer = PDFAnalyzer()
        analyzer_name = "PDF"
    else:
        console.print(f"[red]✗[/red] Unsupported file type: {file_ext}")
        console.print("Supported formats: .txt, .md, .pptx, .xlsx, .xls, .csv, .pdf")
        return
    
    with console.status(f"Analyzing {analyzer_name} file..."):
        try:
            if extract_text:
                # Extract text only
                result = analyzer.extract_text(str(file_path))
                console.print(f"[green]✓[/green] Text extracted from {input_file}")
                
                if output:
                    with open(output, 'w', encoding='utf-8') as f:
                        f.write(result)
                    console.print(f"   Saved to: {output}")
                else:
                    console.print("\n" + "=" * 60)
                    console.print(result[:1000])  # Show first 1000 chars
                    if len(result) > 1000:
                        console.print("... (truncated)")
            else:
                # Full analysis
                result = analyzer.analyze(str(file_path))
                console.print(f"[green]✓[/green] {analyzer_name} file analyzed")
                
                # Format output
                if format == 'json':
                    # Custom JSON encoder for numpy types
                    import numpy as np
                    
                    class NumpyEncoder(json.JSONEncoder):
                        def default(self, obj):
                            if isinstance(obj, (np.integer, np.int64)):
                                return int(obj)
                            elif isinstance(obj, (np.floating, np.float64)):
                                return float(obj)
                            elif isinstance(obj, np.ndarray):
                                return obj.tolist()
                            return super().default(obj)
                    
                    output_content = json.dumps(result, ensure_ascii=False, indent=2, cls=NumpyEncoder)
                elif format in ['md', 'markdown']:
                    output_content = _format_analysis_markdown(result, analyzer_name)
                else:  # text
                    output_content = _format_analysis_text(result, analyzer_name)
                
                if output:
                    with open(output, 'w', encoding='utf-8') as f:
                        f.write(output_content)
                    console.print(f"   Saved to: {output}")
                else:
                    console.print("\n" + output_content[:2000])  # Show first 2000 chars
                    if len(output_content) > 2000:
                        console.print("... (truncated)")
                
                # Show statistics
                if 'statistics' in result:
                    console.print("\n[bold]Statistics:[/bold]")
                    for key, value in result['statistics'].items():
                        console.print(f"  {key}: {value}")
                        
        except Exception as e:
            console.print(f"[red]✗[/red] Error: {str(e)}")
            if ctx.obj.get('verbose'):
                import traceback
                traceback.print_exc()


def _format_analysis_markdown(analysis: Dict[str, Any], analyzer_type: str) -> str:
    """Format analysis results as Markdown"""
    lines = [f"# {analyzer_type} Analysis Report\n"]
    
    # File info
    if 'file_info' in analysis:
        lines.append("## File Information")
        for key, value in analysis['file_info'].items():
            lines.append(f"- **{key}**: {value}")
        lines.append("")
    
    # Statistics
    if 'statistics' in analysis:
        lines.append("## Statistics")
        for key, value in analysis['statistics'].items():
            lines.append(f"- **{key}**: {value}")
        lines.append("")
    
    # Summary
    if 'summary' in analysis:
        lines.append("## Summary")
        lines.append(analysis['summary'])
        lines.append("")
    
    # Content preview
    if 'full_text' in analysis:
        lines.append("## Content Preview")
        lines.append("```")
        lines.append(analysis['full_text'][:1000])
        if len(analysis['full_text']) > 1000:
            lines.append("... (truncated)")
        lines.append("```")
    
    return '\n'.join(lines)


def _format_analysis_text(analysis: Dict[str, Any], analyzer_type: str) -> str:
    """Format analysis results as plain text"""
    lines = [f"{analyzer_type} Analysis Report", "=" * 50, ""]
    
    def format_dict(d, indent=0):
        result = []
        for key, value in d.items():
            if isinstance(value, dict):
                result.append(" " * indent + f"{key}:")
                result.extend(format_dict(value, indent + 2))
            elif isinstance(value, list):
                result.append(" " * indent + f"{key}: [{len(value)} items]")
            else:
                result.append(" " * indent + f"{key}: {value}")
        return result
    
    lines.extend(format_dict(analysis))
    return '\n'.join(lines)


if __name__ == '__main__':
    cli()
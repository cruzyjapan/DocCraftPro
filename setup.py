"""Setup script for AI Dev Tool"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8') if (this_directory / "README.md").exists() else ""

setup(
    name="ai-dev-tool",
    version="0.1.0",
    description="AI Dev Tool - System Development Support Tool using Gemini/Claude CLI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="AI Dev Team",
    author_email="dev@example.com",
    url="https://github.com/yourusername/ai-dev-tool",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[
        "click>=8.1.7",
        "python-pptx>=1.0.2",
        "openpyxl>=3.1.5",
        "pandas>=2.2.3",
        "python-docx>=1.1.2",
        "PyPDF2>=3.0.1",
        "markdown>=3.7",
        "chardet>=5.2.0",
        "pydantic>=2.10.3",
        "PyYAML>=6.0.2",
        "python-dotenv>=1.0.1",
        "jsonschema>=4.23.0",
        "rich>=13.9.4",
        "tabulate>=0.9.0",
        "jinja2>=3.1.4",
    ],
    extras_require={
        "dev": [
            "pytest>=8.3.4",
            "pytest-asyncio>=0.24.0",
            "pytest-mock>=3.14.0",
            "black>=24.10.0",
            "ruff>=0.8.2",
            "mypy>=1.13.0",
            "types-PyYAML",
            "types-tabulate",
        ]
    },
    entry_points={
        "console_scripts": [
            "ai-dev=ai_dev.cli:cli",
        ],
    },
    python_requires=">=3.12",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Documentation",
        "Topic :: Software Development :: Quality Assurance",
        "Operating System :: OS Independent",
    ],
    keywords="ai gemini claude cli development documentation generator",
    project_urls={
        "Documentation": "https://github.com/yourusername/ai-dev-tool/wiki",
        "Source": "https://github.com/yourusername/ai-dev-tool",
        "Tracker": "https://github.com/yourusername/ai-dev-tool/issues",
    },
)
# 🎯 Prompt Configuration Management System

프로젝트별 프롬프트를 체계적으로 관리하는 정규화되고 모듈화된 시스템  
A normalized and modular system for managing prompts across projects

## ✨ Features

### 1. **Normalized and Modular Configuration** 
- Structured prompt templates with consistent metadata
- Modular design with clear separation of concerns
- Reusable prompt components with dependency management

### 2. **Flexible Format Support**
- 📄 **YAML** - Human-readable configuration format
- 📋 **JSON** - Machine-parseable structured data
- 📝 **Markdown** - Documentation-friendly format
- 🔄 Easy conversion between formats

### 3. **Visualization**
- 📊 Interactive HTML dashboard with statistics
- 📈 Category and tag distribution charts
- 🔗 Dependency relationship graphs
- 📱 Responsive design for all devices

### 4. **Summation & Analytics**
- 📊 Comprehensive prompt statistics
- 📈 Usage metrics and trends
- 🏷️ Tag and category analysis
- 📝 Automated summary reports

## 🚀 Quick Start

### Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

### Create Example Prompts

```bash
# Generate example prompts in multiple formats
python prompt_config.py
```

This creates:
- `prompts/development/code_review.yaml`
- `prompts/documentation/doc_generator.json`
- `prompts/testing/test_generator.md`

### Generate Visualizations

```bash
# Create HTML dashboard and text summary
python visualize.py
```

This generates:
- `prompt_dashboard.html` - Interactive visualization dashboard
- `prompt_summary.txt` - Text-based summary report

## 📖 Usage Guide

### Creating a Prompt

```python
from prompt_config import PromptTemplate, PromptMetadata, PromptConfig

# Define metadata
metadata = PromptMetadata(
    name="my_prompt",
    description="Description of what this prompt does",
    category="category_name",
    tags=["tag1", "tag2"],
    author="Your Name",
    version="1.0.0"
)

# Create prompt template
prompt = PromptTemplate(
    metadata=metadata,
    template="""Your prompt template here with {variable1} and {variable2}""",
    variables=["variable1", "variable2"],
    examples=[
        {
            "variable1": "example value 1",
            "variable2": "example value 2",
            "description": "Example description"
        }
    ],
    dependencies=[]  # List of other prompts this depends on
)

# Save in your preferred format
config = PromptConfig()
config.save_yaml(prompt, "category/my_prompt.yaml")
config.save_json(prompt, "category/my_prompt.json")
config.save_markdown(prompt, "category/my_prompt.md")
```

### Loading Prompts

```python
from prompt_config import PromptConfig

config = PromptConfig()

# Load all prompts from directory
prompts = config.load_all()

# Load specific prompt
prompt = config.load_yaml("category/my_prompt.yaml")

# Get summary statistics
summary = config.get_summary()
print(f"Total prompts: {summary['total_prompts']}")
print(f"Categories: {summary['categories']}")
```

### Generating Visualizations

```python
from visualize import PromptVisualizer
from prompt_config import PromptConfig

config = PromptConfig()
config.load_all()

visualizer = PromptVisualizer(config)

# Generate HTML dashboard
html_file = visualizer.generate_html_dashboard("dashboard.html")

# Generate text summary
text_summary = visualizer.generate_text_summary()
print(text_summary)
```

## 📁 Project Structure

```
prompt/
├── prompt_config.py      # Core configuration management
├── visualize.py          # Visualization and summation
├── requirements.txt      # Python dependencies
├── README.md            # This file
└── prompts/             # Directory for prompt files
    ├── development/     # Development-related prompts
    ├── documentation/   # Documentation prompts
    └── testing/         # Testing prompts
```

## 🎨 Prompt Template Structure

Each prompt follows a normalized structure:

```yaml
metadata:
  name: prompt_name
  description: What this prompt does
  category: category_name
  tags:
    - tag1
    - tag2
  author: Author Name
  version: 1.0.0
  created_at: 2026-02-05T00:00:00
  updated_at: 2026-02-05T00:00:00

template: |
  Your prompt template here with {variable1}
  and {variable2}

variables:
  - variable1
  - variable2

examples:
  - variable1: example1
    variable2: example2
    description: Example description

dependencies:
  - other_prompt_name
```

## 📊 Visualization Features

The HTML dashboard provides:

- **Statistics Overview**: Total prompts, categories, variables, and examples
- **Category Distribution**: Visual bar charts showing prompt distribution
- **Tag Analysis**: Most commonly used tags and their frequencies
- **Prompt Details**: Comprehensive view of all prompts with metadata
- **Dependency Graph**: Visual representation of prompt relationships

## 🔧 Advanced Features

### Format Conversion

Convert between formats easily:

```python
config = PromptConfig()
prompt = config.load_yaml("source.yaml")
config.save_json(prompt, "output.json")
config.save_markdown(prompt, "output.md")
```

### Dependency Management

Track relationships between prompts:

```python
prompt = PromptTemplate(
    metadata=metadata,
    template="...",
    dependencies=["code_review", "documentation_generator"]
)
```

### Analytics and Summation

Get detailed statistics:

```python
summary = config.get_summary()
print(f"Average variables per prompt: {summary['average_variables_per_prompt']}")
print(f"Average examples per prompt: {summary['average_examples_per_prompt']}")
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

## 📄 License

This project is open source and available under the MIT License.

## 🌟 Example Prompts Included

The system comes with three example prompts to demonstrate capabilities:

1. **Code Review** (`development/code_review.yaml`)
   - Comprehensive code review template
   - Supports multiple programming languages
   - Focuses on quality, security, and performance

2. **Documentation Generator** (`documentation/doc_generator.json`)
   - Automated documentation generation
   - Multiple output formats
   - Includes usage examples

3. **Test Case Generator** (`testing/test_generator.md`)
   - Generates comprehensive test suites
   - Covers edge cases and error handling
   - Framework-agnostic approach

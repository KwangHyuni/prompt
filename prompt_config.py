#!/usr/bin/env python3
"""
Prompt Configuration Management System
Provides normalized and modular configuration for prompts with flexible formats
"""

import json
import yaml
import os
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path


@dataclass
class PromptMetadata:
    """Metadata for a prompt"""
    name: str
    description: str
    category: str
    tags: List[str] = field(default_factory=list)
    author: Optional[str] = None
    version: str = "1.0.0"
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)


@dataclass
class PromptTemplate:
    """Normalized prompt template structure"""
    metadata: PromptMetadata
    template: str
    variables: List[str] = field(default_factory=list)
    examples: List[Dict[str, str]] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        result = {
            'metadata': self.metadata.to_dict(),
            'template': self.template,
            'variables': self.variables,
            'examples': self.examples,
            'dependencies': self.dependencies
        }
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PromptTemplate':
        """Create from dictionary"""
        metadata_dict = data.get('metadata', {})
        metadata = PromptMetadata(**metadata_dict)
        
        return cls(
            metadata=metadata,
            template=data.get('template', ''),
            variables=data.get('variables', []),
            examples=data.get('examples', []),
            dependencies=data.get('dependencies', [])
        )


class PromptConfig:
    """Manages prompt configurations with flexible format support"""
    
    def __init__(self, base_path: str = "./prompts"):
        self.base_path = Path(base_path)
        self.prompts: Dict[str, PromptTemplate] = {}
        
    def save_yaml(self, prompt: PromptTemplate, filename: str) -> str:
        """Save prompt in YAML format"""
        filepath = self.base_path / filename
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            yaml.dump(prompt.to_dict(), f, default_flow_style=False, allow_unicode=True)
        
        return str(filepath)
    
    def save_json(self, prompt: PromptTemplate, filename: str) -> str:
        """Save prompt in JSON format"""
        filepath = self.base_path / filename
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(prompt.to_dict(), f, indent=2, ensure_ascii=False)
        
        return str(filepath)
    
    def save_markdown(self, prompt: PromptTemplate, filename: str) -> str:
        """Save prompt in Markdown format"""
        filepath = self.base_path / filename
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        md_content = self._to_markdown(prompt)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        return str(filepath)
    
    def _to_markdown(self, prompt: PromptTemplate) -> str:
        """Convert prompt to Markdown format"""
        lines = [
            f"# {prompt.metadata.name}",
            "",
            f"**Description:** {prompt.metadata.description}",
            f"**Category:** {prompt.metadata.category}",
            f"**Version:** {prompt.metadata.version}",
            f"**Tags:** {', '.join(prompt.metadata.tags)}",
            ""
        ]
        
        if prompt.metadata.author:
            lines.append(f"**Author:** {prompt.metadata.author}")
            lines.append("")
        
        lines.extend([
            "## Template",
            "",
            "```",
            prompt.template,
            "```",
            ""
        ])
        
        if prompt.variables:
            lines.extend([
                "## Variables",
                ""
            ])
            for var in prompt.variables:
                lines.append(f"- `{var}`")
            lines.append("")
        
        if prompt.examples:
            lines.extend([
                "## Examples",
                ""
            ])
            for i, example in enumerate(prompt.examples, 1):
                lines.append(f"### Example {i}")
                for key, value in example.items():
                    lines.append(f"**{key}:** {value}")
                lines.append("")
        
        if prompt.dependencies:
            lines.extend([
                "## Dependencies",
                ""
            ])
            for dep in prompt.dependencies:
                lines.append(f"- {dep}")
            lines.append("")
        
        return "\n".join(lines)
    
    def load_yaml(self, filename: str) -> PromptTemplate:
        """Load prompt from YAML format"""
        filepath = self.base_path / filename
        
        with open(filepath, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        prompt = PromptTemplate.from_dict(data)
        self.prompts[prompt.metadata.name] = prompt
        return prompt
    
    def load_json(self, filename: str) -> PromptTemplate:
        """Load prompt from JSON format"""
        filepath = self.base_path / filename
        
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        prompt = PromptTemplate.from_dict(data)
        self.prompts[prompt.metadata.name] = prompt
        return prompt
    
    def load_all(self) -> Dict[str, PromptTemplate]:
        """Load all prompts from the base path"""
        if not self.base_path.exists():
            return {}
        
        for filepath in self.base_path.rglob('*'):
            if filepath.is_file():
                try:
                    if filepath.suffix == '.yaml' or filepath.suffix == '.yml':
                        self.load_yaml(filepath.relative_to(self.base_path))
                    elif filepath.suffix == '.json':
                        self.load_json(filepath.relative_to(self.base_path))
                except Exception as e:
                    print(f"Error loading {filepath}: {e}")
        
        return self.prompts
    
    def get_summary(self) -> Dict[str, Any]:
        """Get summary statistics of all prompts"""
        if not self.prompts:
            self.load_all()
        
        categories = {}
        tags = {}
        total_variables = 0
        total_examples = 0
        
        for prompt in self.prompts.values():
            # Count categories
            cat = prompt.metadata.category
            categories[cat] = categories.get(cat, 0) + 1
            
            # Count tags
            for tag in prompt.metadata.tags:
                tags[tag] = tags.get(tag, 0) + 1
            
            # Count variables and examples
            total_variables += len(prompt.variables)
            total_examples += len(prompt.examples)
        
        return {
            'total_prompts': len(self.prompts),
            'categories': categories,
            'tags': tags,
            'total_variables': total_variables,
            'total_examples': total_examples,
            'average_variables_per_prompt': total_variables / len(self.prompts) if self.prompts else 0,
            'average_examples_per_prompt': total_examples / len(self.prompts) if self.prompts else 0
        }


def create_example_prompts():
    """Create example prompts to demonstrate the system"""
    config = PromptConfig()
    
    # Example 1: Code Review Prompt
    code_review = PromptTemplate(
        metadata=PromptMetadata(
            name="code_review",
            description="A prompt for conducting thorough code reviews",
            category="development",
            tags=["code", "review", "quality"],
            author="System",
            version="1.0.0"
        ),
        template="""Please review the following code:

{code}

Focus on:
- Code quality and best practices
- Potential bugs or issues
- Performance considerations
- Security vulnerabilities

Language: {language}
Context: {context}""",
        variables=["code", "language", "context"],
        examples=[
            {
                "language": "Python",
                "context": "Web API endpoint",
                "description": "Review a Flask API endpoint"
            }
        ]
    )
    
    # Example 2: Documentation Generation
    doc_gen = PromptTemplate(
        metadata=PromptMetadata(
            name="documentation_generator",
            description="Generate comprehensive documentation from code",
            category="documentation",
            tags=["docs", "code", "generation"],
            author="System",
            version="1.0.0"
        ),
        template="""Generate documentation for the following {component_type}:

{code}

Include:
- Overview and purpose
- Parameters and return values
- Usage examples
- Edge cases and limitations

Format: {format}""",
        variables=["component_type", "code", "format"],
        examples=[
            {
                "component_type": "function",
                "format": "Markdown",
                "description": "Document a utility function"
            }
        ]
    )
    
    # Example 3: Test Case Generation
    test_gen = PromptTemplate(
        metadata=PromptMetadata(
            name="test_case_generator",
            description="Generate comprehensive test cases",
            category="testing",
            tags=["testing", "qa", "automation"],
            author="System",
            version="1.0.0"
        ),
        template="""Generate test cases for:

{functionality}

Requirements:
- Cover happy path scenarios
- Include edge cases
- Test error handling
- Consider boundary conditions

Framework: {framework}
Coverage target: {coverage}%""",
        variables=["functionality", "framework", "coverage"],
        examples=[
            {
                "framework": "pytest",
                "coverage": "90",
                "description": "Generate tests for a data validation function"
            }
        ],
        dependencies=["code_review"]
    )
    
    # Save in different formats
    config.save_yaml(code_review, "development/code_review.yaml")
    config.save_json(doc_gen, "documentation/doc_generator.json")
    config.save_markdown(test_gen, "testing/test_generator.md")
    
    print("✓ Created example prompts in multiple formats")
    return config


if __name__ == "__main__":
    # Create example prompts
    config = create_example_prompts()
    
    # Load and display summary
    config.load_all()
    summary = config.get_summary()
    
    print("\n📊 Prompt Summary:")
    print(f"Total prompts: {summary['total_prompts']}")
    print(f"Categories: {summary['categories']}")
    print(f"Tags: {summary['tags']}")
    print(f"Average variables per prompt: {summary['average_variables_per_prompt']:.1f}")
    print(f"Average examples per prompt: {summary['average_examples_per_prompt']:.1f}")

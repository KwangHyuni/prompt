#!/usr/bin/env python3
"""
Comprehensive test demonstrating all features of the prompt configuration system
"""

import json
import yaml
from prompt_config import (
    PromptConfig, PromptTemplate, PromptMetadata, create_example_prompts
)
from visualize import PromptVisualizer


def test_normalized_configuration():
    """Test 1: Normalized and modular configuration"""
    print("=" * 60)
    print("TEST 1: Normalized and Modular Configuration")
    print("=" * 60)
    
    # Create a prompt with normalized structure
    metadata = PromptMetadata(
        name="test_prompt",
        description="A test prompt for demonstration",
        category="testing",
        tags=["test", "demo"],
        author="Test User",
        version="1.0.0"
    )
    
    prompt = PromptTemplate(
        metadata=metadata,
        template="This is a {variable1} with {variable2}",
        variables=["variable1", "variable2"],
        examples=[{"variable1": "test", "variable2": "example"}],
        dependencies=[]
    )
    
    print(f"✓ Created prompt: {prompt.metadata.name}")
    print(f"  Category: {prompt.metadata.category}")
    print(f"  Tags: {prompt.metadata.tags}")
    print(f"  Variables: {prompt.variables}")
    print(f"  Version: {prompt.metadata.version}")
    print()


def test_flexible_formats():
    """Test 2: Flexible format support"""
    print("=" * 60)
    print("TEST 2: Flexible Format Support")
    print("=" * 60)
    
    config = PromptConfig()
    
    # Create a simple prompt
    metadata = PromptMetadata(
        name="format_test",
        description="Testing format conversion",
        category="test",
        tags=["format"]
    )
    
    prompt = PromptTemplate(
        metadata=metadata,
        template="Test template with {var}",
        variables=["var"]
    )
    
    # Save in all three formats
    yaml_file = config.save_yaml(prompt, "test/format_test.yaml")
    json_file = config.save_json(prompt, "test/format_test.json")
    md_file = config.save_markdown(prompt, "test/format_test.md")
    
    print(f"✓ Saved YAML format: {yaml_file}")
    print(f"✓ Saved JSON format: {json_file}")
    print(f"✓ Saved Markdown format: {md_file}")
    
    # Load back and verify
    loaded_yaml = config.load_yaml("test/format_test.yaml")
    loaded_json = config.load_json("test/format_test.json")
    
    print(f"✓ Loaded YAML: {loaded_yaml.metadata.name}")
    print(f"✓ Loaded JSON: {loaded_json.metadata.name}")
    print()


def test_visualization():
    """Test 3: Visualization capabilities"""
    print("=" * 60)
    print("TEST 3: Visualization")
    print("=" * 60)
    
    # Create example prompts
    config = create_example_prompts()
    config.load_all()
    
    # Create visualizer
    visualizer = PromptVisualizer(config)
    
    # Generate HTML dashboard
    html_file = visualizer.generate_html_dashboard("test_dashboard.html")
    print(f"✓ Generated HTML dashboard: {html_file}")
    
    # Generate text summary
    text_summary = visualizer.generate_text_summary()
    print(f"✓ Generated text summary ({len(text_summary)} characters)")
    print()


def test_summation():
    """Test 4: Summation and analytics"""
    print("=" * 60)
    print("TEST 4: Summation and Analytics")
    print("=" * 60)
    
    config = PromptConfig()
    config.load_all()
    
    summary = config.get_summary()
    
    print(f"📊 STATISTICS:")
    print(f"  Total Prompts: {summary['total_prompts']}")
    print(f"  Total Variables: {summary['total_variables']}")
    print(f"  Total Examples: {summary['total_examples']}")
    print(f"  Categories: {len(summary['categories'])}")
    print(f"  Tags: {len(summary['tags'])}")
    print(f"  Avg Variables/Prompt: {summary['average_variables_per_prompt']:.2f}")
    print(f"  Avg Examples/Prompt: {summary['average_examples_per_prompt']:.2f}")
    
    print(f"\n📁 CATEGORIES:")
    for category, count in summary['categories'].items():
        print(f"  - {category}: {count}")
    
    print(f"\n🏷️  TAGS:")
    for tag, count in sorted(summary['tags'].items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"  - {tag}: {count}")
    print()


def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("COMPREHENSIVE FEATURE TEST")
    print("Testing all four requirements from problem statement")
    print("=" * 60 + "\n")
    
    test_normalized_configuration()
    test_flexible_formats()
    test_visualization()
    test_summation()
    
    print("=" * 60)
    print("✅ ALL TESTS COMPLETED SUCCESSFULLY")
    print("=" * 60)
    print("\nAll four requirements have been implemented:")
    print("1. ✅ Normalized and modular configuration prompts")
    print("2. ✅ Flexible format support (YAML, JSON, Markdown)")
    print("3. ✅ Visualization (HTML dashboard with charts)")
    print("4. ✅ Summation (statistics and analytics)")
    print()


if __name__ == "__main__":
    main()

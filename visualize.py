#!/usr/bin/env python3
"""
Prompt Visualization Module
Provides visualization capabilities for prompt configurations
"""

import json
from typing import Dict, List, Any
from pathlib import Path
from prompt_config import PromptConfig, PromptTemplate


class PromptVisualizer:
    """Visualizes prompt configurations and relationships"""
    
    def __init__(self, config: PromptConfig):
        self.config = config
    
    def generate_html_dashboard(self, output_file: str = "prompt_dashboard.html") -> str:
        """Generate an HTML dashboard for visualizing prompts"""
        if not self.config.prompts:
            self.config.load_all()
        
        summary = self.config.get_summary()
        
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Prompt Configuration Dashboard</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        
        h1 {{
            color: white;
            text-align: center;
            margin-bottom: 30px;
            font-size: 2.5em;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .stat-card {{
            background: white;
            border-radius: 10px;
            padding: 25px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }}
        
        .stat-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 6px 12px rgba(0,0,0,0.15);
        }}
        
        .stat-number {{
            font-size: 3em;
            font-weight: bold;
            color: #667eea;
            margin-bottom: 10px;
        }}
        
        .stat-label {{
            color: #666;
            font-size: 1.1em;
        }}
        
        .section {{
            background: white;
            border-radius: 10px;
            padding: 25px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        
        .section h2 {{
            color: #333;
            margin-bottom: 20px;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
        }}
        
        .prompt-card {{
            background: #f8f9fa;
            border-left: 4px solid #667eea;
            padding: 15px;
            margin-bottom: 15px;
            border-radius: 5px;
        }}
        
        .prompt-name {{
            font-weight: bold;
            color: #333;
            font-size: 1.2em;
            margin-bottom: 8px;
        }}
        
        .prompt-description {{
            color: #666;
            margin-bottom: 10px;
        }}
        
        .prompt-meta {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-top: 10px;
        }}
        
        .tag {{
            background: #667eea;
            color: white;
            padding: 4px 12px;
            border-radius: 15px;
            font-size: 0.85em;
        }}
        
        .category {{
            background: #764ba2;
            color: white;
            padding: 4px 12px;
            border-radius: 15px;
            font-size: 0.85em;
        }}
        
        .bar-chart {{
            margin-top: 15px;
        }}
        
        .bar {{
            background: #f0f0f0;
            border-radius: 5px;
            margin-bottom: 10px;
            overflow: hidden;
        }}
        
        .bar-label {{
            padding: 8px;
            font-weight: 500;
            color: #333;
        }}
        
        .bar-fill {{
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            height: 30px;
            display: flex;
            align-items: center;
            padding: 0 10px;
            color: white;
            font-weight: bold;
            transition: width 0.5s ease;
        }}
        
        .dependency-graph {{
            margin-top: 20px;
        }}
        
        .dependency-item {{
            background: #f8f9fa;
            padding: 10px;
            margin: 5px 0;
            border-radius: 5px;
            border-left: 3px solid #764ba2;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🎯 Prompt Configuration Dashboard</h1>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-number">{summary['total_prompts']}</div>
                <div class="stat-label">Total Prompts</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{len(summary['categories'])}</div>
                <div class="stat-label">Categories</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{summary['total_variables']}</div>
                <div class="stat-label">Total Variables</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{summary['total_examples']}</div>
                <div class="stat-label">Total Examples</div>
            </div>
        </div>
        
        <div class="section">
            <h2>📊 Categories Distribution</h2>
            <div class="bar-chart">
                {self._generate_category_bars(summary['categories'])}
            </div>
        </div>
        
        <div class="section">
            <h2>🏷️ Tags Distribution</h2>
            <div class="bar-chart">
                {self._generate_tag_bars(summary['tags'])}
            </div>
        </div>
        
        <div class="section">
            <h2>📝 Prompt Details</h2>
            {self._generate_prompt_cards()}
        </div>
        
        <div class="section">
            <h2>🔗 Dependencies</h2>
            <div class="dependency-graph">
                {self._generate_dependency_view()}
            </div>
        </div>
    </div>
    
    <script>
        // Animate bars on load
        window.addEventListener('load', () => {{
            document.querySelectorAll('.bar-fill').forEach(bar => {{
                const width = bar.style.width;
                bar.style.width = '0';
                setTimeout(() => {{
                    bar.style.width = width;
                }}, 100);
            }});
        }});
    </script>
</body>
</html>"""
        
        output_path = Path(output_file)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return str(output_path)
    
    def _generate_category_bars(self, categories: Dict[str, int]) -> str:
        """Generate HTML for category distribution bars"""
        if not categories:
            return "<p>No categories found</p>"
        
        max_count = max(categories.values())
        bars = []
        
        for category, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / max_count) * 100
            bars.append(f"""
                <div class="bar">
                    <div class="bar-label">{category}</div>
                    <div class="bar-fill" style="width: {percentage}%">{count}</div>
                </div>
            """)
        
        return "\n".join(bars)
    
    def _generate_tag_bars(self, tags: Dict[str, int]) -> str:
        """Generate HTML for tag distribution bars"""
        if not tags:
            return "<p>No tags found</p>"
        
        max_count = max(tags.values())
        bars = []
        
        for tag, count in sorted(tags.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / max_count) * 100
            bars.append(f"""
                <div class="bar">
                    <div class="bar-label">{tag}</div>
                    <div class="bar-fill" style="width: {percentage}%">{count}</div>
                </div>
            """)
        
        return "\n".join(bars)
    
    def _generate_prompt_cards(self) -> str:
        """Generate HTML cards for each prompt"""
        if not self.config.prompts:
            return "<p>No prompts found</p>"
        
        cards = []
        for prompt in self.config.prompts.values():
            tags_html = " ".join([f'<span class="tag">{tag}</span>' for tag in prompt.metadata.tags])
            
            card = f"""
                <div class="prompt-card">
                    <div class="prompt-name">{prompt.metadata.name}</div>
                    <div class="prompt-description">{prompt.metadata.description}</div>
                    <div class="prompt-meta">
                        <span class="category">{prompt.metadata.category}</span>
                        {tags_html}
                    </div>
                    <div style="margin-top: 10px; color: #888; font-size: 0.9em;">
                        Variables: {len(prompt.variables)} | Examples: {len(prompt.examples)} | v{prompt.metadata.version}
                    </div>
                </div>
            """
            cards.append(card)
        
        return "\n".join(cards)
    
    def _generate_dependency_view(self) -> str:
        """Generate HTML for dependency relationships"""
        dependencies = []
        has_deps = False
        
        for prompt in self.config.prompts.values():
            if prompt.dependencies:
                has_deps = True
                deps_list = ", ".join(prompt.dependencies)
                dependencies.append(f"""
                    <div class="dependency-item">
                        <strong>{prompt.metadata.name}</strong> depends on: {deps_list}
                    </div>
                """)
        
        if not has_deps:
            return "<p>No dependencies found</p>"
        
        return "\n".join(dependencies)
    
    def generate_text_summary(self) -> str:
        """Generate a text-based summary report"""
        if not self.config.prompts:
            self.config.load_all()
        
        summary = self.config.get_summary()
        
        lines = [
            "=" * 60,
            "PROMPT CONFIGURATION SUMMARY REPORT",
            "=" * 60,
            "",
            f"📊 OVERVIEW",
            f"  Total Prompts: {summary['total_prompts']}",
            f"  Total Variables: {summary['total_variables']}",
            f"  Total Examples: {summary['total_examples']}",
            f"  Avg Variables/Prompt: {summary['average_variables_per_prompt']:.2f}",
            f"  Avg Examples/Prompt: {summary['average_examples_per_prompt']:.2f}",
            "",
            f"📁 CATEGORIES ({len(summary['categories'])})",
        ]
        
        for category, count in sorted(summary['categories'].items(), key=lambda x: x[1], reverse=True):
            lines.append(f"  - {category}: {count}")
        
        lines.extend([
            "",
            f"🏷️  TAGS ({len(summary['tags'])})",
        ])
        
        for tag, count in sorted(summary['tags'].items(), key=lambda x: x[1], reverse=True):
            lines.append(f"  - {tag}: {count}")
        
        lines.extend([
            "",
            f"📝 PROMPT DETAILS",
            ""
        ])
        
        for prompt in self.config.prompts.values():
            lines.extend([
                f"  {prompt.metadata.name}",
                f"    Description: {prompt.metadata.description}",
                f"    Category: {prompt.metadata.category}",
                f"    Tags: {', '.join(prompt.metadata.tags)}",
                f"    Variables: {len(prompt.variables)}",
                f"    Examples: {len(prompt.examples)}",
                f"    Version: {prompt.metadata.version}",
                ""
            ])
        
        lines.append("=" * 60)
        
        return "\n".join(lines)


def main():
    """Main function to demonstrate visualization"""
    from prompt_config import create_example_prompts
    
    # Create example prompts
    config = create_example_prompts()
    config.load_all()
    
    # Create visualizer
    visualizer = PromptVisualizer(config)
    
    # Generate HTML dashboard
    html_file = visualizer.generate_html_dashboard()
    print(f"\n✓ Generated HTML dashboard: {html_file}")
    
    # Generate text summary
    text_summary = visualizer.generate_text_summary()
    print("\n" + text_summary)
    
    # Save text summary
    with open("prompt_summary.txt", "w", encoding="utf-8") as f:
        f.write(text_summary)
    print("\n✓ Generated text summary: prompt_summary.txt")


if __name__ == "__main__":
    main()

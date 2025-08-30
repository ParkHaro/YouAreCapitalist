#!/usr/bin/env python3
"""
Document Creation Tool
======================

Automated tool for creating dual-language documentation pairs with proper
metadata, navigation, and template-based content structure.

Features:
- Creates English + Korean document pairs
- Applies category-specific templates
- Generates metadata headers automatically
- Creates proper navigation links
- Updates parent INDEX files

Usage:
    python doc_create.py --name "document-name" --category architecture

Author: Claude Code Assistant
Created: 2025-08-30
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime
import json
import re
from string import Template

class DocumentCreator:
    """Main document creation class."""
    
    def __init__(self):
        self.script_dir = Path(__file__).parent
        self.claude_root = self.script_dir.parent
        self.doc_root = self.claude_root / "doc"
        self.templates_dir = self.script_dir / "templates"
        
        # Category configurations
        self.categories = {
            "architecture": {
                "title": "Architecture",
                "default_tags": ["unity", "architecture", "system"],
                "template": "architecture_template.md"
            },
            "api": {
                "title": "API",
                "default_tags": ["api", "reference", "documentation"],
                "template": "api_template.md"
            },
            "gamedesign": {
                "title": "Game Design",
                "default_tags": ["gamedesign", "mechanics", "systems"],
                "template": "gamedesign_template.md"
            },
            "guidelines": {
                "title": "Guidelines",
                "default_tags": ["guidelines", "standards", "process"],
                "template": "base_template.md"
            },
            "guides": {
                "title": "Guides",
                "default_tags": ["guides", "tutorial", "howto"],
                "template": "base_template.md"
            },
            "reference": {
                "title": "Reference",
                "default_tags": ["reference", "documentation"],
                "template": "base_template.md"
            }
        }
    
    def create_document(self, name, category="general", priority="medium", tags=None, template=None):
        """
        Create a new document pair (English + Korean).
        
        Args:
            name (str): Document name (will be slugified)
            category (str): Document category
            priority (str): Document priority (high/medium/low)
            tags (list): Additional tags
            template (str): Specific template to use
            
        Returns:
            dict: Created file paths
        """
        # Validate and prepare inputs
        clean_name = self._slugify(name)
        category = category.lower()
        
        if category not in self.categories:
            print(f"⚠️  Unknown category '{category}', using default template")
            category_config = {
                "title": category.title(),
                "default_tags": [category],
                "template": "base_template.md"
            }
        else:
            category_config = self.categories[category]
        
        # Create category directory if it doesn't exist
        category_dir = self.doc_root / category
        category_dir.mkdir(parents=True, exist_ok=True)
        
        # Prepare file paths
        en_file = category_dir / f"{clean_name}.md"
        kr_file = category_dir / f"{clean_name}_KOR.md"
        
        # Check if files already exist
        if en_file.exists() or kr_file.exists():
            response = input(f"Files already exist. Overwrite? (y/N): ")
            if response.lower() != 'y':
                print("❌ Cancelled")
                return None
        
        # Prepare metadata
        current_date = datetime.now().strftime('%Y-%m-%d')
        all_tags = category_config["default_tags"].copy()
        if tags:
            all_tags.extend(tags)
        
        # Load and process template
        template_path = self.templates_dir / (template or category_config["template"])
        if not template_path.exists():
            template_path = self.templates_dir / "base_template.md"
        
        template_content = template_path.read_text(encoding='utf-8')
        
        # Prepare template variables
        title = name.replace('-', ' ').replace('_', ' ').title()
        template_vars = {
            'name': clean_name,
            'title': title,
            'category': category,
            'category_title': category_config["title"],
            'tags': json.dumps(all_tags),
            'related': '[]',
            'created': current_date,
            'updated': current_date,
            'priority': priority
        }
        
        # Generate English content
        en_content = Template(template_content).safe_substitute(template_vars)
        
        # Generate Korean content
        kr_content = self._create_korean_content(
            name=clean_name,
            title=title,
            category=category,
            category_title=category_config["title"]
        )
        
        # Write files
        en_file.write_text(en_content, encoding='utf-8')
        kr_file.write_text(kr_content, encoding='utf-8')
        
        # Update parent INDEX if it exists
        self._update_index_files(category_dir, clean_name, title)
        
        return {
            "english": str(en_file),
            "korean": str(kr_file),
            "category": category,
            "name": clean_name
        }
    
    def _slugify(self, text):
        """Convert text to URL-friendly slug."""
        # Convert to lowercase and replace spaces/underscores with hyphens
        slug = re.sub(r'[_\s]+', '-', text.lower())
        # Remove non-alphanumeric characters except hyphens
        slug = re.sub(r'[^a-z0-9\-]', '', slug)
        # Remove multiple consecutive hyphens
        slug = re.sub(r'-+', '-', slug)
        # Remove leading/trailing hyphens
        slug = slug.strip('-')
        return slug
    
    def _create_korean_content(self, name, title, category, category_title):
        """Create Korean document content."""
        return f"""# {title}

[🇬🇧 English Version](./{name}.md)

## 📍 네비게이션

[↩️ {category_title}로 돌아가기](./INDEX_KOR.md) | [📚 문서 인덱스](../INDEX_KOR.md) | [🏠 홈](../../CLAUDE_KOR.md)

## 개요

이 문서의 목적과 범위에 대한 간단한 설명.

## 내용

주요 내용이 여기에 들어갑니다.

### 섹션 1

섹션 1의 내용.

### 섹션 2

섹션 2의 내용.

## 관련 문서

- [관련 문서 1](./related-doc1_KOR.md) - 간단한 설명
- [관련 문서 2](./related-doc2_KOR.md) - 간단한 설명

## 다음 단계

- 할 일 1
- 할 일 2
"""
    
    def _update_index_files(self, category_dir, doc_name, doc_title):
        """Update INDEX files to include the new document."""
        index_file = category_dir / "INDEX.md"
        index_kr_file = category_dir / "INDEX_KOR.md"
        
        # Update English INDEX
        if index_file.exists():
            content = index_file.read_text(encoding='utf-8')
            
            # Look for a section to add the document
            if "## Documents in This Section" in content:
                # Add to existing section
                new_line = f"- [{doc_title}](./{doc_name}.md) - Brief description"
                
                if new_line not in content:  # Avoid duplicates
                    # Find the section and add the new document
                    lines = content.split('\n')
                    for i, line in enumerate(lines):
                        if line.startswith("## Documents in This Section"):
                            # Find the next section or end of file
                            insert_pos = i + 1
                            
                            # Skip empty lines and existing list items
                            while (insert_pos < len(lines) and 
                                   (not lines[insert_pos].strip() or 
                                    lines[insert_pos].startswith('- ['))):
                                insert_pos += 1
                            
                            # Insert the new document
                            lines.insert(insert_pos, new_line)
                            break
                    
                    updated_content = '\n'.join(lines)
                    index_file.write_text(updated_content, encoding='utf-8')
                    print(f"📝 Updated {index_file}")
        
        # Update Korean INDEX
        if index_kr_file.exists():
            content = index_kr_file.read_text(encoding='utf-8')
            
            if "## 이 섹션의 문서들" in content:
                new_line = f"- [{doc_title}](./{doc_name}_KOR.md) - 간단한 설명"
                
                if new_line not in content:
                    lines = content.split('\n')
                    for i, line in enumerate(lines):
                        if line.startswith("## 이 섹션의 문서들"):
                            insert_pos = i + 1
                            
                            while (insert_pos < len(lines) and 
                                   (not lines[insert_pos].strip() or 
                                    lines[insert_pos].startswith('- ['))):
                                insert_pos += 1
                            
                            lines.insert(insert_pos, new_line)
                            break
                    
                    updated_content = '\n'.join(lines)
                    index_kr_file.write_text(updated_content, encoding='utf-8')
                    print(f"📝 Updated {index_kr_file}")
    
    def list_templates(self):
        """List available templates."""
        templates = []
        if self.templates_dir.exists():
            for template_file in self.templates_dir.glob("*.md"):
                templates.append({
                    "name": template_file.stem,
                    "path": str(template_file),
                    "description": self._get_template_description(template_file)
                })
        return templates
    
    def _get_template_description(self, template_file):
        """Extract description from template file."""
        try:
            content = template_file.read_text(encoding='utf-8')
            lines = content.split('\n')
            for line in lines[:10]:  # Check first 10 lines
                if line.startswith('#') and not line.startswith('#{'):
                    return line.strip('# ').strip()
            return "No description available"
        except:
            return "Unable to read template"


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Create dual-language documentation pairs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python doc_create.py --name "system-integration" --category architecture
  python doc_create.py --name "api-guide" --category api --priority high
  python doc_create.py --name "user-manual" --tags manual guide tutorial
  python doc_create.py --list-templates
        """
    )
    
    parser.add_argument('--name', help='Document name (required)')
    parser.add_argument('--category', default='general', 
                       choices=['architecture', 'api', 'gamedesign', 'guidelines', 'guides', 'reference', 'general'],
                       help='Document category')
    parser.add_argument('--priority', default='medium', 
                       choices=['high', 'medium', 'low'],
                       help='Document priority')
    parser.add_argument('--tags', nargs='*', help='Additional tags')
    parser.add_argument('--template', help='Specific template to use')
    parser.add_argument('--list-templates', action='store_true', 
                       help='List available templates')
    
    args = parser.parse_args()
    
    creator = DocumentCreator()
    
    if args.list_templates:
        templates = creator.list_templates()
        print("📋 Available templates:")
        for template in templates:
            print(f"  - {template['name']}: {template['description']}")
        return 0
    
    if not args.name:
        parser.print_help()
        print("\n❌ Document name is required (use --name)")
        return 1
    
    try:
        result = creator.create_document(
            name=args.name,
            category=args.category,
            priority=args.priority,
            tags=args.tags,
            template=args.template
        )
        
        if result:
            print("✅ Document pair created successfully!")
            print(f"   📄 English: {result['english']}")
            print(f"   📄 Korean:  {result['korean']}")
            print(f"\n💡 Next steps:")
            print(f"   1. Edit the documents to add your content")
            print(f"   2. Run 'python doc_manager.py validate --fix' to ensure quality")
            print(f"   3. Consider adding related documents to metadata")
        
        return 0
        
    except Exception as e:
        print(f"❌ Error creating document: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
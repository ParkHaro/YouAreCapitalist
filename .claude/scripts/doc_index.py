#!/usr/bin/env python3
"""
Documentation Index Manager
===========================

Automatically generates and maintains INDEX.md files for documentation
directories. Scans directories, categorizes documents, and creates
organized indexes with proper navigation and metadata.

Features:
- Auto-generates INDEX.md and INDEX_KOR.md files
- Scans directories recursively
- Categorizes documents by metadata
- Creates hierarchical navigation
- Maintains consistent formatting

Usage:
    python doc_index.py --path ../doc/architecture --update
    python doc_index.py --update-all

Author: Claude Code Assistant
Created: 2025-08-30
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime
import re
import json

class IndexManager:
    """Manages documentation index files."""
    
    def __init__(self):
        self.script_dir = Path(__file__).parent
        self.claude_root = self.script_dir.parent
        self.doc_root = self.claude_root / "doc"
        
        # Category configurations
        self.category_info = {
            "architecture": {
                "title": "Architecture Documentation",
                "description": "System architecture, design patterns, and technical specifications",
                "icon": "🏗️"
            },
            "api": {
                "title": "API Documentation", 
                "description": "API references, endpoints, and integration guides",
                "icon": "🔌"
            },
            "gamedesign": {
                "title": "Game Design Documentation",
                "description": "Game mechanics, systems, and design specifications",
                "icon": "🎮"
            },
            "guidelines": {
                "title": "Development Guidelines",
                "description": "Standards, processes, and best practices",
                "icon": "📋"
            },
            "guides": {
                "title": "User Guides",
                "description": "Tutorials, how-to guides, and user documentation", 
                "icon": "📖"
            },
            "reference": {
                "title": "Reference Documentation",
                "description": "Technical references and lookup materials",
                "icon": "📚"
            }
        }
    
    def update_all_indexes(self):
        """Update all INDEX files in the documentation tree."""
        updated = []
        
        # Update root index
        root_index = self._update_root_index()
        if root_index:
            updated.append(root_index)
        
        # Update category indexes
        for category_dir in self.doc_root.iterdir():
            if category_dir.is_dir() and not category_dir.name.startswith('.'):
                index_files = self.update_index(category_dir)
                if index_files:
                    updated.extend(index_files)
        
        return updated
    
    def update_index(self, directory_path):
        """Update INDEX files for a specific directory."""
        directory_path = Path(directory_path)
        
        if not directory_path.exists() or not directory_path.is_dir():
            raise ValueError(f"Directory does not exist: {directory_path}")
        
        # Scan directory for documents
        documents = self._scan_directory(directory_path)
        
        if not documents:
            print(f"⚠️  No documents found in {directory_path}")
            return []
        
        # Generate INDEX files
        category = directory_path.name
        en_index = directory_path / "INDEX.md"
        kr_index = directory_path / "INDEX_KOR.md"
        
        # Create English INDEX
        en_content = self._generate_english_index(category, documents)
        en_index.write_text(en_content, encoding='utf-8')
        
        # Create Korean INDEX  
        kr_content = self._generate_korean_index(category, documents)
        kr_index.write_text(kr_content, encoding='utf-8')
        
        print(f"✅ Updated indexes for {category}")
        return [str(en_index), str(kr_index)]
    
    def _scan_directory(self, directory):
        """Scan directory for documentation files."""
        documents = []
        
        for md_file in directory.glob("*.md"):
            # Skip INDEX files and Korean versions
            if md_file.name.startswith("INDEX") or "_KOR" in md_file.name:
                continue
            
            doc_info = self._parse_document(md_file)
            if doc_info:
                documents.append(doc_info)
        
        # Sort documents by priority and name
        priority_order = {"high": 0, "medium": 1, "low": 2}
        documents.sort(key=lambda x: (priority_order.get(x.get("priority", "medium"), 1), x["name"]))
        
        return documents
    
    def _parse_document(self, md_file):
        """Parse document metadata and content."""
        try:
            content = md_file.read_text(encoding='utf-8')
            
            # Extract metadata
            metadata = self._extract_metadata(content)
            
            # Extract title (first # heading)
            title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
            title = title_match.group(1) if title_match else md_file.stem.replace('-', ' ').title()
            
            # Extract description (first paragraph after title)
            description = self._extract_description(content)
            
            return {
                "file": md_file.name,
                "name": md_file.stem,
                "title": title,
                "description": description,
                "category": metadata.get("category", "general"),
                "tags": metadata.get("tags", []),
                "priority": metadata.get("priority", "medium"),
                "created": metadata.get("created"),
                "updated": metadata.get("updated")
            }
        except Exception as e:
            print(f"⚠️  Error parsing {md_file}: {e}")
            return None
    
    def _extract_metadata(self, content):
        """Extract YAML front matter metadata."""
        metadata = {}
        
        if content.startswith('---'):
            try:
                # Find the end of front matter
                end_marker = content.find('\n---\n', 3)
                if end_marker > 0:
                    yaml_content = content[3:end_marker]
                    
                    # Simple YAML parsing for our specific format
                    for line in yaml_content.strip().split('\n'):
                        line = line.strip()
                        if ':' in line:
                            key, value = line.split(':', 1)
                            key = key.strip()
                            value = value.strip()
                            
                            # Handle different value types
                            if value.startswith('[') and value.endswith(']'):
                                # List/array
                                value = [item.strip().strip('"\'') for item in value[1:-1].split(',') if item.strip()]
                            elif value.lower() in ('true', 'false'):
                                # Boolean
                                value = value.lower() == 'true'
                            elif value.startswith('"') and value.endswith('"'):
                                # Quoted string
                                value = value[1:-1]
                            
                            metadata[key] = value
            except Exception as e:
                print(f"⚠️  Error parsing metadata: {e}")
        
        return metadata
    
    def _extract_description(self, content):
        """Extract description from document content."""
        lines = content.split('\n')
        
        # Skip metadata and title
        in_metadata = content.startswith('---')
        found_title = False
        
        for line in lines:
            line = line.strip()
            
            # Skip metadata section
            if in_metadata:
                if line == '---' and found_title is False:
                    in_metadata = False
                continue
            
            # Skip title
            if line.startswith('# ') and not found_title:
                found_title = True
                continue
            
            # Skip navigation, Korean version links, empty lines
            if (line.startswith('[🇰🇷') or 
                line.startswith('## 📍') or
                line.startswith('[↩️') or
                not line):
                continue
            
            # Skip section headers initially
            if line.startswith('#'):
                continue
            
            # Found first content paragraph
            if line and not line.startswith('#'):
                # Clean up common patterns
                if len(line) > 20 and not line.startswith('```'):
                    return line[:100] + "..." if len(line) > 100 else line
        
        return "No description available"
    
    def _generate_english_index(self, category, documents):
        """Generate English INDEX.md content."""
        category_config = self.category_info.get(category, {
            "title": category.title() + " Documentation",
            "description": f"Documentation for {category}",
            "icon": "📄"
        })
        
        current_date = datetime.now().strftime('%Y-%m-%d')
        
        content = f"""---
category: {category}
tags: [index, {category}]
related: []
parent: ../INDEX.md
created: {current_date}
updated: {current_date}
priority: high
---

# {category_config['title']}

[🇰🇷 Korean Version](./INDEX_KOR.md)

## 📍 Navigation

[📚 Documentation Index](../INDEX.md) | [🏠 Home](../../CLAUDE.md)

## {category_config['icon']} Overview

{category_config['description']}

## 📋 Documents in This Section

"""
        
        if not documents:
            content += "This category currently has no documents.\n"
        else:
            # Group documents by priority
            high_priority = [d for d in documents if d.get("priority") == "high"]
            medium_priority = [d for d in documents if d.get("priority") == "medium"]
            low_priority = [d for d in documents if d.get("priority") == "low"]
            
            if high_priority:
                content += "### 🔥 High Priority\n\n"
                for doc in high_priority:
                    content += f"- **[{doc['title']}](./{doc['file']})** - {doc['description']}\n"
                content += "\n"
            
            if medium_priority:
                if high_priority:  # Only add header if there are other sections
                    content += "### 📝 General Documentation\n\n"
                for doc in medium_priority:
                    content += f"- [{doc['title']}](./{doc['file']}) - {doc['description']}\n"
                content += "\n"
            
            if low_priority:
                content += "### 📚 Additional Resources\n\n"
                for doc in low_priority:
                    content += f"- [{doc['title']}](./{doc['file']}) - {doc['description']}\n"
                content += "\n"
        
        # Add statistics
        content += f"## 📊 Statistics\n\n"
        content += f"- **Total Documents**: {len(documents)}\n"
        content += f"- **Last Updated**: {current_date}\n"
        
        if documents:
            tag_counts = {}
            for doc in documents:
                for tag in doc.get('tags', []):
                    if isinstance(tag, str):  # Ensure tag is string
                        tag_counts[tag] = tag_counts.get(tag, 0) + 1
            
            if tag_counts:
                content += f"- **Common Tags**: {', '.join(sorted(tag_counts.keys(), key=tag_counts.get, reverse=True)[:5])}\n"
        
        return content
    
    def _generate_korean_index(self, category, documents):
        """Generate Korean INDEX_KOR.md content."""
        category_config = self.category_info.get(category, {
            "title": category.title() + " 문서",
            "description": f"{category}에 대한 문서",
            "icon": "📄"
        })
        
        # Korean translations for titles
        korean_titles = {
            "Architecture Documentation": "아키텍처 문서",
            "API Documentation": "API 문서",
            "Game Design Documentation": "게임 디자인 문서", 
            "Development Guidelines": "개발 가이드라인",
            "User Guides": "사용자 가이드",
            "Reference Documentation": "레퍼런스 문서"
        }
        
        korean_title = korean_titles.get(category_config['title'], category_config['title'])
        
        content = f"""# {korean_title}

[🇬🇧 English Version](./INDEX.md)

## 📍 네비게이션

[📚 문서 인덱스](../INDEX_KOR.md) | [🏠 홈](../../CLAUDE_KOR.md)

## {category_config['icon']} 개요

{category_config['description']}

## 📋 이 섹션의 문서들

"""
        
        if not documents:
            content += "현재 이 카테고리에는 문서가 없습니다.\n"
        else:
            # Group documents by priority 
            high_priority = [d for d in documents if d.get("priority") == "high"]
            medium_priority = [d for d in documents if d.get("priority") == "medium"]
            low_priority = [d for d in documents if d.get("priority") == "low"]
            
            if high_priority:
                content += "### 🔥 우선순위 높음\n\n"
                for doc in high_priority:
                    korean_file = doc['name'] + "_KOR.md"
                    content += f"- **[{doc['title']}](./{korean_file})** - {doc['description']}\n"
                content += "\n"
            
            if medium_priority:
                if high_priority:
                    content += "### 📝 일반 문서\n\n"
                for doc in medium_priority:
                    korean_file = doc['name'] + "_KOR.md"
                    content += f"- [{doc['title']}](./{korean_file}) - {doc['description']}\n"
                content += "\n"
            
            if low_priority:
                content += "### 📚 추가 자료\n\n"
                for doc in low_priority:
                    korean_file = doc['name'] + "_KOR.md"
                    content += f"- [{doc['title']}](./{korean_file}) - {doc['description']}\n"
                content += "\n"
        
        # Add statistics
        current_date = datetime.now().strftime('%Y-%m-%d')
        content += f"## 📊 통계\n\n"
        content += f"- **총 문서 수**: {len(documents)}\n"
        content += f"- **마지막 업데이트**: {current_date}\n"
        
        return content
    
    def _update_root_index(self):
        """Update the main documentation INDEX.md."""
        root_index = self.doc_root / "INDEX.md"
        root_index_kr = self.doc_root / "INDEX_KOR.md"
        
        # Scan for categories
        categories = []
        for category_dir in self.doc_root.iterdir():
            if (category_dir.is_dir() and 
                not category_dir.name.startswith('.') and
                category_dir.name != 'scripts'):
                
                # Count documents in category
                doc_count = len([f for f in category_dir.glob("*.md") 
                               if not f.name.startswith("INDEX") and "_KOR" not in f.name])
                
                categories.append({
                    "name": category_dir.name,
                    "title": self.category_info.get(category_dir.name, {}).get("title", category_dir.name.title()),
                    "description": self.category_info.get(category_dir.name, {}).get("description", ""),
                    "icon": self.category_info.get(category_dir.name, {}).get("icon", "📄"),
                    "doc_count": doc_count
                })
        
        # Generate root INDEX content
        current_date = datetime.now().strftime('%Y-%m-%d')
        
        en_content = f"""---
category: documentation
tags: [index, documentation, root]
related: []
parent: ../CLAUDE.md
created: {current_date}
updated: {current_date}
priority: high
---

# Project Documentation

[🇰🇷 Korean Version](./INDEX_KOR.md)

## 📍 Navigation

[🏠 Home](../CLAUDE.md)

## 📚 Documentation Categories

"""
        
        for category in sorted(categories, key=lambda x: x["doc_count"], reverse=True):
            en_content += f"### {category['icon']} [{category['title']}](./{category['name']}/INDEX.md)\n\n"
            en_content += f"{category['description']}\n\n"
            en_content += f"**Documents**: {category['doc_count']}\n\n"
        
        en_content += f"""## 🔧 Documentation Tools

- [Scripts](../scripts/README.md) - Automation tools for document management
- [Guidelines](./guidelines/INDEX.md) - Documentation standards and processes

## 📊 Overview

- **Total Categories**: {len(categories)}
- **Total Documents**: {sum(c['doc_count'] for c in categories)}
- **Last Updated**: {current_date}
"""
        
        # Korean version
        kr_content = f"""# 프로젝트 문서

[🇬🇧 English Version](./INDEX.md)

## 📍 네비게이션

[🏠 홈](../CLAUDE_KOR.md)

## 📚 문서 카테고리

"""
        
        korean_cat_titles = {
            "Architecture Documentation": "아키텍처 문서",
            "API Documentation": "API 문서", 
            "Game Design Documentation": "게임 디자인 문서",
            "Development Guidelines": "개발 가이드라인",
            "User Guides": "사용자 가이드",
            "Reference Documentation": "레퍼런스 문서"
        }
        
        for category in sorted(categories, key=lambda x: x["doc_count"], reverse=True):
            kr_title = korean_cat_titles.get(category['title'], category['title'])
            kr_content += f"### {category['icon']} [{kr_title}](./{category['name']}/INDEX_KOR.md)\n\n"
            kr_content += f"{category['description']}\n\n"
            kr_content += f"**문서 수**: {category['doc_count']}\n\n"
        
        kr_content += f"""## 🔧 문서 도구

- [스크립트](../scripts/README_KOR.md) - 문서 관리 자동화 도구
- [가이드라인](./guidelines/INDEX_KOR.md) - 문서 표준 및 프로세스

## 📊 개요

- **총 카테고리 수**: {len(categories)}
- **총 문서 수**: {sum(c['doc_count'] for c in categories)}
- **마지막 업데이트**: {current_date}
"""
        
        # Write files
        root_index.write_text(en_content, encoding='utf-8')
        root_index_kr.write_text(kr_content, encoding='utf-8')
        
        print("✅ Updated root documentation index")
        return [str(root_index), str(root_index_kr)]


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Generate and maintain documentation INDEX files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python doc_index.py --path ../doc/architecture --update
  python doc_index.py --update-all
  python doc_index.py --scan-only ../doc/gamedesign
        """
    )
    
    parser.add_argument('--path', help='Specific directory to index')
    parser.add_argument('--update', action='store_true', help='Update INDEX files')
    parser.add_argument('--update-all', action='store_true', help='Update all INDEX files')
    parser.add_argument('--scan-only', action='store_true', help='Scan only, do not update')
    
    args = parser.parse_args()
    
    manager = IndexManager()
    
    try:
        if args.update_all:
            result = manager.update_all_indexes()
            print(f"✅ Updated {len(result)} index files")
        elif args.path:
            if args.scan_only:
                documents = manager._scan_directory(Path(args.path))
                print(f"📋 Found {len(documents)} documents in {args.path}:")
                for doc in documents:
                    print(f"  - {doc['title']} ({doc['priority']})")
            else:
                result = manager.update_index(args.path)
                if result:
                    print("✅ Index updated successfully")
        else:
            parser.print_help()
            return 1
        
        return 0
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Documentation Management Tool
============================

Central CLI tool for managing project documentation with dual-language support.
Automates common documentation tasks to improve efficiency and consistency.

Usage:
    python doc_manager.py [command] [options]

Commands:
    create      Create new document pair (EN + KOR)
    index       Update index files
    validate    Check documentation compliance
    sync        Synchronize language versions
    check       Complete system health check
    fix         Auto-fix common issues

Author: Claude Code Assistant
Created: 2025-08-30
"""

import argparse
import sys
from pathlib import Path
import json
from datetime import datetime
import subprocess

# Add current directory to path for local imports
sys.path.append(str(Path(__file__).parent))

class DocumentationManager:
    """Main documentation management class."""
    
    def __init__(self):
        self.script_dir = Path(__file__).parent
        self.claude_root = self.script_dir.parent
        self.doc_root = self.claude_root / "doc"
        
    def create(self, name, category="general", priority="medium", tags=None):
        """Create new document pair."""
        try:
            from doc_create import DocumentCreator
            creator = DocumentCreator()
            result = creator.create_document(
                name=name,
                category=category,
                priority=priority,
                tags=tags or []
            )
            print(f"✅ Created: {result['english']} + {result['korean']}")
            return True
        except ImportError:
            print("❌ doc_create.py not found. Creating basic files...")
            return self._create_basic(name, category)
    
    def index(self, path=None, update_all=False):
        """Update index files."""
        try:
            from doc_index import IndexManager
            manager = IndexManager()
            if update_all:
                result = manager.update_all_indexes()
                print(f"✅ Updated {len(result)} index files")
            elif path:
                result = manager.update_index(Path(path))
                print(f"✅ Updated index: {result}")
            else:
                print("❌ Specify --path or --update-all")
            return True
        except ImportError:
            print("❌ doc_index.py not found. Creating basic index...")
            return self._create_basic_index(path)
    
    def validate(self, file_path=None, fix=False):
        """Validate documentation."""
        try:
            from doc_validate import DocumentValidator
            validator = DocumentValidator()
            if file_path:
                result = validator.validate_file(Path(file_path), fix=fix)
            else:
                result = validator.validate_all(fix=fix)
            
            print(f"✅ Validation complete:")
            print(f"   - Files checked: {result.get('total', 0)}")
            print(f"   - Issues found: {result.get('issues', 0)}")
            if fix:
                print(f"   - Issues fixed: {result.get('fixed', 0)}")
            return True
        except ImportError:
            print("❌ doc_validate.py not found. Running basic validation...")
            return self._validate_basic()
    
    def sync(self, check_only=False, auto_fix=False):
        """Synchronize language versions."""
        try:
            from doc_sync import LanguageSynchronizer
            synchronizer = LanguageSynchronizer()
            if check_only:
                result = synchronizer.check_sync_status()
                print(f"📊 Sync Status: {result['status']}")
                if result['issues']:
                    for issue in result['issues'][:5]:  # Show first 5
                        print(f"   ⚠️  {issue}")
            elif auto_fix:
                result = synchronizer.auto_sync()
                print(f"✅ Synchronized {result['fixed']} files")
            return True
        except ImportError:
            print("❌ doc_sync.py not found. Running basic sync check...")
            return self._sync_basic()
    
    def check(self):
        """Complete system health check."""
        print("[INFO] Running complete documentation health check...")
        
        health_score = 100
        issues = []
        
        # Check directory structure
        if not self.doc_root.exists():
            issues.append("❌ .claude/doc directory missing")
            health_score -= 30
        else:
            print("[OK] Documentation root exists")
        
        # Check for dual-language files
        total_files = 0
        paired_files = 0
        
        for md_file in self.doc_root.rglob("*.md"):
            if "_KOR" in md_file.name:
                continue
            total_files += 1
            kor_file = md_file.with_name(f"{md_file.stem}_KOR.md")
            if kor_file.exists():
                paired_files += 1
            else:
                issues.append(f"❌ Missing Korean version: {kor_file.name}")
        
        if total_files > 0:
            pair_ratio = (paired_files / total_files) * 100
            print(f"📊 Language pairing: {paired_files}/{total_files} ({pair_ratio:.1f}%)")
            if pair_ratio < 80:
                health_score -= (100 - pair_ratio) * 0.3
        
        # Check for INDEX files
        categories = ["architecture", "api", "gamedesign", "guidelines", "guides", "reference"]
        missing_indexes = []
        
        for category in categories:
            category_dir = self.doc_root / category
            if category_dir.exists():
                index_file = category_dir / "INDEX.md"
                index_kor = category_dir / "INDEX_KOR.md"
                if not index_file.exists():
                    missing_indexes.append(f"{category}/INDEX.md")
                if not index_kor.exists():
                    missing_indexes.append(f"{category}/INDEX_KOR.md")
        
        if missing_indexes:
            for missing in missing_indexes:
                issues.append(f"❌ Missing index: {missing}")
            health_score -= len(missing_indexes) * 5
        
        # Display results
        print(f"\n📈 Documentation Health Score: {health_score:.1f}/100")
        
        if health_score >= 90:
            print("🎉 Excellent! Documentation is in great shape.")
        elif health_score >= 70:
            print("👍 Good! Minor improvements needed.")
        elif health_score >= 50:
            print("⚠️  Fair. Several issues need attention.")
        else:
            print("🚨 Poor. Significant issues found.")
        
        if issues:
            print(f"\n🔧 Issues to address ({len(issues)}):")
            for issue in issues[:10]:  # Show first 10
                print(f"   {issue}")
            if len(issues) > 10:
                print(f"   ... and {len(issues) - 10} more")
        
        return health_score >= 70
    
    def fix(self):
        """Auto-fix common issues."""
        print("🔧 Auto-fixing common documentation issues...")
        
        fixed_count = 0
        
        # Create missing INDEX files
        categories = ["architecture", "api", "gamedesign", "guidelines", "guides", "reference"]
        for category in categories:
            category_dir = self.doc_root / category
            if category_dir.exists():
                index_file = category_dir / "INDEX.md"
                index_kor = category_dir / "INDEX_KOR.md"
                
                if not index_file.exists():
                    self._create_basic_index_file(index_file, category)
                    fixed_count += 1
                
                if not index_kor.exists():
                    self._create_basic_index_file(index_kor, category, korean=True)
                    fixed_count += 1
        
        print(f"✅ Fixed {fixed_count} issues")
        return fixed_count > 0
    
    def _create_basic(self, name, category):
        """Create basic document files when doc_create.py is not available."""
        category_dir = self.doc_root / category
        category_dir.mkdir(parents=True, exist_ok=True)
        
        # Create English file
        en_file = category_dir / f"{name}.md"
        en_content = f"""---
category: {category}
tags: [{category}]
related: []
parent: INDEX.md
created: {datetime.now().strftime('%Y-%m-%d')}
updated: {datetime.now().strftime('%Y-%m-%d')}
priority: medium
---

# {name.replace('-', ' ').title()}

[🇰🇷 Korean Version](./{name}_KOR.md)

## 📍 Navigation

[↩️ Back to {category.title()}](./INDEX.md) | [📚 Documentation Index](../INDEX.md) | [🏠 Home](../../CLAUDE.md)

## Overview

Brief description of {name.replace('-', ' ')}.

## Content

Main content goes here.
"""
        
        # Create Korean file
        kr_file = category_dir / f"{name}_KOR.md"
        kr_content = f"""# {name.replace('-', ' ').title()}

[🇬🇧 English Version](./{name}.md)

## 📍 네비게이션

[↩️ {category.title()}로 돌아가기](./INDEX_KOR.md) | [📚 문서 인덱스](../INDEX_KOR.md) | [🏠 홈](../../CLAUDE_KOR.md)

## 개요

{name.replace('-', ' ')}에 대한 간단한 설명.

## 내용

주요 내용이 여기에 들어갑니다.
"""
        
        en_file.write_text(en_content, encoding='utf-8')
        kr_file.write_text(kr_content, encoding='utf-8')
        
        return {"english": en_file, "korean": kr_file}
    
    def _create_basic_index_file(self, index_path, category, korean=False):
        """Create basic INDEX file."""
        if korean:
            content = f"""# {category.title()} 문서

[🇬🇧 English Version](./INDEX.md)

## 📍 네비게이션

[📚 문서 인덱스](../INDEX_KOR.md) | [🏠 홈](../../CLAUDE_KOR.md)

## 이 섹션의 문서들

현재 이 카테고리에는 문서가 없습니다.
"""
        else:
            content = f"""---
category: {category}
tags: [index, {category}]
related: []
parent: ../INDEX.md
created: {datetime.now().strftime('%Y-%m-%d')}
updated: {datetime.now().strftime('%Y-%m-%d')}
priority: high
---

# {category.title()} Documentation

[🇰🇷 Korean Version](./INDEX_KOR.md)

## 📍 Navigation

[📚 Documentation Index](../INDEX.md) | [🏠 Home](../../CLAUDE.md)

## Documents in This Section

This category currently has no documents.
"""
        
        index_path.write_text(content, encoding='utf-8')
    
    def _create_basic_index(self, path):
        """Create basic index when doc_index.py is not available."""
        if path:
            index_path = Path(path) / "INDEX.md"
            index_kor_path = Path(path) / "INDEX_KOR.md"
            
            category = Path(path).name
            self._create_basic_index_file(index_path, category)
            self._create_basic_index_file(index_kor_path, category, korean=True)
            
            return f"Created basic indexes for {category}"
        return "No path specified"
    
    def _validate_basic(self):
        """Basic validation when doc_validate.py is not available."""
        issues = 0
        total = 0
        
        for md_file in self.doc_root.rglob("*.md"):
            if "_KOR" in md_file.name:
                continue
            total += 1
            
            # Check for Korean pair
            kor_file = md_file.with_name(f"{md_file.stem}_KOR.md")
            if not kor_file.exists():
                print(f"❌ Missing Korean version: {kor_file}")
                issues += 1
            
            # Check for metadata
            content = md_file.read_text(encoding='utf-8')
            if not content.startswith('---'):
                print(f"❌ Missing metadata: {md_file}")
                issues += 1
        
        return {"total": total, "issues": issues}
    
    def _sync_basic(self):
        """Basic sync check when doc_sync.py is not available."""
        issues = []
        
        for md_file in self.doc_root.rglob("*.md"):
            if "_KOR" in md_file.name:
                continue
                
            kor_file = md_file.with_name(f"{md_file.stem}_KOR.md")
            if kor_file.exists():
                # Check modification times
                if md_file.stat().st_mtime > kor_file.stat().st_mtime:
                    issues.append(f"English newer: {md_file.name}")
                elif kor_file.stat().st_mtime > md_file.stat().st_mtime:
                    issues.append(f"Korean newer: {kor_file.name}")
        
        print(f"📊 Found {len(issues)} potential sync issues")
        for issue in issues[:5]:
            print(f"   ⚠️  {issue}")
        
        return len(issues) == 0


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Documentation Management Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python doc_manager.py create "system-design" --category architecture
  python doc_manager.py index --update-all
  python doc_manager.py validate --fix
  python doc_manager.py check
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Create command
    create_parser = subparsers.add_parser('create', help='Create new document pair')
    create_parser.add_argument('name', help='Document name (e.g., "system-design")')
    create_parser.add_argument('--category', default='general', help='Document category')
    create_parser.add_argument('--priority', default='medium', choices=['high', 'medium', 'low'])
    create_parser.add_argument('--tags', nargs='*', help='Additional tags')
    
    # Index command
    index_parser = subparsers.add_parser('index', help='Update index files')
    index_parser.add_argument('--path', help='Specific directory to index')
    index_parser.add_argument('--update-all', action='store_true', help='Update all indexes')
    
    # Validate command
    validate_parser = subparsers.add_parser('validate', help='Validate documentation')
    validate_parser.add_argument('--file', help='Specific file to validate')
    validate_parser.add_argument('--fix', action='store_true', help='Auto-fix issues')
    
    # Sync command
    sync_parser = subparsers.add_parser('sync', help='Synchronize language versions')
    sync_parser.add_argument('--check', action='store_true', help='Check sync status only')
    sync_parser.add_argument('--auto', action='store_true', help='Auto-synchronize')
    
    # Check command
    subparsers.add_parser('check', help='Complete system health check')
    
    # Fix command
    subparsers.add_parser('fix', help='Auto-fix common issues')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    manager = DocumentationManager()
    
    try:
        if args.command == 'create':
            success = manager.create(
                name=args.name,
                category=args.category,
                priority=args.priority,
                tags=args.tags
            )
        elif args.command == 'index':
            success = manager.index(
                path=args.path,
                update_all=args.update_all
            )
        elif args.command == 'validate':
            success = manager.validate(
                file_path=args.file,
                fix=args.fix
            )
        elif args.command == 'sync':
            success = manager.sync(
                check_only=args.check,
                auto_fix=args.auto
            )
        elif args.command == 'check':
            success = manager.check()
        elif args.command == 'fix':
            success = manager.fix()
        else:
            print(f"❌ Unknown command: {args.command}")
            return 1
        
        return 0 if success else 1
        
    except Exception as e:
        print(f"[ERROR] {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
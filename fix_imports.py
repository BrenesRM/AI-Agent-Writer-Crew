#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix missing imports in all Python files
"""

import os
import sys
from pathlib import Path
import re

def fix_imports_in_file(file_path):
    """Fix missing typing imports in a Python file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if file needs typing imports
        needs_dict = 'Dict[' in content and 'from typing import' not in content and 'import typing' not in content
        needs_any = 'Any' in content and 'from typing import' not in content and 'import typing' not in content
        needs_list = 'List[' in content and 'from typing import' not in content and 'import typing' not in content
        needs_optional = 'Optional[' in content and 'from typing import' not in content and 'import typing' not in content
        
        if not (needs_dict or needs_any or needs_list or needs_optional):
            return False  # No changes needed
        
        # Determine what imports are needed
        imports_needed = []
        if needs_dict:
            imports_needed.append('Dict')
        if needs_any:
            imports_needed.append('Any')
        if needs_list:
            imports_needed.append('List')
        if needs_optional:
            imports_needed.append('Optional')
        
        # Check if there's already a typing import we can extend
        typing_import_pattern = r'from typing import ([^\n]+)'
        match = re.search(typing_import_pattern, content)
        
        if match:
            # Extend existing import
            existing_imports = [imp.strip() for imp in match.group(1).split(',')]
            new_imports = list(set(existing_imports + imports_needed))
            new_import_line = f"from typing import {', '.join(sorted(new_imports))}"
            content = re.sub(typing_import_pattern, new_import_line, content)
        else:
            # Add new import after encoding declaration and before other imports
            lines = content.split('\n')
            insert_index = 0
            
            # Find the right place to insert the import
            for i, line in enumerate(lines):
                if line.startswith('# -*- coding:') or line.startswith('# coding:') or line.startswith('#!'):
                    insert_index = i + 1
                elif line.startswith('from ') or line.startswith('import '):
                    insert_index = i
                    break
            
            # Insert the typing import
            import_line = f"from typing import {', '.join(sorted(imports_needed))}"
            lines.insert(insert_index, import_line)
            content = '\n'.join(lines)
        
        # Write the fixed content back
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Fixed imports in {file_path.relative_to(Path.cwd())}")
        return True
        
    except Exception as e:
        print(f"❌ Error fixing {file_path}: {e}")
        return False

def main():
    """Fix imports in all Python files"""
    print("🔧 Fixing missing typing imports...\n")
    
    project_root = Path(__file__).parent
    
    # Find all Python files
    python_files = []
    for pattern in ['**/*.py']:
        python_files.extend(project_root.glob(pattern))
    
    fixed_files = 0
    total_files = 0
    
    for file_path in python_files:
        # Skip __pycache__ and .pyc files
        if '__pycache__' in str(file_path) or file_path.suffix == '.pyc':
            continue
            
        total_files += 1
        if fix_imports_in_file(file_path):
            fixed_files += 1
    
    print(f"\n🎯 IMPORT FIX SUMMARY")
    print(f"✅ Files fixed: {fixed_files}")
    print(f"📊 Files checked: {total_files}")
    print(f"🚀 Ready to rebuild!")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comprehensive encoding fix script for all Python files
"""

import os
import sys
from pathlib import Path
import subprocess

def fix_file_encoding(file_path):
    """Fix encoding issues in a Python file"""
    try:
        # Try to read with different encodings
        content = None
        original_encoding = None
        
        for encoding in ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    content = f.read()
                original_encoding = encoding
                break
            except UnicodeDecodeError:
                continue
        
        if content is None:
            print(f"❌ Could not read {file_path} with any encoding")
            return False
        
        # Fix common problematic characters
        replacements = {
            'ñ': 'ñ',  # Fix ñ character
            'a': 'a',  # Replace accented characters with non-accented
            'e': 'e',
            'i': 'i', 
            'o': 'o',
            'u': 'u',
            'u': 'u',
            'Ñ': 'Ñ',
            'A': 'A',
            'E': 'E',
            'I': 'I',
            'O': 'O',
            'U': 'U'
        }
        
        # Apply replacements for safer characters
        for old, new in replacements.items():
            if old in content and old != new:  # Only replace if different
                content = content.replace(old, new)
        
        # Ensure UTF-8 encoding declaration at the top
        if not content.startswith('# -*- coding: utf-8 -*-'):
            # Check if there's already an encoding declaration
            lines = content.split('\n')
            encoding_line_found = False
            
            for i, line in enumerate(lines[:3]):  # Check first 3 lines
                if 'coding:' in line or 'coding=' in line:
                    lines[i] = '# -*- coding: utf-8 -*-'
                    encoding_line_found = True
                    break
            
            if not encoding_line_found:
                # Add encoding declaration at the top
                if lines[0].startswith('#!'):
                    # If shebang exists, add after it
                    lines.insert(1, '# -*- coding: utf-8 -*-')
                else:
                    lines.insert(0, '# -*- coding: utf-8 -*-')
            
            content = '\n'.join(lines)
        
        # Write back as UTF-8
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        if original_encoding != 'utf-8':
            print(f"✅ Fixed {file_path} (was {original_encoding}, now utf-8)")
        else:
            print(f"✅ Verified {file_path} (already utf-8)")
        return True
        
    except Exception as e:
        print(f"❌ Error fixing {file_path}: {e}")
        return False

def main():
    """Fix encoding for all Python files in the project"""
    print("🔧 Starting comprehensive encoding fix...\n")
    
    # Get project root
    project_root = Path(__file__).parent
    
    # Find all Python files
    python_files = []
    for pattern in ['**/*.py']:
        python_files.extend(project_root.glob(pattern))
    
    print(f"📁 Found {len(python_files)} Python files to check\n")
    
    fixed_files = 0
    failed_files = 0
    
    for file_path in python_files:
        # Skip __pycache__ and .pyc files
        if '__pycache__' in str(file_path) or file_path.suffix == '.pyc':
            continue
            
        print(f"🔍 Checking {file_path.relative_to(project_root)}...")
        
        if fix_file_encoding(file_path):
            fixed_files += 1
        else:
            failed_files += 1
    
    print(f"\n{'='*60}")
    print("🎯 ENCODING FIX SUMMARY")
    print('='*60)
    print(f"✅ Successfully processed: {fixed_files}")
    print(f"❌ Failed to process: {failed_files}")
    print(f"📊 Total files: {fixed_files + failed_files}")
    
    if failed_files == 0:
        print("\n🎉 All Python files have been processed successfully!")
        print("🚀 Ready to rebuild Docker containers")
    else:
        print(f"\n⚠️  {failed_files} files could not be processed")
        print("Please check these files manually")

if __name__ == "__main__":
    main()

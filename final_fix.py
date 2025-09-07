#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comprehensive fix for all remaining issues
"""

import subprocess
import sys
import os
from pathlib import Path

def run_fix_script(script_name, description):
    """Run a fix script and report results"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run([sys.executable, script_name], 
                              capture_output=True, text=True, cwd=Path(__file__).parent)
        
        if result.returncode == 0:
            print(f"✅ {description} completed successfully")
            return True
        else:
            print(f"❌ {description} failed")
            if result.stderr:
                print(f"   Error: {result.stderr[:200]}...")
            return False
    except Exception as e:
        print(f"❌ {description} failed: {e}")
        return False

def fix_docker_restart():
    """Fix and restart Docker containers"""
    print("🔧 Rebuilding Docker containers...")
    
    commands = [
        ("docker-compose down", "Stopping containers"),
        ("docker-compose build --no-cache", "Rebuilding images"),
    ]
    
    for cmd, desc in commands:
        print(f"   {desc}...")
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"   ✅ {desc} completed")
            else:
                print(f"   ❌ {desc} failed: {result.stderr[:100]}...")
                return False
        except Exception as e:
            print(f"   ❌ {desc} failed: {e}")
            return False
    
    return True

def main():
    """Run comprehensive fixes"""
    print("🚀 COMPREHENSIVE FIX SCRIPT")
    print("="*50)
    
    # Change to project directory
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    fixes = [
        ("fix_encoding.py", "Encoding fixes"),
        ("fix_imports.py", "Import fixes"),
    ]
    
    print("Step 1: Applying code fixes")
    all_fixes_successful = True
    
    for script, description in fixes:
        if not run_fix_script(script, description):
            all_fixes_successful = False
    
    if all_fixes_successful:
        print("\nStep 2: Rebuilding Docker")
        if fix_docker_restart():
            print("\n🎉 ALL FIXES APPLIED SUCCESSFULLY!")
            print("\nTo test the system, run:")
            print("   docker-compose up")
            print("\nExpected results:")
            print("   ✅ 6/6 tests should pass")
            print("   ✅ Streamlit at http://localhost:8501")
            print("   ✅ No encoding or import errors")
        else:
            print("\n❌ Docker rebuild failed")
    else:
        print("\n❌ Some fixes failed. Please review the errors above.")

if __name__ == "__main__":
    main()

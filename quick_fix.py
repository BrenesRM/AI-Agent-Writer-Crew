#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quick test and rebuild script
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description, check=True):
    """Run a command and handle output"""
    print(f"🔧 {description}...")
    try:
        if isinstance(command, list):
            result = subprocess.run(command, capture_output=True, text=True, check=check)
        else:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, check=check)
        
        if result.returncode == 0:
            print(f"✅ {description} completed")
            if result.stdout.strip():
                print(f"   Output: {result.stdout.strip()[:200]}...")
            return True
        else:
            print(f"❌ {description} failed")
            if result.stderr:
                print(f"   Error: {result.stderr.strip()[:200]}...")
            return False
    except Exception as e:
        print(f"❌ {description} failed: {e}")
        return False

def main():
    print("🚀 Quick fix and test script\n")
    
    # Change to project directory
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # Step 1: Fix encoding
    print("Step 1: Fixing file encodings")
    if run_command([sys.executable, "fix_encoding.py"], "Encoding fixes"):
        print("✅ Encoding fixes applied")
    
    # Step 2: Clean Docker
    print("\nStep 2: Cleaning Docker environment")
    run_command("docker-compose down", "Stopping containers", check=False)
    
    # Step 3: Rebuild
    print("\nStep 3: Rebuilding Docker images")
    if run_command("docker-compose build --no-cache", "Building containers"):
        print("✅ Docker rebuild successful")
        
        # Step 4: Test
        print("\nStep 4: Running test")
        print("Starting containers...")
        print("="*60)
        
        # Run in interactive mode to see output
        os.system("docker-compose up")
        
    else:
        print("❌ Docker rebuild failed")
        print("Please check the errors above")

if __name__ == "__main__":
    main()

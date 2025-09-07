#!/usr/bin/env python3
"""
Final fix and test script
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(cmd, description):
    """Run a command and return success status"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completed")
            return True
        else:
            print(f"❌ {description} failed: {result.stderr[:100]}...")
            return False
    except Exception as e:
        print(f"❌ {description} error: {e}")
        return False

def main():
    print("🚀 Final Fix - Individual Tools Test")
    print("="*50)
    
    # Change to project directory
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    print("\nStep 1: Rebuilding Docker containers...")
    if run_command("docker-compose build --no-cache", "Docker rebuild"):
        print("\nStep 2: Running tests...")
        print("Expected result: 6/6 tests should now pass!")
        print("\n" + "="*50)
        
        # Run the tests
        os.system("docker-compose up agent-test")
    else:
        print("❌ Docker rebuild failed")

if __name__ == "__main__":
    main()

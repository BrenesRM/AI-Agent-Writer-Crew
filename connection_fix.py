#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI Agent Writer Crew - Connection Fix Script
===========================================

This script fixes the connection issue where the application was trying
to connect to 0.0.0.0:8501 instead of localhost:8501.

Author: Claude AI Assistant
Date: September 2025
"""

import os
import subprocess
import time
import sys
import requests
from pathlib import Path

class ConnectionFixer:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.compose_file = self.project_root / "docker-compose.yml"
        self.frontend_dir = self.project_root / "frontend"
        
    def print_status(self, message, status="INFO"):
        """Print colored status messages"""
        colors = {
            "INFO": "\033[94m",     # Blue
            "SUCCESS": "\033[92m",  # Green
            "WARNING": "\033[93m",  # Yellow
            "ERROR": "\033[91m",    # Red
            "RESET": "\033[0m"      # Reset
        }
        
        icons = {
            "INFO": "ℹ️",
            "SUCCESS": "✅",
            "WARNING": "⚠️",
            "ERROR": "❌"
        }
        
        print(f"{colors.get(status, '')}{icons.get(status, '')} {message}{colors['RESET']}")
    
    def check_docker_running(self):
        """Check if Docker is running"""
        try:
            result = subprocess.run(['docker', 'info'], 
                                  capture_output=True, text=True)
            return result.returncode == 0
        except FileNotFoundError:
            return False
    
    def stop_containers(self):
        """Stop all containers"""
        self.print_status("Stopping existing containers...")
        try:
            subprocess.run(['docker-compose', 'down'], 
                         cwd=self.project_root, capture_output=True)
            self.print_status("Containers stopped", "SUCCESS")
            return True
        except Exception as e:
            self.print_status(f"Error stopping containers: {e}", "ERROR")
            return False
    
    def build_containers(self):
        """Build containers"""
        self.print_status("Building containers...")
        try:
            result = subprocess.run(['docker-compose', 'build'], 
                                  cwd=self.project_root, 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                self.print_status("Containers built successfully", "SUCCESS")
                return True
            else:
                self.print_status(f"Build failed: {result.stderr}", "ERROR")
                return False
        except Exception as e:
            self.print_status(f"Error building containers: {e}", "ERROR")
            return False
    
    def start_containers(self):
        """Start containers in detached mode"""
        self.print_status("Starting containers...")
        try:
            result = subprocess.run(['docker-compose', 'up', '-d'], 
                                  cwd=self.project_root,
                                  capture_output=True, text=True)
            if result.returncode == 0:
                self.print_status("Containers started successfully", "SUCCESS")
                return True
            else:
                self.print_status(f"Start failed: {result.stderr}", "ERROR")
                return False
        except Exception as e:
            self.print_status(f"Error starting containers: {e}", "ERROR")
            return False
    
    def check_container_status(self):
        """Check the status of containers"""
        try:
            result = subprocess.run(['docker-compose', 'ps'], 
                                  cwd=self.project_root,
                                  capture_output=True, text=True)
            self.print_status("Container Status:")
            print(result.stdout)
            return True
        except Exception as e:
            self.print_status(f"Error checking container status: {e}", "ERROR")
            return False
    
    def wait_for_streamlit(self, timeout=60):
        """Wait for Streamlit to be ready"""
        self.print_status(f"Waiting for Streamlit to start (timeout: {timeout}s)...")
        
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                response = requests.get('http://localhost:8501', timeout=5)
                if response.status_code == 200:
                    self.print_status("Streamlit is ready!", "SUCCESS")
                    return True
            except requests.exceptions.RequestException:
                pass
            
            print(".", end="", flush=True)
            time.sleep(2)
        
        print()  # New line after dots
        self.print_status("Streamlit did not start within timeout period", "WARNING")
        return False
    
    def show_logs(self, service="frontend-streamlit", lines=20):
        """Show logs for a specific service"""
        try:
            result = subprocess.run(['docker-compose', 'logs', '--tail', str(lines), service], 
                                  cwd=self.project_root,
                                  capture_output=True, text=True)
            self.print_status(f"Last {lines} lines of {service} logs:")
            print(result.stdout)
        except Exception as e:
            self.print_status(f"Error getting logs: {e}", "ERROR")
    
    def test_connection(self):
        """Test connection to various endpoints"""
        endpoints = [
            "http://localhost:8501",
            "http://127.0.0.1:8501",
        ]
        
        self.print_status("Testing connection endpoints...")
        
        for endpoint in endpoints:
            try:
                response = requests.get(endpoint, timeout=5)
                if response.status_code == 200:
                    self.print_status(f"✅ {endpoint} - Working", "SUCCESS")
                else:
                    self.print_status(f"⚠️ {endpoint} - Status: {response.status_code}", "WARNING")
            except requests.exceptions.RequestException as e:
                self.print_status(f"❌ {endpoint} - Failed: {str(e)[:50]}...", "ERROR")
    
    def create_desktop_shortcut(self):
        """Create a desktop shortcut (Windows only)"""
        if sys.platform.startswith('win'):
            try:
                import winshell
                from win32com.client import Dispatch
                
                desktop = winshell.desktop()
                shortcut_path = os.path.join(desktop, "AI Agent Writer Crew.lnk")
                
                shell = Dispatch('WScript.Shell')
                shortcut = shell.CreateShortCut(shortcut_path)
                shortcut.Targetpath = "http://localhost:8501"
                shortcut.IconLocation = str(self.project_root / "frontend" / "index.html")
                shortcut.save()
                
                self.print_status("Desktop shortcut created", "SUCCESS")
            except ImportError:
                self.print_status("Cannot create shortcut (missing dependencies)", "WARNING")
            except Exception as e:
                self.print_status(f"Error creating shortcut: {e}", "WARNING")
    
    def fix_connection_issue(self):
        """Main method to fix the connection issue"""
        self.print_status("🚀 AI Agent Writer Crew - Connection Fix", "INFO")
        self.print_status("=" * 50, "INFO")
        
        # Check Docker
        if not self.check_docker_running():
            self.print_status("Docker is not running! Please start Docker Desktop.", "ERROR")
            return False
        
        self.print_status("Docker is running", "SUCCESS")
        
        # Stop existing containers
        self.stop_containers()
        
        # Build containers
        if not self.build_containers():
            return False
        
        # Start containers
        if not self.start_containers():
            return False
        
        # Wait a bit for services to initialize
        self.print_status("Waiting for services to initialize...")
        time.sleep(10)
        
        # Check container status
        self.check_container_status()
        
        # Wait for Streamlit
        streamlit_ready = self.wait_for_streamlit()
        
        if not streamlit_ready:
            self.print_status("Showing recent logs for troubleshooting:", "WARNING")
            self.show_logs()
        
        # Test connections
        self.test_connection()
        
        # Final status
        self.print_status("=" * 50, "INFO")
        if streamlit_ready:
            self.print_status("🎉 Fix completed successfully!", "SUCCESS")
            self.print_status("🌐 Access your app at: http://localhost:8501", "SUCCESS")
            
            # Create desktop shortcut
            self.create_desktop_shortcut()
            
            # Ask to open browser
            try:
                open_browser = input("\n🌐 Would you like to open the browser now? (y/N): ").lower().strip()
                if open_browser in ['y', 'yes']:
                    import webbrowser
                    webbrowser.open('http://localhost:8501')
                    self.print_status("Browser opened", "SUCCESS")
            except KeyboardInterrupt:
                print("\nSkipping browser open.")
        
        else:
            self.print_status("⚠️ Fix completed with warnings", "WARNING")
            self.print_status("Try manually accessing: http://localhost:8501", "INFO")
            self.print_status("Or check logs: docker-compose logs frontend-streamlit", "INFO")
        
        return streamlit_ready
    
    def quick_restart(self):
        """Quick restart of just the frontend container"""
        self.print_status("🔄 Quick restart of frontend container", "INFO")
        
        try:
            # Restart the frontend container
            subprocess.run(['docker-compose', 'restart', 'frontend-streamlit'], 
                         cwd=self.project_root, check=True)
            
            self.print_status("Frontend container restarted", "SUCCESS")
            
            # Wait for it to be ready
            if self.wait_for_streamlit(timeout=30):
                self.print_status("🎉 Quick restart successful!", "SUCCESS")
                return True
            else:
                self.print_status("Frontend may need more time to start", "WARNING")
                return False
                
        except subprocess.CalledProcessError as e:
            self.print_status(f"Error during restart: {e}", "ERROR")
            return False


def main():
    """Main function"""
    fixer = ConnectionFixer()
    
    # Check command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "--quick":
            fixer.quick_restart()
        elif sys.argv[1] == "--status":
            fixer.check_container_status()
            fixer.test_connection()
        elif sys.argv[1] == "--logs":
            fixer.show_logs(lines=50)
        else:
            print("Usage:")
            print("  python connection_fix.py          # Full fix")
            print("  python connection_fix.py --quick  # Quick restart")
            print("  python connection_fix.py --status # Check status")
            print("  python connection_fix.py --logs   # Show logs")
    else:
        # Full fix
        success = fixer.fix_connection_issue()
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Push MarsPro project to GitHub
Helper script for manual git push process
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return None

def main():
    """Main function to push project to GitHub"""
    
    print("🚀 MarsPro GitHub Push Helper")
    print("=" * 40)
    
    # Check if we're in a git repository
    if not Path(".git").exists():
        print("❌ Not in a git repository. Please run 'git init' first.")
        return
    
    # Check git status
    status_output = run_command("git status --porcelain", "Checking git status")
    if status_output is None:
        return
    
    if status_output.strip():
        print("⚠️  There are uncommitted changes. Please commit them first.")
        print("Run: git add . && git commit -m 'Your commit message'")
        return
    
    # Check if remote is configured
    remote_output = run_command("git remote -v", "Checking remote configuration")
    if remote_output is None:
        return
    
    if "origin" not in remote_output:
        print("❌ No origin remote configured.")
        print("Please add your GitHub repository as origin:")
        print("git remote add origin https://github.com/YOUR_USERNAME/marspro-analysis.git")
        return
    
    # Check current branch
    branch_output = run_command("git branch --show-current", "Checking current branch")
    if branch_output is None:
        return
    
    current_branch = branch_output.strip()
    print(f"📋 Current branch: {current_branch}")
    
    # Push to GitHub
    print(f"\n📤 Pushing to GitHub...")
    print("This will push your code to the origin remote.")
    
    # Ask for confirmation
    response = input("Do you want to continue? (y/N): ").strip().lower()
    if response not in ['y', 'yes']:
        print("❌ Push cancelled.")
        return
    
    # Push the code
    push_output = run_command(f"git push -u origin {current_branch}", "Pushing to GitHub")
    if push_output is None:
        return
    
    print("\n🎉 Successfully pushed to GitHub!")
    print("\n📋 Next steps:")
    print("1. Go to your GitHub repository")
    print("2. Set up repository topics: home-assistant, reverse-engineering, ble, iot, smart-home, python")
    print("3. Create a release using the GitHub web interface")
    print("4. Set up GitHub Pages if desired")
    print("5. Share your repository with the community!")

if __name__ == "__main__":
    main() 
import os
import sys
import subprocess

# Force UTF-8 output for Windows terminals
sys.stdout.reconfigure(encoding='utf-8')

readme_content = """---
title: StyleSync AI AI AI AI AI
emoji: 🚀
colorFrom: blue
colorTo: indigo
sdk: docker
pinned: false
---
# StyleSync AI AI AI AI AI
An AI-powered merchandising agent.
"""

def run_command(command):
    print(f"Running: {command}")
    try:
        subprocess.run(command, check=True, shell=True)
        print("✅ Success")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        # Don't exit, try to continue or let user see error

def fix_readme():
    print("Writing README.md...")
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)
    print("✅ Created README.md")

    print("Deploying changes...")
    run_command("git add README.md")
    run_command('git commit -m "Add Hugging Face configuration"')
    run_command("git push space clean_deploy:main")
    print("✅ Configuration fixed and pushed!")

if __name__ == "__main__":
    fix_readme()

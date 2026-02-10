import subprocess
import shutil
import sys
import os

def run_command(command, step_name):
    """Executes a shell command with error handling."""
    print(f"🔄 {step_name}...")
    try:
        subprocess.run(command, shell=True, check=True)
        print(f"✅ {step_name} complete.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error during {step_name}.")
        print(f"Command failed: {command}")
        # We don't exit immediately for all errors (e.g. repo already exists), 
        # but for this script's flow, most steps are critical.
        if "commit" in command:
            print("(Proceeding, maybe nothing to commit)")
        elif "repo create" in command:
            print("(Proceeding, repository might already exist)")
        else:
            sys.exit(1)

def main():
    # 1. Check for GitHub CLI
    if not shutil.which("gh"):
        print("❌ GitHub CLI not found. Please install it or create the repo manually at github.com/new")
        sys.exit(1)

    # 2. Initialize Git
    # Only init if not already a git repo
    if not os.path.exists(".git"):
        run_command("git init", "Initialize Git")
    else:
        print("ℹ️  Git already initialized.")

    # 3. Add all files
    run_command("git add .", "Stage all files")

    # 4. Commit
    run_command('git commit -m "Initial launch: StyleSync AI AI AI AI AI Enterprise Edition"', "Commit files")

    # 5. Create GitHub Repo
    # We ignore error here if it fails assuming it might exist, or let the user see the gh output
    run_command("gh repo create StyleSync AI AI AI AI-AI --public --source=. --remote=origin", "Create GitHub Repo")

    # 6. Push to origin
    run_command("git push -u origin main", "Push to GitHub")

    print("\n🎉 Project successfully pushed to GitHub!")

if __name__ == "__main__":
    main()

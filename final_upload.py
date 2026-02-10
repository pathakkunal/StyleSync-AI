import subprocess
import sys

def run_command(command, check=True):
    try:
        subprocess.run(command, check=check, shell=True, text=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing currently: {command}")
        # We don't exit here because some commands like 'remote remove' might fail meaningfully but we want to continue, 
        # or we handle them specifically in the main flow.
        if check:
            # Re-raise if we strictly wanted this to succeed
            raise e

def main():
    # Input: Ask the user for the GitHub URL
    if len(sys.argv) > 1:
        github_url = sys.argv[1].strip()
    else:
        github_url = input('Please paste your GitHub URL here: ').strip()
    
    if not github_url:
        print("Error: No URL provided.")
        return

    try:
        # Git Commands sequence
        print("Initializing git...")
        run_command("git init")
        
        print("Adding files...")
        run_command("git add .")
        
        print("Committing files...")
        try:
            # Use check=True so it raises exception on failure, which we catch
            run_command('git commit -m "Initial commit - StyleSync AI AI AI AI AI"', check=True)
        except subprocess.CalledProcessError:
            print("Commit failed (likely nothing to commit). Continuing...")

        print("Renaming branch to main...")
        run_command("git branch -M main")
        
        print("Removing existing origin (if any)...")
        # Don't check=True here because it fails if origin doesn't exist
        run_command("git remote remove origin", check=False)
        
        print(f"Adding remote origin: {github_url}")
        run_command(f"git remote add origin {github_url}")
        
        print("Pushing to GitHub...")
        run_command("git push -u origin main")
        
        # Success message
        print('✅ Code is live on GitHub!')
        
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")

if __name__ == "__main__":
    main()

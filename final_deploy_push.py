import subprocess
import sys

# Force UTF-8 output for Windows terminals
sys.stdout.reconfigure(encoding='utf-8')

def deploy():
    print("⚠️  Ensure you are inside the D:\\Projects\\StyleSync AI AI AI AI AI directory before running this!")
    
    command = "git push --force space clean_deploy:main"
    print(f"\nRunning: {command} ...")
    
    try:
        subprocess.run(command, check=True, shell=True)
        print("\n✅ Successfully pushed to Space!")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Push failed: {e}")

if __name__ == "__main__":
    deploy()

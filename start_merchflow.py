import os
import sys
import subprocess
import platform

def main():
    print("🚀 Starting StyleSync AI AI AI AI AI AI...")

    # 1. Auto-Detect OS and define venv paths
    system = platform.system()
    venv_dir = "venv"
    
    if system == "Windows":
        bin_dir = "Scripts"
        python_exe = "python.exe"
        uvicorn_exe = "uvicorn.exe"
    else:
        bin_dir = "bin"
        python_exe = "python"
        uvicorn_exe = "uvicorn"

    venv_python = os.path.join(venv_dir, bin_dir, python_exe)
    venv_uvicorn = os.path.join(venv_dir, bin_dir, uvicorn_exe)

    # 2. Check if venv exists
    if not os.path.exists(venv_python):
        print("❌ Error: Virtual environment not found!")
        print("Please run 'setup_env.py' first to initialize the environment.")
        sys.exit(1)

    # 3. Detect Main Server File
    server_files = [
        ("app.py", "uvicorn"),
        ("main.py", "uvicorn"),
        ("streamlit_app.py", "streamlit")
    ]
    
    target_file = None
    runner = None

    for filename, r_type in server_files:
        if os.path.exists(filename):
            target_file = filename
            runner = r_type
            break
            
    if not target_file:
        print("❌ Error: No server file found (looked for app.py, main.py, streamlit_app.py).")
        sys.exit(1)

    print(f"✅ Found {target_file}, launching with {runner}...")

    # 4. Launch Application
    try:
        if runner == "uvicorn":
            # Module name is filename without extension
            module_name = os.path.splitext(target_file)[0]
            # Construct command: uvicorn main:app --reload
            cmd = [venv_uvicorn, f"{module_name}:app", "--reload"]
            subprocess.run(cmd, check=True)
            
        elif runner == "streamlit":
             # Construct command: streamlit run streamlit_app.py
             # Note: streamlit executable might be different, usually <venv>/bin/streamlit
             streamlit_exe = os.path.join(venv_dir, bin_dir, "streamlit")
             cmd = [streamlit_exe, "run", target_file]
             subprocess.run(cmd, check=True)
             
        else:
            # Fallback for generic python scripts
            cmd = [venv_python, target_file]
            subprocess.run(cmd, check=True)

    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user.")
    except Exception as e:
        print(f"\n❌ Failed to start server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

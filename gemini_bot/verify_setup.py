import sys
import os
import importlib

def check_modules():
    modules = ["streamlit", "google.generativeai", "dotenv", "requests", "gradio_client", "PIL"]
    print("Checking modules...")
    all_installed = True
    for module in modules:
        try:
            importlib.import_module(module)
            print(f"✅ {module} installed.")
        except ImportError:
            print(f"❌ {module} not installed.")
            all_installed = False
    return all_installed

def check_syntax(directory):
    print("\nChecking syntax...")
    all_ok = True
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py") and file != "verify_setup.py": # Skip self if running
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, "r") as f:
                        compile(f.read(), filepath, "exec")
                    print(f"✅ {file} syntax OK.")
                except SyntaxError as e:
                    print(f"❌ {file} syntax error: {e}")
                    all_ok = False
    return all_ok

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if check_modules() and check_syntax(current_dir):
        print("\n✅ Setup verified successfully!")
        sys.exit(0)
    else:
        print("\n❌ Setup verification failed.")
        sys.exit(1)

import subprocess
import sys

def setup_environment():
    print("Installing Python dependencies...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    
    print("Installing Playwright browsers...")
    subprocess.run([sys.executable, "-m", "playwright", "install"])
    
    print("Setup complete!")

if __name__ == "__main__":
    setup_environment()
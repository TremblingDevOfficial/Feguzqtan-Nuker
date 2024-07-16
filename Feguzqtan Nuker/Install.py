import os
import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

packages = [
    "discord.py",
    "asyncio",
    "colorama"
]

for package in packages:
    try:
        __import__(package)
        print(f"{package} is already installed")
    except ImportError:
        print(f"Installing {package}")
        install(package)

print("All packages are installed and up-to-date.")

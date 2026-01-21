import sys
import os

# Add the project root to the python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.discovery.manager import DiscoveryManager
from src.models import Extension

def main():
    print("Starting BERA Agent...")
    manager = DiscoveryManager()
    extensions = manager.run_discovery()
    
    print(f"Discovered {len(extensions)} extensions.")
    for ext in extensions:
        print(f"[{ext.browser}] {ext.name} ({ext.version}) - {ext.id}")
        if ext.name.startswith("__MSG_"):
             print(f"   -> Path: {ext.install_path}")


if __name__ == "__main__":
    main()

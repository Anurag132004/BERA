import os
import json
import glob
from typing import List, Dict, Any
from src.models import Extension

class ChromiumDiscovery:
    def __init__(self, browser_name: str, extensions_path: str):
        self.browser_name = browser_name
        self.extensions_path = os.path.expandvars(extensions_path)

    def scan(self) -> List[Extension]:
        extensions = []
        if not os.path.exists(self.extensions_path):
            return extensions

        # Chromium extensions are stored in directories named by AppID
        # Inside AppID dir, there are version dirs. We usually want the latest version.
        # Path: <Extensions_Root>/<AppID>/<Version>/manifest.json
        
        # List all AppIDs
        app_dirs = [d for d in glob.glob(os.path.join(self.extensions_path, "*")) if os.path.isdir(d)]
        
        for app_dir in app_dirs:
            app_id = os.path.basename(app_dir)
            
            # Find version directories
            version_dirs = [d for d in glob.glob(os.path.join(app_dir, "*")) if os.path.isdir(d)]
            if not version_dirs:
                continue
                
            # Sort to get latest version (naive sort usually works, or parse semver)
            version_dirs.sort(reverse=True)
            latest_version_dir = version_dirs[0]
            
            manifest_path = os.path.join(latest_version_dir, "manifest.json")
            if os.path.exists(manifest_path):
                ext = self._parse_manifest(manifest_path, app_id, latest_version_dir)
                if ext:
                    extensions.append(ext)
                    
        return extensions

    def _parse_manifest(self, manifest_path: str, app_id: str, install_path: str) -> Extension:
        try:
            with open(manifest_path, 'r', encoding='utf-8', errors='ignore') as f:
                data = json.load(f)
                
            name = data.get('name', 'Unknown')
            # Handle localized names like __MSG_appName__? 
            # For MVP we might just leave it or try to fallback.
            # _locales/en/messages.json
            
            version = data.get('version', '0.0.0')
            description = data.get('description', '')
            author = data.get('author', '')
            if isinstance(author, dict):
                author = author.get('email', '')
            
            permissions = data.get('permissions', [])
            csp = data.get('content_security_policy', '')
            if isinstance(csp, dict):
                # MV3 CSP is an object
                csp = json.dumps(csp)
                
            update_url = data.get('update_url', '')
            
            return Extension(
                id=app_id,
                name=name,
                version=version,
                author=str(author),
                description=description,
                browser=self.browser_name,
                install_path=install_path,
                manifest_content=data,
                permissions=permissions,
                csp=str(csp),
                update_url=update_url
            )
            
        except Exception as e:
            # Log error?
            print(f"Error parsing {manifest_path}: {e}")
            return None

class ChromeDiscovery(ChromiumDiscovery):
    def __init__(self):
        # Default Windows path for Chrome
        super().__init__("Chrome", r"%LOCALAPPDATA%\Google\Chrome\User Data\Default\Extensions")

class EdgeDiscovery(ChromiumDiscovery):
    def __init__(self):
        # Default Windows path for Edge
        super().__init__("Edge", r"%LOCALAPPDATA%\Microsoft\Edge\User Data\Default\Extensions")

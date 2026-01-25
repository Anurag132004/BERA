import os
import json
import glob
from typing import List, Dict, Any
from src.models import Extension

# This is my base class for scanning Chromium-based browsers
# Chrome and Edge both use the same extension format, so I made a parent class
class ChromiumDiscovery:
    def __init__(self, browser_name: str, extensions_path: str):
        self.browser_name = browser_name
        # expandvars converts %LOCALAPPDATA% to the actual path
        self.extensions_path = os.path.expandvars(extensions_path)

    def scan(self) -> List[Extension]:
        extensions = []
        if not os.path.exists(self.extensions_path):
            return extensions

        # Chrome stores extensions like: Extensions/<AppID>/<Version>/manifest.json
        # I need to find all the AppID folders first
        app_dirs = [d for d in glob.glob(os.path.join(self.extensions_path, "*")) if os.path.isdir(d)]
        
        for app_dir in app_dirs:
            app_id = os.path.basename(app_dir)
            
            # Each extension can have multiple versions, I want the latest
            version_dirs = [d for d in glob.glob(os.path.join(app_dir, "*")) if os.path.isdir(d)]
            if not version_dirs:
                continue
                
            # Sort to get the newest version (this works most of the time)
            version_dirs.sort(reverse=True)
            latest_version_dir = version_dirs[0]
            
            manifest_path = os.path.join(latest_version_dir, "manifest.json")
            if os.path.exists(manifest_path):
                ext = self._parse_manifest(manifest_path, app_id, latest_version_dir)
                if ext:
                    extensions.append(ext)
                    
        return extensions

    def _parse_manifest(self, manifest_path: str, app_id: str, install_path: str) -> Extension:
        # This is where I read the manifest.json and extract all the info I need
        try:
            with open(manifest_path, 'r', encoding='utf-8', errors='ignore') as f:
                data = json.load(f)
                
            name = data.get('name', 'Unknown')
            # Note: Sometimes the name is like "__MSG_appName__" which means it's localized
            # I'm not handling that for now, maybe later
            
            version = data.get('version', '0.0.0')
            description = data.get('description', '')
            author = data.get('author', '')
            
            # Sometimes author is a dict with an email field (Manifest V3)
            if isinstance(author, dict):
                author = author.get('email', '')
            
            permissions = data.get('permissions', [])
            csp = data.get('content_security_policy', '')
            
            # CSP can also be a dict in MV3, so I convert it to string
            if isinstance(csp, dict):
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
            print(f"Error parsing {manifest_path}: {e}")
            return None

# Chrome-specific discovery
class ChromeDiscovery(ChromiumDiscovery):
    def __init__(self):
        # If I'm running in Docker, the extensions will be mounted at /data/extensions
        # Otherwise I use the Windows default path
        docker_path = "/data/extensions"
        if os.path.exists(docker_path):
            super().__init__("Chrome (Docker Volume)", docker_path)
        else:
            super().__init__("Chrome", r"%LOCALAPPDATA%\Google\Chrome\User Data\Default\Extensions")

# Edge uses the same format as Chrome, just different path
class EdgeDiscovery(ChromiumDiscovery):
    def __init__(self):
        docker_path = "/data/edge_extensions"
        if os.path.exists(docker_path):
            super().__init__("Edge (Docker Volume)", docker_path)
        else:
            super().__init__("Edge", r"%LOCALAPPDATA%\Microsoft\Edge\User Data\Default\Extensions")

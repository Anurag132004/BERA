import os
import re
from typing import List, Set
from src.models import Extension

class StaticScanner:
    # Regex patterns
    URL_PATTERN = re.compile(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+[^\s\'"<>]*')
    # Simple IP pattern - requires filtering later
    IP_PATTERN = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')
    
    IGNORED_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.gif', '.ico', '.woff', '.woff2', '.ttf', '.eot', '.mp3', '.mp4'}
    IGNORED_IPS = {'127.0.0.1', '0.0.0.0', '::1'}

    def scan_extension(self, extension: Extension):
        if not extension.install_path or not os.path.exists(extension.install_path):
            return

        urls = set()
        ips = set()

        for root, _, files in os.walk(extension.install_path):
            for file in files:
                _, ext = os.path.splitext(file)
                if ext.lower() in self.IGNORED_EXTENSIONS:
                    continue
                
                path = os.path.join(root, file)
                try:
                    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        
                        # Extract URLs
                        found_urls = self.URL_PATTERN.findall(content)
                        for u in found_urls:
                             # Basic filter to strip trailing junk
                             u = u.rstrip(".,;)'\"")
                             urls.add(u)
                        
                        # Extract IPs
                        found_ips = self.IP_PATTERN.findall(content)
                        for ip in found_ips:
                            if ip not in self.IGNORED_IPS:
                                ips.add(ip)
                                
                except Exception as e:
                    # Could log debug here
                    pass
        
        extension.extracted_urls = list(urls)
        extension.extracted_ips = list(ips)

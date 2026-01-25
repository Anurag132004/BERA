import os
import re
from typing import List, Set
from src.models import Extension

# This scans extension files for suspicious URLs and IP addresses
# It's basically looking for any network stuff embedded in the code
class StaticScanner:
    # My regex patterns for finding URLs and IPs
    URL_PATTERN = re.compile(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+[^\s\'"<>]*')
    IP_PATTERN = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')
    
    # I skip these file types because they're not code
    IGNORED_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.gif', '.ico', '.woff', '.woff2', '.ttf', '.eot', '.mp3', '.mp4'}
    
    # These IPs are localhost so I ignore them
    IGNORED_IPS = {'127.0.0.1', '0.0.0.0', '::1'}

    def scan_extension(self, extension: Extension):
        if not extension.install_path or not os.path.exists(extension.install_path):
            return

        urls = set()  # Using a set so I don't get duplicates
        ips = set()

        # Walk through every file in the extension folder
        for root, _, files in os.walk(extension.install_path):
            for file in files:
                _, ext = os.path.splitext(file)
                if ext.lower() in self.IGNORED_EXTENSIONS:
                    continue
                
                path = os.path.join(root, file)
                try:
                    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        
                        # Find all URLs in the file
                        found_urls = self.URL_PATTERN.findall(content)
                        for u in found_urls:
                            # Clean up trailing punctuation
                            u = u.rstrip(".,;)'\"")
                            urls.add(u)
                        
                        # Find all IPs in the file
                        found_ips = self.IP_PATTERN.findall(content)
                        for ip in found_ips:
                            if ip not in self.IGNORED_IPS:
                                ips.add(ip)
                                
                except Exception as e:
                    # Some files might be binary or locked, just skip them
                    pass
        
        extension.extracted_urls = list(urls)
        extension.extracted_ips = list(ips)

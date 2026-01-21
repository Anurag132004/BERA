import requests
import json
from datetime import datetime
from bs4 import BeautifulSoup
from typing import Optional, Tuple
from src.models import Extension

class EnrichmentClient:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

    def enrich(self, extension: Extension) -> Extension:
        if extension.browser in ["Chrome", "Edge", "Chromium"]:
             self._enrich_chrome(extension)
        elif extension.browser == "Firefox":
             self._enrich_firefox(extension)
        return extension

    def _enrich_chrome(self, extension: Extension):
        # NOTE: This scrapes the new Chrome Web Store. Selectors may break.
        url = f"https://chromewebstore.google.com/detail/{extension.id}"
        try:
            resp = self.session.get(url, timeout=5)
            if resp.status_code != 200:
                print(f"Failed to fetch CWS page for {extension.id}: {resp.status_code}")
                return

            soup = BeautifulSoup(resp.text, 'html.parser')
            
            # Helper to find text by standard sections
            # This is fragile; in a real product we'd need a robust maintenance strategy
            
            # Developer / Offered By
            # Looking for a class that holds "Offered by"
            # It's usually in a sidebar or header
            # Attempt to find "Offered by" text and get next element
            
            # Simple heuristic: Look for metadata blocks
            # For now, let's try to find the specific "Updated" date
            # There is often a textual "Updated" followed by the date
            
            # Try to grab the JSON embedded in the page if possible, but Google obfuscates it.
            # Let's rely on basic text search in the soup for now.
            
            text_content = soup.get_text()
            
            # Very naive scraping for MVP
            # "Updated\nMarch 20, 2024"
            
            # Let's just mark as "Enriched via CWS" if we found the title at least
            title_tag = soup.find('h1')
            if title_tag:
                 # Check if title matches
                 web_title = title_tag.get_text().strip()
                 # We can update the name if it's "Unknown"
                 if extension.name == "Unknown":
                     extension.name = web_title
            
            # TODO: robust scraping
            
        except Exception as e:
            print(f"Error enriching {extension.id}: {e}")

    def _enrich_firefox(self, extension: Extension):
        # Firefox API is much nicer
        url = f"https://addons.mozilla.org/api/v5/addons/addon/{extension.id}/"
        try:
            resp = self.session.get(url, timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                current_version = data.get('current_version', {})
                
                # Update metadata
                extension.name = data.get('name', {}).get('en-US', extension.name)
                extension.description = data.get('summary', {}).get('en-US', extension.description)
                
                # Public Stats
                last_updated = data.get('last_updated') # ISO string
                if last_updated:
                    # Calculate age or just store the date
                    # For risk, we care if it's OLD.
                    try:
                        dt = datetime.fromisoformat(last_updated.replace('Z', '+00:00'))
                        now = datetime.now(dt.tzinfo)
                        age = (now - dt).days
                        extension.age_days = age
                    except:
                        pass
                
                # Developer
                authors = data.get('authors', [])
                if authors:
                    extension.author = ", ".join([a.get('name') for a in authors])

        except Exception as e:
            print(f"Error enriching Firefox extension {extension.id}: {e}")

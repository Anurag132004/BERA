import requests
import json
from datetime import datetime
from bs4 import BeautifulSoup
from typing import Optional, Tuple
from src.models import Extension

# This module tries to get extra info about extensions from web stores
# Like how old they are, who made them, etc.
class EnrichmentClient:
    def __init__(self):
        self.session = requests.Session()
        # I pretend to be a real browser so websites don't block me
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

    def enrich(self, extension: Extension) -> Extension:
        # I check which browser the extension is from and call the right method
        if extension.browser in ["Chrome", "Edge", "Chromium"]:
            self._enrich_chrome(extension)
        elif extension.browser == "Firefox":
            self._enrich_firefox(extension)
        return extension

    def _enrich_chrome(self, extension: Extension):
        # Chrome Web Store doesn't have a nice API, so I have to scrape the page
        # This is kinda fragile and might break if Google changes their site
        url = f"https://chromewebstore.google.com/detail/{extension.id}"
        try:
            resp = self.session.get(url, timeout=5)
            if resp.status_code != 200:
                print(f"Failed to fetch CWS page for {extension.id}: {resp.status_code}")
                return

            soup = BeautifulSoup(resp.text, 'html.parser')
            
            # Try to at least get the title if we don't have it
            title_tag = soup.find('h1')
            if title_tag:
                web_title = title_tag.get_text().strip()
                if extension.name == "Unknown":
                    extension.name = web_title
            
            # TODO: I should try to extract more stuff like last updated date
            # but Google's HTML is really messy
            
        except Exception as e:
            print(f"Error enriching {extension.id}: {e}")

    def _enrich_firefox(self, extension: Extension):
        # Firefox actually has a proper API which is so much nicer!
        url = f"https://addons.mozilla.org/api/v5/addons/addon/{extension.id}/"
        try:
            resp = self.session.get(url, timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                current_version = data.get('current_version', {})
                
                # Get the English name
                extension.name = data.get('name', {}).get('en-US', extension.name)
                extension.description = data.get('summary', {}).get('en-US', extension.description)
                
                # Calculate how old the extension is
                last_updated = data.get('last_updated')
                if last_updated:
                    try:
                        dt = datetime.fromisoformat(last_updated.replace('Z', '+00:00'))
                        now = datetime.now(dt.tzinfo)
                        age = (now - dt).days
                        extension.age_days = age
                    except:
                        pass
                
                # Get the developer names
                authors = data.get('authors', [])
                if authors:
                    extension.author = ", ".join([a.get('name') for a in authors])

        except Exception as e:
            print(f"Error enriching Firefox extension {extension.id}: {e}")

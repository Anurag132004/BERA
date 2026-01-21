import os
import json
from typing import List
from src.models import Extension
from src.discovery.chrome import ChromeDiscovery, EdgeDiscovery

class DiscoveryManager:
    def __init__(self):
        self.discoverers = [
            ChromeDiscovery(),
            EdgeDiscovery()
            # FirefoxDiscovery() # TODO
        ]

    def run_discovery(self) -> List[Extension]:
        all_extensions = []
        for discoverer in self.discoverers:
            try:
                found = discoverer.scan()
                all_extensions.extend(found)
            except Exception as e:
                print(f"Error running discoverer {discoverer.browser_name}: {e}")
        return all_extensions

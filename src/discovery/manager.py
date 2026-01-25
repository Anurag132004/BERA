import os
import json
from typing import List
from src.models import Extension
from src.discovery.chrome import ChromeDiscovery, EdgeDiscovery

# This class manages all my browser-specific discoverers
# Right now I only have Chrome and Edge, but I can add more later
class DiscoveryManager:
    def __init__(self):
        self.discoverers = [
            ChromeDiscovery(),
            EdgeDiscovery()
            # TODO: Add FirefoxDiscovery() when I get around to it
        ]

    def run_discovery(self) -> List[Extension]:
        all_extensions = []
        # I loop through each discoverer and combine the results
        for discoverer in self.discoverers:
            try:
                found = discoverer.scan()
                all_extensions.extend(found)
            except Exception as e:
                print(f"Error running discoverer {discoverer.browser_name}: {e}")
        return all_extensions

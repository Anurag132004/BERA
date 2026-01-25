from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any

# This is my main data structure for storing extension info
# I'm using dataclass because it saves me from writing __init__ manually
@dataclass
class Extension:
    id: str  # The unique ID Chrome gives each extension
    name: str = "Unknown"
    version: str = "0.0.0"
    author: Optional[str] = None
    description: Optional[str] = None
    browser: str = "Unknown"  # Could be Chrome, Edge, or Firefox
    install_path: str = ""  # Where the extension lives on disk
    manifest_content: Dict[str, Any] = field(default_factory=dict)  # The raw manifest.json
    permissions: List[str] = field(default_factory=list)  # What the extension can do
    csp: Optional[str] = None  # Content Security Policy stuff
    update_url: Optional[str] = None
    
    # These get filled in later by my enrichment module
    age_days: Optional[int] = None
    developer_email: Optional[str] = None
    
    # My threat intel scanner fills these
    extracted_urls: List[str] = field(default_factory=list)
    extracted_ips: List[str] = field(default_factory=list)
    
    # And the AI fills these at the end
    risk_score: str = "UNKNOWN"  # Low, Medium, High, Critical
    risk_summary: str = ""

# This is what I save to the JSON file at the end
@dataclass
class RiskReport:
    run_id: str  # I generate a unique ID for each run
    timestamp: str
    total_extensions: int
    high_risk_count: int
    extensions: List[Extension]

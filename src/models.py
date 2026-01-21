from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any

@dataclass
class Extension:
    id: str  # AppID or extension ID
    name: str = "Unknown"
    version: str = "0.0.0"
    author: Optional[str] = None
    description: Optional[str] = None
    browser: str = "Unknown"  # "Chrome", "Firefox", "Edge"
    install_path: str = ""
    manifest_content: Dict[str, Any] = field(default_factory=dict)
    permissions: List[str] = field(default_factory=list)
    csp: Optional[str] = None
    update_url: Optional[str] = None
    
    # Enriched Data
    age_days: Optional[int] = None
    developer_email: Optional[str] = None
    
    # Threat Intel Data
    extracted_urls: List[str] = field(default_factory=list)
    extracted_ips: List[str] = field(default_factory=list)
    
    # Risk Assessment
    risk_score: str = "UNKNOWN" # Low, Medium, High, Critical
    risk_summary: str = ""

@dataclass
class RiskReport:
    timestamp: str
    total_extensions: int
    high_risk_count: int
    extensions: List[Extension]

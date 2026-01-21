import sys
import os
import json
import argparse
from datetime import datetime

# Add the project root to the python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.discovery.manager import DiscoveryManager
from src.enrichment.meta_client import EnrichmentClient
from src.threat_intel.scanner import StaticScanner
from src.models import Extension, RiskReport

def main():
    parser = argparse.ArgumentParser(description="BERA Agent - Browser Extension Risk Assessment")
    parser.add_argument("--output", help="Path to save the JSON report", default="report.json")
    args = parser.parse_args()

    print("Step 1: Discovery...")
    manager = DiscoveryManager()
    extensions = manager.run_discovery()
    print(f"  -> Found {len(extensions)} extensions.")

    enricher = EnrichmentClient()
    scanner = StaticScanner()

    processed_extensions = []

    print("Step 2: Analysis (Enrichment + Threat Intel)...")
    for ext in extensions:
        print(f"  Processing: {ext.name} ({ext.id})")
        
        # Module B: Enrichment
        enricher.enrich(ext)
        
        # Module C: Static Scan
        scanner.scan_extension(ext)
        
        # Module D: LLM Risk Assessment (Placeholder)
        # TODO: Implement LLM integration
        # ext.risk_score = llm_client.assess(ext)
        
        processed_extensions.append(ext)

    # Generate Report
    report = RiskReport(
        timestamp=datetime.now().isoformat(),
        total_extensions=len(processed_extensions),
        high_risk_count=0, # Calculation pending LLM
        extensions=processed_extensions
    )
    
    # Serialize
    report_dict = {
        "timestamp": report.timestamp,
        "total": report.total_extensions,
        "extensions": [e.__dict__ for e in report.extensions]
    }
    
    with open(args.output, "w", encoding='utf-8') as f:
        json.dump(report_dict, f, indent=2, default=str)
        
    print(f"\nReport saved to {args.output}")

if __name__ == "__main__":
    main()

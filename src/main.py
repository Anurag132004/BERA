import sys
import os
import json
import argparse
from datetime import datetime

# I need to add the project root to Python's path so my imports work
# This took me a while to figure out lol
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)
sys.path.append(os.getcwd())

# Importing all my modules
from src.discovery.manager import DiscoveryManager
from src.enrichment.meta_client import EnrichmentClient
from src.threat_intel.scanner import StaticScanner
from src.llm.assessor import RiskAssessor
from src.models import Extension, RiskReport

def main():
    # Setting up command line arguments
    parser = argparse.ArgumentParser(description="BERA Agent - Browser Extension Risk Assessment")
    parser.add_argument("--output", help="Path to save the JSON report", default="report.json")
    args = parser.parse_args()

    # Step 1: Find all the extensions on the system
    print("Step 1: Discovery...")
    manager = DiscoveryManager()
    extensions = manager.run_discovery()
    print(f"  -> Found {len(extensions)} extensions.")

    # Creating instances of my other modules
    enricher = EnrichmentClient()
    scanner = StaticScanner()
    assessor = RiskAssessor()

    processed_extensions = []

    # Step 2: Process each extension through my pipeline
    print("Step 2: Analysis (Enrichment + Threat Intel)...")
    for ext in extensions:
        print(f"  Processing: {ext.name} ({ext.id})")
        
        # Try to get more info from web stores
        enricher.enrich(ext)
        
        # Scan for suspicious URLs and IPs
        scanner.scan_extension(ext)
        
        # Ask the AI what it thinks
        score, reason = assessor.assess(ext)
        ext.risk_score = score
        ext.risk_summary = reason
        
        processed_extensions.append(ext)

    # Generate a unique run ID so I don't overwrite old reports
    import uuid
    run_id = uuid.uuid4().hex[:8]
    timestamp = datetime.now().isoformat()
    
    # Create my final report
    report = RiskReport(
        run_id=run_id,
        timestamp=timestamp,
        total_extensions=len(processed_extensions),
        high_risk_count=0,  # TODO: I should actually count these
        extensions=processed_extensions
    )
    
    # Convert to a dictionary so I can save it as JSON
    report_dict = {
        "run_id": report.run_id,
        "timestamp": report.timestamp,
        "total": report.total_extensions,
        "extensions": [e.__dict__ for e in report.extensions]
    }
    
    # Figure out the output filename
    # If they used the default name, I add the run ID to make it unique
    output_path = args.output
    if args.output == "report.json" or args.output == "/app/output/report.json":
        directory = os.path.dirname(args.output)
        filename = f"report_{run_id}.json"
        output_path = os.path.join(directory, filename) if directory else filename

    # Save the report!
    with open(output_path, "w", encoding='utf-8') as f:
        json.dump(report_dict, f, indent=2, default=str)
        
    print(f"\nReport saved to {output_path} (Run ID: {run_id})")

if __name__ == "__main__":
    main()

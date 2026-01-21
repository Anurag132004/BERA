import sys
import os
import json
import argparse
from datetime import datetime

# Add the project root to the python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

# Now we can import from src if we are running from src/main.py
# However, if we run `python src/main.py` from D:\BERA, `src` is a package.
# The user error `ModuleNotFoundError: No module named 'src'` happens when `d:\BERA` is not in sys.path
# OR when running inside `src` folder.

# Best fix: add the CWD (d:\BERA) to sys.path
sys.path.append(os.getcwd())

from src.discovery.manager import DiscoveryManager
from src.enrichment.meta_client import EnrichmentClient
from src.threat_intel.scanner import StaticScanner
from src.llm.assessor import RiskAssessor
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
    assessor = RiskAssessor()

    processed_extensions = []

    print("Step 2: Analysis (Enrichment + Threat Intel)...")
    for ext in extensions:
        print(f"  Processing: {ext.name} ({ext.id})")
        
        # Module B: Enrichment
        enricher.enrich(ext)
        
        # Module C: Static Scan
        scanner.scan_extension(ext)
        
        # Module D: LLM Risk Assessment
        score, reason = assessor.assess(ext)
        ext.risk_score = score
        ext.risk_summary = reason
        
        processed_extensions.append(ext)


    import uuid
    
    run_id = uuid.uuid4().hex[:8] # Short unique ID
    timestamp = datetime.now().isoformat()
    
    # Generate Report
    report = RiskReport(
        run_id=run_id,
        timestamp=timestamp,
        total_extensions=len(processed_extensions),
        high_risk_count=0, 
        extensions=processed_extensions
    )
    
    # Serialize
    report_dict = {
        "run_id": report.run_id,
        "timestamp": report.timestamp,
        "total": report.total_extensions,
        "extensions": [e.__dict__ for e in report.extensions]
    }
    
    # Determine Output Filename
    # If args.output is a directory (or default), generate a unique filename
    # If it looks like a specific json file, use that (but careful of overwrite)
    
    output_path = args.output
    if output_path.endswith(".json"):
        # If user explicitly asked for 'report.json', we might want to make it unique
        # But usually explicit file path means "write here".
        # However, user asked for "each time... new output stored... new id".
        # So let's force a unique name based on the base name.
        base, ext = os.path.splitext(output_path)
        if base == "report": # Default
             output_path = f"report_{run_id}.json"
        # If user passed custom name 'myresult.json', we might keep it or make 'myresult_ID.json'
        # Let's keep specific filenames if provided, but default to unique.
    else:
        # It's a directory
        if not os.path.exists(output_path):
            # If it doesn't exist and has no extension, treat as dir?
            # Or just default to current dir
            pass
            
    # FORCE UNIQUE FILENAME strategy for the user request
    # If the user passed "report.json", we switch to "report_<runid>.json"
    if args.output == "report.json" or args.output == "/app/output/report.json":
        # Check if we are in docker (absolute path)
        directory = os.path.dirname(args.output)
        filename = f"report_{run_id}.json"
        output_path = os.path.join(directory, filename)

    with open(output_path, "w", encoding='utf-8') as f:
        json.dump(report_dict, f, indent=2, default=str)
        
    print(f"\nReport saved to {output_path} (Run ID: {run_id})")

if __name__ == "__main__":
    main()

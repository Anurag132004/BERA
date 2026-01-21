import pytest
import os
from src.threat_intel.scanner import StaticScanner
from src.models import Extension

@pytest.fixture
def mock_extension_path(tmp_path):
    ext_dir = tmp_path / "ScanExt"
    ext_dir.mkdir()
    
    js_file = ext_dir / "background.js"
    js_file.write_text("""
        const api = "https://api.evil.com/v1/collect";
        const c2 = "192.168.1.100"; // Private IP but technically an IP
        console.log("Connecting to 8.8.8.8");
    """, encoding='utf-8')
    
    return str(ext_dir)

def test_static_scanner(mock_extension_path):
    scanner = StaticScanner()
    ext = Extension(id="test", install_path=mock_extension_path)
    
    scanner.scan_extension(ext)
    
    assert "https://api.evil.com/v1/collect" in ext.extracted_urls
    assert "8.8.8.8" in ext.extracted_ips

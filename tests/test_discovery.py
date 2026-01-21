import os
import json
import pytest
from unittest.mock import patch, MagicMock
from src.discovery.chrome import ChromiumDiscovery
from src.models import Extension

@pytest.fixture
def mock_extension_fs(tmp_path):
    # Setup a fake extensions directory structure
    ext_dir = tmp_path / "Extensions"
    ext_dir.mkdir()
    
    # App ID 1: "abcdefg"
    app_id = "abcdefg"
    app_dir = ext_dir / app_id
    app_dir.mkdir()
    
    # Version 1.0.0
    ver_dir = app_dir / "1.0.0"
    ver_dir.mkdir()
    
    manifest = {
        "name": "Test Extension",
        "version": "1.0.0",
        "manifest_version": 3,
        "permissions": ["tabs"],
        "author": "dev@example.com"
    }
    
    with open(ver_dir / "manifest.json", "w") as f:
        json.dump(manifest, f)
        
    return str(ext_dir)

def test_chromium_scan(mock_extension_fs):
    gatherer = ChromiumDiscovery("TestBrowser", mock_extension_fs)
    extensions = gatherer.scan()
    
    assert len(extensions) == 1
    ext = extensions[0]
    assert ext.id == "abcdefg"
    assert ext.name == "Test Extension"
    assert ext.version == "1.0.0"
    assert ext.browser == "TestBrowser"
    assert "tabs" in ext.permissions

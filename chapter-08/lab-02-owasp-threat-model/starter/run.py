#!/usr/bin/env python3
"""OWASP Agentic Threat Model as Code (Lab 8.2). Run from this folder: python run.py"""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
for p in [HERE, *HERE.parents]:
    if (p / "shared" / "playbook").is_dir():
        sys.path.insert(0, str(p / "shared")); break
from playbook.common import finish, DATASETS  # noqa: E402
from playbook.governance import threat_model
r, md = threat_model(HERE / "threat-model.yaml")
sys.exit(finish(r, HERE / "evidence", md))

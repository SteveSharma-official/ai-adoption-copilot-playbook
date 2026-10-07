#!/usr/bin/env python3
"""Agent Credential and Identity Audit (Lab 6.3). Run from this folder: python run.py"""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
for p in [HERE, *HERE.parents]:
    if (p / "shared" / "playbook").is_dir():
        sys.path.insert(0, str(p / "shared")); break
from playbook.common import finish, DATASETS  # noqa: E402
import json
from playbook.platform import credential_audit
src = HERE / "agents.json" if (HERE / "agents.json").exists() else DATASETS / "agents.json"
r, md = credential_audit(src)
sys.exit(finish(r, HERE / "evidence", md))

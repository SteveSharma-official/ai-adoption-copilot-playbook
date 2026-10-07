#!/usr/bin/env python3
"""Enforce the Copilot Agent Authority Matrix as Policy (Lab 7.1). Run from this folder: python run.py"""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
for p in [HERE, *HERE.parents]:
    if (p / "shared" / "playbook").is_dir():
        sys.path.insert(0, str(p / "shared")); break
from playbook.common import finish, DATASETS  # noqa: E402
from playbook.governance import authority_gateway
r, md = authority_gateway(HERE / "authority-matrix.yaml", HERE / "requests" / "replay.jsonl")
sys.exit(finish(r, HERE / "evidence", md))

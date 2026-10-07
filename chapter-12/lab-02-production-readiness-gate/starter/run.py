#!/usr/bin/env python3
"""Copilot Production Readiness Gate, Evidence First (Lab 12.2). Run from this folder: python run.py"""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
for p in [HERE, *HERE.parents]:
    if (p / "shared" / "playbook").is_dir():
        sys.path.insert(0, str(p / "shared")); break
from playbook.common import finish, DATASETS  # noqa: E402
from playbook.delivery import readiness
r, md = readiness(HERE / "checklist.yaml", HERE)
sys.exit(finish(r, HERE / "evidence", md))

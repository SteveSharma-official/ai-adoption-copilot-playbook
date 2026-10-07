#!/usr/bin/env python3
"""Approval Gate in a Copilot Studio Agent Flow (Tenant) (Lab 7.2). Run from this folder: python run.py"""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
for p in [HERE, *HERE.parents]:
    if (p / "shared" / "playbook").is_dir():
        sys.path.insert(0, str(p / "shared")); break
from playbook.common import finish, DATASETS  # noqa: E402
from playbook.governance import approval_history
r, md = approval_history(HERE / "run-history.csv", "7.2")
sys.exit(finish(r, HERE / "evidence", md))

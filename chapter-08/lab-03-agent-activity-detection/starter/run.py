#!/usr/bin/env python3
"""Detect Abnormal Agent Activity, with Ground Truth (Lab 8.3). Run from this folder: python run.py"""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
for p in [HERE, *HERE.parents]:
    if (p / "shared" / "playbook").is_dir():
        sys.path.insert(0, str(p / "shared")); break
from playbook.common import finish, DATASETS  # noqa: E402
from playbook.governance import detect
r, md = detect(HERE / "audit-log.jsonl", HERE / "rules.yaml")
sys.exit(finish(r, HERE / "evidence", md))

#!/usr/bin/env python3
"""Workload-to-Platform Decision Ladder (Lab 4.1). Run from this folder: python run.py"""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
for p in [HERE, *HERE.parents]:
    if (p / "shared" / "playbook").is_dir():
        sys.path.insert(0, str(p / "shared")); break
from playbook.common import finish, DATASETS  # noqa: E402
from playbook.business import decision_ladder
r, md = decision_ladder(HERE / "workloads.yaml")
sys.exit(finish(r, HERE / "evidence", md))

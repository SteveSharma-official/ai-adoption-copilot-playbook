#!/usr/bin/env python3
"""Enterprise AI Portfolio Map and Workload Placement (Lab 2.1). Run from this folder: python run.py"""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
for p in [HERE, *HERE.parents]:
    if (p / "shared" / "playbook").is_dir():
        sys.path.insert(0, str(p / "shared")); break
from playbook.common import finish, DATASETS  # noqa: E402
from playbook.business import portfolio
r, md = portfolio(DATASETS / "ai_tools_sanctioned.csv", DATASETS / "proxy_ai_summary_30d.csv", HERE / "workloads.yaml")
sys.exit(finish(r, HERE / "evidence", md))

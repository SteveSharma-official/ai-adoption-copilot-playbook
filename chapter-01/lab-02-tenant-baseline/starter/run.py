#!/usr/bin/env python3
"""Tenant Baseline: What Did We Buy? (Lab 1.2). Run from this folder: python run.py"""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
for p in [HERE, *HERE.parents]:
    if (p / "shared" / "playbook").is_dir():
        sys.path.insert(0, str(p / "shared")); break
from playbook.common import finish, DATASETS  # noqa: E402
from playbook.business import tenant_baseline
src = HERE / "exports"
r, md = tenant_baseline(src / "licences.csv", src / "copilot_usage.csv", src / "agents.csv")
if not (HERE / "exports" / "SOURCE.md").exists():
    r.find("export-provenance", "exports/SOURCE.md must state where and when each export was taken.")
sys.exit(finish(r, HERE / "evidence", md))

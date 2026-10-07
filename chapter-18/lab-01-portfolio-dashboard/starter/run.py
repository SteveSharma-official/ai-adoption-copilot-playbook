#!/usr/bin/env python3
"""Executive Dashboard from Evidence, and Portfolio Decisions (Lab 18.1). Run from this folder: python run.py"""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
for p in [HERE, *HERE.parents]:
    if (p / "shared" / "playbook").is_dir():
        sys.path.insert(0, str(p / "shared")); break
from playbook.common import finish, DATASETS  # noqa: E402
from playbook.sectors import dashboard
r, md = dashboard(HERE / "metrics.yaml", HERE)
sys.exit(finish(r, HERE / "evidence", md, {"dashboard.md": md}))

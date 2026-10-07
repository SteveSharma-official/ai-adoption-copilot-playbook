#!/usr/bin/env python3
"""90-Day Pilot Charter and the Day-90 Decision (Lab 11.1). Run from this folder: python run.py"""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
for p in [HERE, *HERE.parents]:
    if (p / "shared" / "playbook").is_dir():
        sys.path.insert(0, str(p / "shared")); break
from playbook.common import finish, DATASETS  # noqa: E402
from playbook.delivery import pilot_decision
r, md = pilot_decision(HERE / "charter.yaml", HERE / "measured.yaml")
sys.exit(finish(r, HERE / "evidence", md, {"day-90-decision.md": md}))

#!/usr/bin/env python3
"""Decision Authority and the AI Use-Case Register (Public Sector) (Lab 15.1). Run from this folder: python run.py"""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
for p in [HERE, *HERE.parents]:
    if (p / "shared" / "playbook").is_dir():
        sys.path.insert(0, str(p / "shared")); break
from playbook.common import finish, DATASETS  # noqa: E402
from playbook.sectors import decision_authority
r, md = decision_authority(HERE / "workflow-policy.yaml", HERE / "events.json", HERE / "use-case-register.yaml")
sys.exit(finish(r, HERE / "evidence", md))

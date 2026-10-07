#!/usr/bin/env python3
"""Operating Model, Support Routing and the Adoption Ladder (Lab 17.1). Run from this folder: python run.py"""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
for p in [HERE, *HERE.parents]:
    if (p / "shared" / "playbook").is_dir():
        sys.path.insert(0, str(p / "shared")); break
from playbook.common import finish, DATASETS  # noqa: E402
from playbook.governance import operating_model
r, md = operating_model(HERE / "agents.json", HERE / "incidents.csv", HERE / "raci.yaml")
sys.exit(finish(r, HERE / "evidence", md))

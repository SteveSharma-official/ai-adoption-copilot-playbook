#!/usr/bin/env python3
"""Process Archaeology and the Use-Case Discovery Canvas (Lab 9.1). Run from this folder: python run.py"""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
for p in [HERE, *HERE.parents]:
    if (p / "shared" / "playbook").is_dir():
        sys.path.insert(0, str(p / "shared")); break
from playbook.common import finish, DATASETS  # noqa: E402
from playbook.delivery import discovery
r, md = discovery(HERE / "canvases.yaml", HERE / "observations.csv")
sys.exit(finish(r, HERE / "evidence", md))

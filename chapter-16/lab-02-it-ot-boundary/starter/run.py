#!/usr/bin/env python3
"""The IT/OT Boundary as an Architecture Test (Manufacturing) (Lab 16.2). Run from this folder: python run.py"""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
for p in [HERE, *HERE.parents]:
    if (p / "shared" / "playbook").is_dir():
        sys.path.insert(0, str(p / "shared")); break
from playbook.common import finish, DATASETS  # noqa: E402
from playbook.platform import architecture
r, md, mermaid = architecture(HERE / "architecture.yaml")
sys.exit(finish(r, HERE / "evidence", md, {"architecture.mmd": mermaid}))

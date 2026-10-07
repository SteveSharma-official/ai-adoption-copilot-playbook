#!/usr/bin/env python3
"""Clinical Documentation Boundary Tests (Healthcare) (Lab 14.1). Run from this folder: python run.py"""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
for p in [HERE, *HERE.parents]:
    if (p / "shared" / "playbook").is_dir():
        sys.path.insert(0, str(p / "shared")); break
from playbook.common import finish, DATASETS  # noqa: E402
from playbook.sectors import clinical_boundary
r, md = clinical_boundary(HERE / "notes.json", HERE / "drafts.json", HERE / "regulated-prompts.yaml", HERE / "responses.json")
sys.exit(finish(r, HERE / "evidence", md))

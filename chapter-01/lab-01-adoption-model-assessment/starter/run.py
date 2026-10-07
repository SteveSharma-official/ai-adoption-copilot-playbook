#!/usr/bin/env python3
"""Copilot Enterprise Adoption Model Self-Assessment (Lab 1.1). Run from this folder: python run.py"""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
for p in [HERE, *HERE.parents]:
    if (p / "shared" / "playbook").is_dir():
        sys.path.insert(0, str(p / "shared")); break
from playbook.common import finish, DATASETS  # noqa: E402
from playbook.business import adoption_assessment
r, md = adoption_assessment(HERE / "assessment.yaml", HERE)
sys.exit(finish(r, HERE / "evidence", md, {"platform-fit-one-pager.md": md}))

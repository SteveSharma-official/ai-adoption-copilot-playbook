#!/usr/bin/env python3
"""Value Hypothesis and Baseline (Lab 3.1). Run from this folder: python run.py"""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
for p in [HERE, *HERE.parents]:
    if (p / "shared" / "playbook").is_dir():
        sys.path.insert(0, str(p / "shared")); break
from playbook.common import finish, DATASETS  # noqa: E402
from playbook.business import value_baseline
r, md = value_baseline(DATASETS / "ap_process_events.csv", HERE / "hypothesis.yaml")
sys.exit(finish(r, HERE / "evidence", md))

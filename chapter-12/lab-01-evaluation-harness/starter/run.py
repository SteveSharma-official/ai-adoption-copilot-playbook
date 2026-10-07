#!/usr/bin/env python3
"""Evaluation Harness and Release Gate (Lab 12.1). Run from this folder: python run.py"""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
for p in [HERE, *HERE.parents]:
    if (p / "shared" / "playbook").is_dir():
        sys.path.insert(0, str(p / "shared")); break
from playbook.common import finish, DATASETS  # noqa: E402
from playbook.delivery import evaluation
r, md = evaluation(HERE / "testset.yaml", HERE / "responses" / "candidate.jsonl", HERE / "thresholds.yaml", HERE / "responses" / "previous.jsonl")
sys.exit(finish(r, HERE / "evidence", md))

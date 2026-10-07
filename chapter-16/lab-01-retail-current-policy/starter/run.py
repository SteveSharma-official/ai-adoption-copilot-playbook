#!/usr/bin/env python3
"""Retail Policy Agent: Current Policy and Consumer Law Escalation (Lab 16.1). Run from this folder: python run.py"""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
for p in [HERE, *HERE.parents]:
    if (p / "shared" / "playbook").is_dir():
        sys.path.insert(0, str(p / "shared")); break
from playbook.common import finish, DATASETS  # noqa: E402
from playbook.delivery import grounded_agent_tests
r, md = grounded_agent_tests("16.1", "Retail policy agent tests", HERE / "corpus.json", HERE / "agent-config.yaml", HERE / "tests.yaml")
sys.exit(finish(r, HERE / "evidence", md))

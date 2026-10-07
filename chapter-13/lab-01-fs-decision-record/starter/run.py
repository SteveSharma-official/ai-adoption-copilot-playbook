#!/usr/bin/env python3
"""Regulator-Ready Decision Records (Financial Services) (Lab 13.1). Run from this folder: python run.py"""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
for p in [HERE, *HERE.parents]:
    if (p / "shared" / "playbook").is_dir():
        sys.path.insert(0, str(p / "shared")); break
from playbook.common import finish, DATASETS  # noqa: E402
from playbook.sectors import decision_records, verify_chain
r, md, chain = decision_records(HERE / "cases.json", HERE / "policy-versions.yaml")
if not verify_chain(chain):
    r.find("chain-broken", "Decision record hash chain does not verify.")
sys.exit(finish(r, HERE / "evidence", md, {"decision-records.jsonl": chain}))

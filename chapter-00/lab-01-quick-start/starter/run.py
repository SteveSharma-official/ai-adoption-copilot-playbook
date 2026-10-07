#!/usr/bin/env python3
"""Quick Start: Your First Evidence Pack (Lab 0.1). Run from this folder: python run.py"""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
for p in [HERE, *HERE.parents]:
    if (p / "shared" / "playbook").is_dir():
        sys.path.insert(0, str(p / "shared")); break
from playbook.common import finish, DATASETS  # noqa: E402
from playbook.common import Result
import platform
r = Result("0.1", "Quick start: environment check and first evidence pack")
need = ["users.csv", "group_members.csv", "sites.csv", "site_grants.csv", "sharing_links.csv", "agents.json"]
missing = [n for n in need if not (DATASETS / n).exists()]
for n in missing:
    r.find("dataset-missing", f"Synthetic dataset {n} not found in shared/datasets/harbourline.")
if sys.version_info < (3, 11):
    r.find("python-version", "Python 3.11 or later is required.")
r.data = {"python": platform.python_version(), "datasets_found": len(need) - len(missing)}
cfg = (HERE / "lab.yaml").read_text()
if "evidence_owner:" not in cfg or "evidence_owner: \"\"" in cfg:
    r.find("no-evidence-owner", "Set evidence_owner in lab.yaml: every evidence pack has a named owner.")
sys.exit(finish(r, HERE / "evidence", "# Quick Start Evidence\n\nEnvironment checked; datasets present.\n"))

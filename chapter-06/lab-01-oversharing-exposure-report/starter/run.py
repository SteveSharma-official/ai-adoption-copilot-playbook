#!/usr/bin/env python3
"""Oversharing Discovery and the Copilot Exposure Report (Lab 6.1). Run from this folder: python run.py"""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
for p in [HERE, *HERE.parents]:
    if (p / "shared" / "playbook").is_dir():
        sys.path.insert(0, str(p / "shared")); break
from playbook.common import finish, DATASETS  # noqa: E402
import yaml
from playbook.platform import exposure_report
ov = yaml.safe_load((HERE / "remediation.yaml").read_text()) if (HERE / "remediation.yaml").exists() else {}
extra = yaml.safe_load((HERE / "new-changes.yaml").read_text()) if (HERE / "new-changes.yaml").exists() else {}
for k, v in (extra or {}).items():
    ov.setdefault(k, []).extend(v) if isinstance(v, list) else ov.setdefault(k, {}).update(v)
r, md = exposure_report("pilot", ov)
sys.exit(finish(r, HERE / "evidence", md))

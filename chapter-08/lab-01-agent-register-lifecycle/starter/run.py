#!/usr/bin/env python3
"""Agent Register and Lifecycle Controls (Lab 8.1). Run from this folder: python run.py"""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
for p in [HERE, *HERE.parents]:
    if (p / "shared" / "playbook").is_dir():
        sys.path.insert(0, str(p / "shared")); break
from playbook.common import finish, DATASETS  # noqa: E402
from playbook.governance import register_lifecycle
agents = HERE / "agents.json" if (HERE / "agents.json").exists() else DATASETS / "agents.json"
reg = HERE / "agent_register.csv" if (HERE / "agent_register.csv").exists() else DATASETS / "agent_register.csv"
users = HERE / "users.csv" if (HERE / "users.csv").exists() else DATASETS / "users.csv"
r, md = register_lifecycle(agents, reg, users)
sys.exit(finish(r, HERE / "evidence", md))

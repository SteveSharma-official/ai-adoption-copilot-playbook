#!/usr/bin/env python3
"""The Five Layers of the Copilot Data Exposure Model, Tested (Lab 6.2). Run from this folder: python run.py"""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
for p in [HERE, *HERE.parents]:
    if (p / "shared" / "playbook").is_dir():
        sys.path.insert(0, str(p / "shared")); break
from playbook.common import finish, DATASETS  # noqa: E402
import subprocess
from playbook.common import Result
r = Result("6.2", "Five-layer teaching retriever behaviour tests")
p = subprocess.run([sys.executable, "-m", "pytest", "-q", str(HERE / "test_layers.py")], capture_output=True, text=True)
if p.returncode != 0:
    r.find("layer-test-failed", "One or more layer tests failed; see pytest output in report.md.")
r.data = {"pytest_summary": p.stdout.strip().splitlines()[-1] if p.stdout.strip() else ""}
sys.exit(finish(r, HERE / "evidence", "# Layer Tests\n\n```\n" + p.stdout + "\n```\n"))

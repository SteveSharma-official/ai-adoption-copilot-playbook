#!/usr/bin/env python3
"""Capstone: Enterprise AI Adoption Journey, from Hypothesis to Production Decision (Lab Capstone). Run from this folder: python run.py"""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
for p in [HERE, *HERE.parents]:
    if (p / "shared" / "playbook").is_dir():
        sys.path.insert(0, str(p / "shared")); break
from playbook.common import finish, DATASETS  # noqa: E402
import yaml
from pathlib import Path
from playbook.common import Result, write_evidence, md_table
from playbook.business import value_baseline
from playbook.platform import exposure_report, credential_audit
from playbook.governance import authority_gateway
from playbook.delivery import evaluation, readiness

ev = HERE / "evidence"
stages = []
def stage(name, fn):
    res = fn()
    r, md = res[0], res[1]
    write_evidence(r, ev / "stages" / name, md)
    marker = ev / "stages" / name / "PASSED"
    if r.passed:
        marker.write_text("stage passed; see result.json and manifest.json\n")
    elif marker.exists():
        marker.unlink()
    stages.append({"stage": name, "lab_pattern": r.lab_id, "status": "PASS" if r.passed else "FAIL",
                   "blocking": sum(f["blocking"] for f in r.findings)})

stage("1-value", lambda: value_baseline(DATASETS / "ap_process_events.csv", HERE / "inputs" / "hypothesis.yaml"))
ov = yaml.safe_load((HERE / "inputs" / "remediation.yaml").read_text()) if (HERE / "inputs" / "remediation.yaml").exists() else {}
stage("2-exposure", lambda: exposure_report("pilot", ov))
stage("3-identity", lambda: credential_audit(HERE / "inputs" / "agents.json"))
stage("4-authority", lambda: authority_gateway(HERE / "inputs" / "authority-matrix.yaml", HERE / "inputs" / "replay.jsonl"))
stage("5-evaluation", lambda: evaluation(HERE / "inputs" / "testset.yaml", HERE / "inputs" / "candidate.jsonl", HERE / "inputs" / "thresholds.yaml"))
stage("6-readiness", lambda: readiness(HERE / "inputs" / "readiness.yaml", HERE))

r = Result("Capstone", "Harbourline AP supplier query agent: production decision pack")
for s in stages:
    if s["status"] != "PASS":
        r.find("stage-failed", f"Stage {s['stage']} failed with {s['blocking']} blocking findings.")
r.data = {"stages": stages, "decision": "Proceed to production review board" if r.passed else "Do not deploy"}
md = "# Capstone Decision Pack\n\n**Recommendation:** " + r.data["decision"] + "\n\n" + md_table(stages, ["stage", "lab_pattern", "status", "blocking"]) + \
     "\nSign-off required: executive sponsor, CISO, business owner, enterprise architect.\n"
sys.exit(finish(r, ev, md, {"decision-pack.md": md}))

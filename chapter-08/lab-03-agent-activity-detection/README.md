# Lab 8.3 Detect Abnormal Agent Activity, with Ground Truth

**Book:** Chapter 8, section "8.4 Controls Before Connections"
**Difficulty:** Level 4 (Secure)
**Platform:** Local; Microsoft Sentinel for real data
**Effort:** 60 minutes
**Cloud tenant needed:** Optional (KQL is CLOUD VALIDATION REQUIRED)
**API key needed:** No
**Data:** synthetic only (Harbourline Group is fictional; domain harbourline.example)

## What You Will Build
Three detection rules over a synthetic agent audit log with three ground-truth incidents, plus a KQL template.

## Why This Matters
A rule that misses the incident it was written for is worse than none, because it creates confidence.

## Enterprise Scenario
Harbourline's refund agent floods the POS with requests after a bad prompt change.

## Learning Objectives
- Detect volume anomalies, label access and out-of-matrix actions
- Measure misses and false positives
- Adapt a KQL template

## Prerequisites
- Python 3.11 or later and `pip install -r requirements.txt` from the repository root
- Lab 0.1 completed (you know how to read an evidence pack)
- The book section above read first: the lab tests the decision, not the reading

## Architecture
The lab follows the repository pattern: your inputs in `starter/`, a shared engine in `shared/playbook/`, and evidence written to `evidence/`.

```
inputs (YAML, CSV, JSON)  -->  run.py  -->  shared/playbook engine  -->  evidence/result.json, report.md, manifest.json
```

Core concept: Agent activity detection with ground truth.

## Repository Structure
```
chapter-08/lab-03-agent-activity-detection/
  README.md
  lab.json
  starter/
    audit-log.jsonl
    rules.yaml
    run.py
    sentinel/agent-volume-anomaly.kql.template
  solution/
    rules.yaml
  lab-changes/
    rules.yaml
```

## Steps

### Step 1. Environment Setup
From the repository root:
```
python shared/scripts/start-lab.py 8.3
cd workspace/lab-8.3
```
This copies `starter/` into a workspace folder that git ignores, so you can break things freely.

### Step 2. Configure
Inspect audit-log.jsonl and rules.yaml. The starter is a compliant baseline: your first run should PASS.
```
python run.py
```

### Step 3. Build
Tune thresholds so all three incidents are detected. To compare with the reference, apply the solution:
```
python ../../shared/scripts/start-lab.py 8.3 --apply solution
```

### Step 4. Test
```
python run.py
```
Expected: `PASS`. Open `evidence/report.md` and `evidence/result.json`.

### Step 5. Secure
Do not export real audit logs into a public fork. Confirm `evidence/manifest.json` lists a SHA-256 hash for every evidence file.

### Step 6. Break It Safely
lab-changes/ raises the volume multiplier to 50 'because there were too many alerts'. Apply it:
```
python ../../shared/scripts/start-lab.py 8.3 --apply lab-changes
```
Anything marked INTENTIONALLY INSECURE is for lab use only.

### Step 7. Observe
```
python run.py
```
Expected: `FAIL` with a blocking finding `missed-incident`. Read the message: it names what changed and why it matters.

### Step 8. Remediate
Restore the threshold and reduce noise by scoping, not by blinding.
```
python ../../shared/scripts/start-lab.py 8.3 --apply solution
```

### Step 9. Validate
```
python run.py
```
Expected: `PASS`. Prove the fix from the repository root as well:
```
python -m pytest -q "tests/test_lab_sequences.py::test_lab_sequence[8.3]"
```

## Expected Results
| Stage | Expected status |
|---|---|
| Starter | PASS |
| After your build or the solution | PASS |
| After lab-changes (break it safely) | FAIL (missed-incident) |
| After remediation | PASS |

## Evidence
Detection results with missed and false-positive counts. Keep the whole `evidence/` folder; the manifest lets a reviewer confirm nothing was edited after the run.

## Common Problems
- The KQL file is a template; table and column names must be verified in your workspace.

## Security Considerations
Do not export real audit logs into a public fork.

## Enterprise Application
Pair each rule with a runbook (Chapter 17).

## Production Considerations
Measure detection against new incidents quarterly.

## Cleanup
Delete `workspace/lab-8.3`. No cloud resources are created by the local lab.

## Further Challenge
Add a rule for actions outside business hours.

---
Validation status: LOCALLY VALIDATED: the full sequence (starter, solution, break it safely, prove the fix) passed on 2026-10-07 with Python 3.13.16, pytest 8.4.2, PyYAML 6.0.3, using synthetic data only. GitHub Actions workflow: STATICALLY VALIDATED (actionlint 1.7.12); EXECUTION VALIDATION REQUIRED on a hosted runner.

# Lab 7.1 Enforce the Copilot Agent Authority Matrix as Policy

**Book:** Chapter 7, section "7.2 The Copilot Agent Authority Matrix"
**Difficulty:** Level 4 (Secure)
**Platform:** Local
**Effort:** 60 minutes
**Cloud tenant needed:** No
**API key needed:** No
**Data:** synthetic only (Harbourline Group is fictional; domain harbourline.example)

## What You Will Build
An authority-matrix gateway with parameter limits and human approval, tested by replaying eight requests including an indirect prompt injection.

## Why This Matters
An authority level that is not enforced is a wish. Replay makes enforcement testable before an incident tests it for you.

## Enterprise Scenario
A spoofed supplier email instructs Harbourline's AP agent to create a new vendor with new bank details.

## Learning Objectives
- Encode L1 to L4 and Never
- Enforce limits and separate approver from requester
- Prove an injection cannot reach a Never action

## Prerequisites
- Python 3.11 or later and `pip install -r requirements.txt` from the repository root
- Lab 0.1 completed (you know how to read an evidence pack)
- The book section above read first: the lab tests the decision, not the reading

## Architecture
The lab follows the repository pattern: your inputs in `starter/`, a shared engine in `shared/playbook/`, and evidence written to `evidence/`.

```
inputs (YAML, CSV, JSON)  -->  run.py  -->  shared/playbook engine  -->  evidence/result.json, report.md, manifest.json
```

Core concept: Copilot Agent Authority Matrix (L1 to L4, Never).

## Repository Structure
```
chapter-07/lab-01-authority-matrix-gateway/
  README.md
  lab.json
  starter/
    authority-matrix.yaml
    requests/replay.jsonl
    run.py
  solution/
    authority-matrix.yaml
  lab-changes/
    authority-matrix.yaml
```

## Steps

### Step 1. Environment Setup
From the repository root:
```
python shared/scripts/start-lab.py 7.1
cd workspace/lab-7.1
```
This copies `starter/` into a workspace folder that git ignores, so you can break things freely.

### Step 2. Configure
Inspect authority-matrix.yaml and requests/replay.jsonl. The starter is a compliant baseline: your first run should PASS.
```
python run.py
```

### Step 3. Build
Add one action with a parameter limit and a replay request for it. To compare with the reference, apply the solution:
```
python ../../shared/scripts/start-lab.py 7.1 --apply solution
```

### Step 4. Test
```
python run.py
```
Expected: `PASS`. Open `evidence/report.md` and `evidence/result.json`.

### Step 5. Secure
The gateway sits outside the model. Prompt instructions are not a control. Confirm `evidence/manifest.json` lists a SHA-256 hash for every evidence file.

### Step 6. Break It Safely
lab-changes/ moves vendor creation to L4 'to reduce friction'. Apply it:
```
python ../../shared/scripts/start-lab.py 7.1 --apply lab-changes
```
Anything marked INTENTIONALLY INSECURE is for lab use only.

### Step 7. Observe
```
python run.py
```
Expected: `FAIL` with a blocking finding `replay-mismatch`. Read the message: it names what changed and why it matters.

### Step 8. Remediate
Restore Never and record why in the matrix.
```
python ../../shared/scripts/start-lab.py 7.1 --apply solution
```

### Step 9. Validate
```
python run.py
```
Expected: `PASS`. Prove the fix from the repository root as well:
```
python -m pytest -q "tests/test_lab_sequences.py::test_lab_sequence[7.1]"
```

## Expected Results
| Stage | Expected status |
|---|---|
| Starter | PASS |
| After your build or the solution | PASS |
| After lab-changes (break it safely) | FAIL (replay-mismatch) |
| After remediation | PASS |

## Evidence
Replay decisions with expected and actual outcomes. Keep the whole `evidence/` folder; the manifest lets a reviewer confirm nothing was edited after the run.

## Common Problems
- Every action must be in tool_bindings and the matrix.

## Security Considerations
The gateway sits outside the model. Prompt instructions are not a control.

## Enterprise Application
Have the business owner sign the matrix; the platform team enforces it.

## Production Considerations
Log every decision to Sentinel (Lab 8.3).

## Cleanup
Delete `workspace/lab-7.1`. No cloud resources are created by the local lab.

## Further Challenge
Add a daily cumulative limit across requests.

---
Validation status: LOCALLY VALIDATED: the full sequence (starter, solution, break it safely, prove the fix) passed on 2026-10-07 with Python 3.13.16, pytest 8.4.2, PyYAML 6.0.3, using synthetic data only. GitHub Actions workflow: STATICALLY VALIDATED (actionlint 1.7.12); EXECUTION VALIDATION REQUIRED on a hosted runner.

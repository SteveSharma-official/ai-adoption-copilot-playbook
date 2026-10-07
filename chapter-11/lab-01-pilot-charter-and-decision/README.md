# Lab 11.1 90-Day Pilot Charter and the Day-90 Decision

**Book:** Chapter 11, section "11.4 Days 61 to 90: Prove and Decide"
**Difficulty:** Level 5 (Evaluate)
**Platform:** Local
**Effort:** 45 minutes
**Cloud tenant needed:** No
**API key needed:** No
**Data:** synthetic only (Harbourline Group is fictional; domain harbourline.example)

## What You Will Build
A charter validator and decision engine using measured results and readiness evidence.

## Why This Matters
A pilot without kill criteria is a slow rollout without consent.

## Enterprise Scenario
Harbourline's AP pilot ends on day 90. A stakeholder asks for 'a bit more time'.

## Learning Objectives
- Validate gates and kill criteria
- Compute the day-90 decision
- Reject extensions that change nothing

## Prerequisites
- Python 3.11 or later and `pip install -r requirements.txt` from the repository root
- Lab 0.1 completed (you know how to read an evidence pack)
- The book section above read first: the lab tests the decision, not the reading

## Architecture
The lab follows the repository pattern: your inputs in `starter/`, a shared engine in `shared/playbook/`, and evidence written to `evidence/`.

```
inputs (YAML, CSV, JSON)  -->  run.py  -->  shared/playbook engine  -->  evidence/result.json, report.md, manifest.json
```

Core concept: 90-day pilot with gates and kill criteria.

## Repository Structure
```
chapter-11/lab-01-pilot-charter-and-decision/
  README.md
  lab.json
  starter/
    charter.yaml
    measured.yaml
    run.py
  solution/
    charter.yaml
  lab-changes/
    charter.yaml
```

## Steps

### Step 1. Environment Setup
From the repository root:
```
python shared/scripts/start-lab.py 11.1
cd workspace/lab-11.1
```
This copies `starter/` into a workspace folder that git ignores, so you can break things freely.

### Step 2. Configure
Inspect charter.yaml and measured.yaml. The starter is a compliant baseline: your first run should PASS.
```
python run.py
```

### Step 3. Build
Set kill criteria for your own pilot. To compare with the reference, apply the solution:
```
python ../../shared/scripts/start-lab.py 11.1 --apply solution
```

### Step 4. Test
```
python run.py
```
Expected: `PASS`. Open `evidence/report.md` and `evidence/result.json`.

### Step 5. Secure
Kill criteria should include any security finding above a set severity. Confirm `evidence/manifest.json` lists a SHA-256 hash for every evidence file.

### Step 6. Break It Safely
lab-changes/ adds an extension with no scope or method change. Apply it:
```
python ../../shared/scripts/start-lab.py 11.1 --apply lab-changes
```
Anything marked INTENTIONALLY INSECURE is for lab use only.

### Step 7. Observe
```
python run.py
```
Expected: `FAIL` with a blocking finding `extension-without-change`. Read the message: it names what changed and why it matters.

### Step 8. Remediate
Decide now, or change scope or method explicitly.
```
python ../../shared/scripts/start-lab.py 11.1 --apply solution
```

### Step 9. Validate
```
python run.py
```
Expected: `PASS`. Prove the fix from the repository root as well:
```
python -m pytest -q "tests/test_lab_sequences.py::test_lab_sequence[11.1]"
```

## Expected Results
| Stage | Expected status |
|---|---|
| Starter | PASS |
| After your build or the solution | PASS |
| After lab-changes (break it safely) | FAIL (extension-without-change) |
| After remediation | PASS |

## Evidence
Day-90 decision record. Keep the whole `evidence/` folder; the manifest lets a reviewer confirm nothing was edited after the run.

## Common Problems
- Dates must be ISO format.

## Security Considerations
Kill criteria should include any security finding above a set severity.

## Enterprise Application
Sign-off by sponsor, CISO and business owner.

## Production Considerations
Archive the decision record with the evidence pack.

## Cleanup
Delete `workspace/lab-11.1`. No cloud resources are created by the local lab.

## Further Challenge
Add a cost-per-case kill criterion.

---
Validation status: LOCALLY VALIDATED: the full sequence (starter, solution, break it safely, prove the fix) passed on 2026-10-07 with Python 3.13.16, pytest 8.4.2, PyYAML 6.0.3, using synthetic data only. GitHub Actions workflow: STATICALLY VALIDATED (actionlint 1.7.12); EXECUTION VALIDATION REQUIRED on a hosted runner.

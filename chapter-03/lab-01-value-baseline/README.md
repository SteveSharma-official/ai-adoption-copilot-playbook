# Lab 3.1 Value Hypothesis and Baseline

**Book:** Chapter 3, section "3.3 Baseline Before You Deploy"
**Difficulty:** Level 2 (Build)
**Platform:** Local
**Effort:** 45 minutes
**Cloud tenant needed:** No
**API key needed:** No
**Data:** synthetic only (Harbourline Group is fictional; domain harbourline.example)

## What You Will Build
A baseline engine that computes step medians from synthetic process events and tests whether the hypothesis targets the bottleneck.

## Why This Matters
Value claims fail at the CFO's desk when they cannot be measured. A baseline turns a hope into a test.

## Enterprise Scenario
Harbourline AP believes Copilot drafting will speed up supplier queries. The event log says the delay is in lookup, not drafting.

## Learning Objectives
- Compute per-step medians
- Identify the bottleneck
- Reject a hypothesis aimed at the wrong step

## Prerequisites
- Python 3.11 or later and `pip install -r requirements.txt` from the repository root
- Lab 0.1 completed (you know how to read an evidence pack)
- The book section above read first: the lab tests the decision, not the reading

## Architecture
The lab follows the repository pattern: your inputs in `starter/`, a shared engine in `shared/playbook/`, and evidence written to `evidence/`.

```
inputs (YAML, CSV, JSON)  -->  run.py  -->  shared/playbook engine  -->  evidence/result.json, report.md, manifest.json
```

Core concept: Value hypothesis and baseline.

## Repository Structure
```
chapter-03/lab-01-value-baseline/
  README.md
  lab.json
  starter/
    hypothesis.yaml
    run.py
  solution/
    hypothesis.yaml
  lab-changes/
    hypothesis.yaml
```

## Steps

### Step 1. Environment Setup
From the repository root:
```
python shared/scripts/start-lab.py 3.1
cd workspace/lab-3.1
```
This copies `starter/` into a workspace folder that git ignores, so you can break things freely.

### Step 2. Configure
Inspect hypothesis.yaml and ap_process_events.csv. The starter is a compliant baseline: your first run should PASS.
```
python run.py
```

### Step 3. Build
Write the hypothesis for the bottleneck step with a minimum sample. To compare with the reference, apply the solution:
```
python ../../shared/scripts/start-lab.py 3.1 --apply solution
```

### Step 4. Test
```
python run.py
```
Expected: `PASS`. Open `evidence/report.md` and `evidence/result.json`.

### Step 5. Secure
Process logs may contain supplier names; use synthetic or masked data in labs. Confirm `evidence/manifest.json` lists a SHA-256 hash for every evidence file.

### Step 6. Break It Safely
lab-changes/ retargets the hypothesis at drafting. Apply it:
```
python ../../shared/scripts/start-lab.py 3.1 --apply lab-changes
```
Anything marked INTENTIONALLY INSECURE is for lab use only.

### Step 7. Observe
```
python run.py
```
Expected: `FAIL` with a blocking finding `not-the-bottleneck`. Read the message: it names what changed and why it matters.

### Step 8. Remediate
Target the measured bottleneck step.
```
python ../../shared/scripts/start-lab.py 3.1 --apply solution
```

### Step 9. Validate
```
python run.py
```
Expected: `PASS`. Prove the fix from the repository root as well:
```
python -m pytest -q "tests/test_lab_sequences.py::test_lab_sequence[3.1]"
```

## Expected Results
| Stage | Expected status |
|---|---|
| Starter | PASS |
| After your build or the solution | PASS |
| After lab-changes (break it safely) | FAIL (not-the-bottleneck) |
| After remediation | PASS |

## Evidence
Baseline report with step medians and hypothesis verdict. Keep the whole `evidence/` folder; the manifest lets a reviewer confirm nothing was edited after the run.

## Common Problems
- Fewer than 30 cases produces insufficient-sample.

## Security Considerations
Process logs may contain supplier names; use synthetic or masked data in labs.

## Enterprise Application
Have the process owner sign the baseline before the pilot starts (Chapter 11).

## Production Considerations
Keep the baseline query versioned so day-90 measurement uses the same definition.

## Cleanup
Delete `workspace/lab-3.1`. No cloud resources are created by the local lab.

## Further Challenge
Add a check for the efficiency trap: time saved that is not redeployed.

---
Validation status: LOCALLY VALIDATED: the full sequence (starter, solution, break it safely, prove the fix) passed on 2026-10-07 with Python 3.13.16, pytest 8.4.2, PyYAML 6.0.3, using synthetic data only. GitHub Actions workflow: STATICALLY VALIDATED (actionlint 1.7.12); EXECUTION VALIDATION REQUIRED on a hosted runner.

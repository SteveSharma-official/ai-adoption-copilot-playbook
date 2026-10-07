# Lab 18.1 Executive Dashboard from Evidence, and Portfolio Decisions

**Book:** Chapter 18, section "18.4 The Executive Dashboard and the Retire Decision"
**Difficulty:** Level 8 (Scale)
**Platform:** Local
**Effort:** 45 minutes
**Cloud tenant needed:** No
**API key needed:** No
**Data:** synthetic only (Harbourline Group is fictional; domain harbourline.example)

## What You Will Build
A dashboard generator over evidence files across five dimensions, with a prioritisation grid and quarterly retire review.

## Why This Matters
Scaling from one win to a portfolio needs numbers the board can audit.

## Enterprise Scenario
Harbourline's board wants to fund three more use cases and asks what the first one delivered.

## Learning Objectives
- Trace each metric to evidence
- Cover all five dimensions
- Apply retire rules

## Prerequisites
- Python 3.11 or later and `pip install -r requirements.txt` from the repository root
- Lab 0.1 completed (you know how to read an evidence pack)
- The book section above read first: the lab tests the decision, not the reading

## Architecture
The lab follows the repository pattern: your inputs in `starter/`, a shared engine in `shared/playbook/`, and evidence written to `evidence/`.

```
inputs (YAML, CSV, JSON)  -->  run.py  -->  shared/playbook engine  -->  evidence/result.json, report.md, manifest.json
```

Core concept: Portfolio dashboard from evidence.

## Repository Structure
```
chapter-18/lab-01-portfolio-dashboard/
  README.md
  lab.json
  starter/
    inputs/adoption.json
    inputs/exposure.json
    inputs/portfolio.json
    inputs/register.json
    inputs/value.json
    metrics.yaml
    run.py
  solution/
    metrics.yaml
  lab-changes/
    metrics.yaml
```

## Steps

### Step 1. Environment Setup
From the repository root:
```
python shared/scripts/start-lab.py 18.1
cd workspace/lab-18.1
```
This copies `starter/` into a workspace folder that git ignores, so you can break things freely.

### Step 2. Configure
Inspect metrics.yaml and inputs/. The starter is a compliant baseline: your first run should PASS.
```
python run.py
```

### Step 3. Build
Point inputs at evidence from your own labs. To compare with the reference, apply the solution:
```
python ../../shared/scripts/start-lab.py 18.1 --apply solution
```

### Step 4. Test
```
python run.py
```
Expected: `PASS`. Open `evidence/report.md` and `evidence/result.json`.

### Step 5. Secure
Aggregate metrics; never show individual usage on an executive dashboard. Confirm `evidence/manifest.json` lists a SHA-256 hash for every evidence file.

### Step 6. Break It Safely
lab-changes/ adds 'hours saved per user' from a vendor survey with no evidence file. Apply it:
```
python ../../shared/scripts/start-lab.py 18.1 --apply lab-changes
```
Anything marked INTENTIONALLY INSECURE is for lab use only.

### Step 7. Observe
```
python run.py
```
Expected: `FAIL` with a blocking finding `metric-without-evidence`. Read the message: it names what changed and why it matters.

### Step 8. Remediate
Remove the metric or measure it.
```
python ../../shared/scripts/start-lab.py 18.1 --apply solution
```

### Step 9. Validate
```
python run.py
```
Expected: `PASS`. Prove the fix from the repository root as well:
```
python -m pytest -q "tests/test_lab_sequences.py::test_lab_sequence[18.1]"
```

## Expected Results
| Stage | Expected status |
|---|---|
| Starter | PASS |
| After your build or the solution | PASS |
| After lab-changes (break it safely) | FAIL (metric-without-evidence) |
| After remediation | PASS |

## Evidence
Dashboard markdown with sources. Keep the whole `evidence/` folder; the manifest lets a reviewer confirm nothing was edited after the run.

## Common Problems
- Metric paths use dot notation into the JSON.

## Security Considerations
Aggregate metrics; never show individual usage on an executive dashboard.

## Enterprise Application
Quarterly portfolio review.

## Production Considerations
Generate from the evidence store on a schedule.

## Cleanup
Delete `workspace/lab-18.1`. No cloud resources are created by the local lab.

## Further Challenge
Add trend lines from successive evidence packs.

---
Validation status: LOCALLY VALIDATED: the full sequence (starter, solution, break it safely, prove the fix) passed on 2026-10-07 with Python 3.13.16, pytest 8.4.2, PyYAML 6.0.3, using synthetic data only. GitHub Actions workflow: STATICALLY VALIDATED (actionlint 1.7.12); EXECUTION VALIDATION REQUIRED on a hosted runner.

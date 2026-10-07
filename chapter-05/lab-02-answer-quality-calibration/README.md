# Lab 5.2 Answer-Quality Calibration

**Book:** Chapter 5, section "5.2 The Semantic Index"
**Difficulty:** Level 2 (Build)
**Platform:** Local
**Effort:** 30 minutes
**Cloud tenant needed:** No
**API key needed:** No
**Data:** synthetic only (Harbourline Group is fictional; domain harbourline.example)

## What You Will Build
A calibration sheet and checker that classifies sampled answers and treats permission surprises as security findings.

## Why This Matters
Most quality problems are content or access problems. Classifying them routes them to the person who can fix them.

## Enterprise Scenario
Harbourline AP staff complain that Copilot quotes old payment terms.

## Learning Objectives
- Sample and classify answers
- Separate content faults from model faults
- Escalate permission surprises

## Prerequisites
- Python 3.11 or later and `pip install -r requirements.txt` from the repository root
- Lab 0.1 completed (you know how to read an evidence pack)
- The book section above read first: the lab tests the decision, not the reading

## Architecture
The lab follows the repository pattern: your inputs in `starter/`, a shared engine in `shared/playbook/`, and evidence written to `evidence/`.

```
inputs (YAML, CSV, JSON)  -->  run.py  -->  shared/playbook engine  -->  evidence/result.json, report.md, manifest.json
```

Core concept: Answer-quality cause classification.

## Repository Structure
```
chapter-05/lab-02-answer-quality-calibration/
  README.md
  lab.json
  starter/
    answers.csv
    run.py
  solution/
    answers.csv
  lab-changes/
    answers.csv
```

## Steps

### Step 1. Environment Setup
From the repository root:
```
python shared/scripts/start-lab.py 5.2
cd workspace/lab-5.2
```
This copies `starter/` into a workspace folder that git ignores, so you can break things freely.

### Step 2. Configure
Inspect answers.csv. The starter is a compliant baseline: your first run should PASS.
```
python run.py
```

### Step 3. Build
Classify five answers from your own pilot (synthetic copies). To compare with the reference, apply the solution:
```
python ../../shared/scripts/start-lab.py 5.2 --apply solution
```

### Step 4. Test
```
python run.py
```
Expected: `PASS`. Open `evidence/report.md` and `evidence/result.json`.

### Step 5. Secure
A permission surprise is a security event, not a quality metric. Confirm `evidence/manifest.json` lists a SHA-256 hash for every evidence file.

### Step 6. Break It Safely
lab-changes/ adds an answer that surfaced board papers. Apply it:
```
python ../../shared/scripts/start-lab.py 5.2 --apply lab-changes
```
Anything marked INTENTIONALLY INSECURE is for lab use only.

### Step 7. Observe
```
python run.py
```
Expected: `FAIL` with a blocking finding `permission-surprise`. Read the message: it names what changed and why it matters.

### Step 8. Remediate
Treat as an exposure finding (Lab 6.1) and remove from the calibration sample.
```
python ../../shared/scripts/start-lab.py 5.2 --apply solution
```

### Step 9. Validate
```
python run.py
```
Expected: `PASS`. Prove the fix from the repository root as well:
```
python -m pytest -q "tests/test_lab_sequences.py::test_lab_sequence[5.2]"
```

## Expected Results
| Stage | Expected status |
|---|---|
| Starter | PASS |
| After your build or the solution | PASS |
| After lab-changes (break it safely) | FAIL (permission-surprise) |
| After remediation | PASS |

## Evidence
Calibration report with cause distribution. Keep the whole `evidence/` folder; the manifest lets a reviewer confirm nothing was edited after the run.

## Common Problems
- Causes must use the listed values exactly.

## Security Considerations
A permission surprise is a security event, not a quality metric.

## Enterprise Application
Run calibration fortnightly during a pilot.

## Production Considerations
Feed failures into the evaluation set (Lab 12.1).

## Cleanup
Delete `workspace/lab-5.2`. No cloud resources are created by the local lab.

## Further Challenge
Add a cause for stale content and link it to an owner.

---
Validation status: LOCALLY VALIDATED: the full sequence (starter, solution, break it safely, prove the fix) passed on 2026-10-07 with Python 3.13.16, pytest 8.4.2, PyYAML 6.0.3, using synthetic data only. GitHub Actions workflow: STATICALLY VALIDATED (actionlint 1.7.12); EXECUTION VALIDATION REQUIRED on a hosted runner.

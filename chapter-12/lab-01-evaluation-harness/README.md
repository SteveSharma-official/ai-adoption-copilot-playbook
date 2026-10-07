# Lab 12.1 Evaluation Harness and Release Gate

**Book:** Chapter 12, section "12.2 The Evaluation Harness"
**Difficulty:** Level 5 (Evaluate)
**Platform:** Local (recorded responses)
**Effort:** 60 minutes
**Cloud tenant needed:** No (recorded responses); live runs need a tenant
**API key needed:** No
**Data:** synthetic only (Harbourline Group is fictional; domain harbourline.example)

## What You Will Build
An evaluation harness over a ten-case test set (core, edge, adversarial, regulated, operational) comparing candidate and previous versions.

## Why This Matters
You cannot prove a change is safe without a test that would have caught it being unsafe.

## Enterprise Scenario
A new prompt template for Harbourline's AP agent drops citations and lets an injected bank-detail change through.

## Learning Objectives
- Grade answer, refuse and approval expectations
- Block on adversarial and regulated failures
- Detect regressions

## Prerequisites
- Python 3.11 or later and `pip install -r requirements.txt` from the repository root
- Lab 0.1 completed (you know how to read an evidence pack)
- The book section above read first: the lab tests the decision, not the reading

## Architecture
The lab follows the repository pattern: your inputs in `starter/`, a shared engine in `shared/playbook/`, and evidence written to `evidence/`.

```
inputs (YAML, CSV, JSON)  -->  run.py  -->  shared/playbook engine  -->  evidence/result.json, report.md, manifest.json
```

Core concept: Evaluation harness and release gate.

## Repository Structure
```
chapter-12/lab-01-evaluation-harness/
  README.md
  lab.json
  starter/
    responses/candidate.jsonl
    responses/previous.jsonl
    run.py
    testset.yaml
    thresholds.yaml
  solution/
    responses/candidate.jsonl
  lab-changes/
    responses/candidate.jsonl
```

## Steps

### Step 1. Environment Setup
From the repository root:
```
python shared/scripts/start-lab.py 12.1
cd workspace/lab-12.1
```
This copies `starter/` into a workspace folder that git ignores, so you can break things freely.

### Step 2. Configure
Inspect testset.yaml, thresholds.yaml, responses/. The starter is a compliant baseline: your first run should PASS.
```
python run.py
```

### Step 3. Build
Add five cases from your own pilot failures. To compare with the reference, apply the solution:
```
python ../../shared/scripts/start-lab.py 12.1 --apply solution
```

### Step 4. Test
```
python run.py
```
Expected: `PASS`. Open `evidence/report.md` and `evidence/result.json`.

### Step 5. Secure
Adversarial cases must never be shortened to pass. Confirm `evidence/manifest.json` lists a SHA-256 hash for every evidence file.

### Step 6. Break It Safely
lab-changes/ evaluates version 2.0. Apply it:
```
python ../../shared/scripts/start-lab.py 12.1 --apply lab-changes
```
Anything marked INTENTIONALLY INSECURE is for lab use only.

### Step 7. Observe
```
python run.py
```
Expected: `FAIL` with a blocking finding `hard-fail`. Read the message: it names what changed and why it matters.

### Step 8. Remediate
Do not release 2.0; fix and re-evaluate.
```
python ../../shared/scripts/start-lab.py 12.1 --apply solution
```

### Step 9. Validate
```
python run.py
```
Expected: `PASS`. Prove the fix from the repository root as well:
```
python -m pytest -q "tests/test_lab_sequences.py::test_lab_sequence[12.1]"
```

## Expected Results
| Stage | Expected status |
|---|---|
| Starter | PASS |
| After your build or the solution | PASS |
| After lab-changes (break it safely) | FAIL (hard-fail) |
| After remediation | PASS |

## Evidence
Scorecard with failures and regressions. Keep the whole `evidence/` folder; the manifest lets a reviewer confirm nothing was edited after the run.

## Common Problems
- Responses are recorded fixtures. Live evaluation needs your agent and is EXECUTION VALIDATION REQUIRED.

## Security Considerations
Adversarial cases must never be shortened to pass.

## Enterprise Application
No release without a scorecard ID (Lab 17.2).

## Production Considerations
Grow the set with every production failure; target 100+ cases.

## Cleanup
Delete `workspace/lab-12.1`. No cloud resources are created by the local lab.

## Further Challenge
Add a cost and latency category.

---
Validation status: LOCALLY VALIDATED: the full sequence (starter, solution, break it safely, prove the fix) passed on 2026-10-07 with Python 3.13.16, pytest 8.4.2, PyYAML 6.0.3, using synthetic data only. GitHub Actions workflow: STATICALLY VALIDATED (actionlint 1.7.12); EXECUTION VALIDATION REQUIRED on a hosted runner.

# Lab 13.1 Regulator-Ready Decision Records (Financial Services)

**Book:** Chapter 13, section "13.3 Designing the Regulator-Ready Audit Trail"
**Difficulty:** Level 6 (Govern)
**Platform:** Local
**Effort:** 60 minutes
**Cloud tenant needed:** No
**API key needed:** No
**Data:** synthetic only (Harbourline Group is fictional; domain harbourline.example)

## What You Will Build
A record generator for synthetic hardship decisions that checks the policy version in force, citations, and human decision with reasons.

## Why This Matters
When the regulator asks why, the answer must exist before the question.

## Enterprise Scenario
Harbourline Finance (fictional lender) changed its hardship policy on 1 July. One agent draft still cites the old version.

## Learning Objectives
- Determine the policy in force on a date
- Require human decision and reasons
- Verify a hash chain

## Prerequisites
- Python 3.11 or later and `pip install -r requirements.txt` from the repository root
- Lab 0.1 completed (you know how to read an evidence pack)
- The book section above read first: the lab tests the decision, not the reading

## Architecture
The lab follows the repository pattern: your inputs in `starter/`, a shared engine in `shared/playbook/`, and evidence written to `evidence/`.

```
inputs (YAML, CSV, JSON)  -->  run.py  -->  shared/playbook engine  -->  evidence/result.json, report.md, manifest.json
```

Core concept: Regulator-ready decision records.

## Repository Structure
```
chapter-13/lab-01-fs-decision-record/
  README.md
  lab.json
  starter/
    cases.json
    policy-versions.yaml
    run.py
  solution/
    cases.json
  lab-changes/
    cases.json
```

## Steps

### Step 1. Environment Setup
From the repository root:
```
python shared/scripts/start-lab.py 13.1
cd workspace/lab-13.1
```
This copies `starter/` into a workspace folder that git ignores, so you can break things freely.

### Step 2. Configure
Inspect cases.json and policy-versions.yaml. The starter is a compliant baseline: your first run should PASS.
```
python run.py
```

### Step 3. Build
Add a case of your own. To compare with the reference, apply the solution:
```
python ../../shared/scripts/start-lab.py 13.1 --apply solution
```

### Step 4. Test
```
python run.py
```
Expected: `PASS`. Open `evidence/report.md` and `evidence/result.json`.

### Step 5. Secure
Not legal advice. Confirm record-keeping obligations with your compliance team. Confirm `evidence/manifest.json` lists a SHA-256 hash for every evidence file.

### Step 6. Break It Safely
lab-changes/ makes one post-July draft cite v3. Apply it:
```
python ../../shared/scripts/start-lab.py 13.1 --apply lab-changes
```
Anything marked INTENTIONALLY INSECURE is for lab use only.

### Step 7. Observe
```
python run.py
```
Expected: `FAIL` with a blocking finding `record-defect`. Read the message: it names what changed and why it matters.

### Step 8. Remediate
Re-draft against the policy in force and re-record.
```
python ../../shared/scripts/start-lab.py 13.1 --apply solution
```

### Step 9. Validate
```
python run.py
```
Expected: `PASS`. Prove the fix from the repository root as well:
```
python -m pytest -q "tests/test_lab_sequences.py::test_lab_sequence[13.1]"
```

## Expected Results
| Stage | Expected status |
|---|---|
| Starter | PASS |
| After your build or the solution | PASS |
| After lab-changes (break it safely) | FAIL (record-defect) |
| After remediation | PASS |

## Evidence
Decision records (JSONL hash chain), defect report. Keep the whole `evidence/` folder; the manifest lets a reviewer confirm nothing was edited after the run.

## Common Problems
- Hash chains break if a record is edited; that is the point.

## Security Considerations
Not legal advice. Confirm record-keeping obligations with your compliance team.

## Enterprise Application
Store records in a system of record with retention.

## Production Considerations
Anchor the chain head periodically in an independent log.

## Cleanup
Delete `workspace/lab-13.1`. No cloud resources are created by the local lab.

## Further Challenge
Add a check that the decision-maker holds the delegation for the amount.

---
Validation status: LOCALLY VALIDATED: the full sequence (starter, solution, break it safely, prove the fix) passed on 2026-10-07 with Python 3.13.16, pytest 8.4.2, PyYAML 6.0.3, using synthetic data only. GitHub Actions workflow: STATICALLY VALIDATED (actionlint 1.7.12); EXECUTION VALIDATION REQUIRED on a hosted runner.

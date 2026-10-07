# Lab 14.1 Clinical Documentation Boundary Tests (Healthcare)

**Book:** Chapter 14, section "14.3 Navigating the Medical Device Boundary"
**Difficulty:** Level 5 (Evaluate)
**Platform:** Local
**Effort:** 45 minutes
**Cloud tenant needed:** No
**API key needed:** No
**Data:** synthetic only (Harbourline Group is fictional; domain harbourline.example)

## What You Will Build
Checks over synthetic notes and drafts for doses not present in source, recommendation language and missing citations.

## Why This Matters
The clinician still signs. The assistant must never write what the clinician did not decide.

## Enterprise Scenario
A synthetic ward-round note says metoprolol 25 mg continued. A draft says 'consider increasing to 50 mg'.

## Learning Objectives
- Detect unsupported doses
- Detect recommendation language
- Require decline-and-redirect

## Prerequisites
- Python 3.11 or later and `pip install -r requirements.txt` from the repository root
- Lab 0.1 completed (you know how to read an evidence pack)
- The book section above read first: the lab tests the decision, not the reading

## Architecture
The lab follows the repository pattern: your inputs in `starter/`, a shared engine in `shared/playbook/`, and evidence written to `evidence/`.

```
inputs (YAML, CSV, JSON)  -->  run.py  -->  shared/playbook engine  -->  evidence/result.json, report.md, manifest.json
```

Core concept: Clinical documentation boundary.

## Repository Structure
```
chapter-14/lab-01-clinical-boundary-tests/
  README.md
  lab.json
  starter/
    drafts.json
    notes.json
    regulated-prompts.yaml
    responses.json
    run.py
  solution/
    drafts.json
  lab-changes/
    drafts.json
```

## Steps

### Step 1. Environment Setup
From the repository root:
```
python shared/scripts/start-lab.py 14.1
cd workspace/lab-14.1
```
This copies `starter/` into a workspace folder that git ignores, so you can break things freely.

### Step 2. Configure
Inspect notes.json, drafts.json, regulated-prompts.yaml. The starter is a compliant baseline: your first run should PASS.
```
python run.py
```

### Step 3. Build
Add a draft and note pair of your own (synthetic). To compare with the reference, apply the solution:
```
python ../../shared/scripts/start-lab.py 14.1 --apply solution
```

### Step 4. Test
```
python run.py
```
Expected: `PASS`. Open `evidence/report.md` and `evidence/result.json`.

### Step 5. Secure
Never use real patient data in labs. Confirm whether your use is regulated as a medical device with your regulator. Confirm `evidence/manifest.json` lists a SHA-256 hash for every evidence file.

### Step 6. Break It Safely
lab-changes/ introduces a draft with a recommendation and a new dose. Apply it:
```
python ../../shared/scripts/start-lab.py 14.1 --apply lab-changes
```
Anything marked INTENTIONALLY INSECURE is for lab use only.

### Step 7. Observe
```
python run.py
```
Expected: `FAIL` with a blocking finding `draft-boundary`. Read the message: it names what changed and why it matters.

### Step 8. Remediate
Reject the draft; tighten the instruction and re-test.
```
python ../../shared/scripts/start-lab.py 14.1 --apply solution
```

### Step 9. Validate
```
python run.py
```
Expected: `PASS`. Prove the fix from the repository root as well:
```
python -m pytest -q "tests/test_lab_sequences.py::test_lab_sequence[14.1]"
```

## Expected Results
| Stage | Expected status |
|---|---|
| Starter | PASS |
| After your build or the solution | PASS |
| After lab-changes (break it safely) | FAIL (draft-boundary) |
| After remediation | PASS |

## Evidence
Boundary report. Keep the whole `evidence/` folder; the manifest lets a reviewer confirm nothing was edited after the run.

## Common Problems
- The regexes are illustrative and will miss paraphrases. This is a documentation-quality test, not a regulatory classification tool.

## Security Considerations
Never use real patient data in labs. Confirm whether your use is regulated as a medical device with your regulator.

## Enterprise Application
Clinical safety officer signs the boundary tests.

## Production Considerations
Sample drafts for human audit regardless of test results.

## Cleanup
Delete `workspace/lab-14.1`. No cloud resources are created by the local lab.

## Further Challenge
Add allergy statements to the source-presence check.

---
Validation status: LOCALLY VALIDATED: the full sequence (starter, solution, break it safely, prove the fix) passed on 2026-10-07 with Python 3.13.16, pytest 8.4.2, PyYAML 6.0.3, using synthetic data only. GitHub Actions workflow: STATICALLY VALIDATED (actionlint 1.7.12); EXECUTION VALIDATION REQUIRED on a hosted runner.

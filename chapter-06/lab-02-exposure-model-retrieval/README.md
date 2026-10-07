# Lab 6.2 The Five Layers of the Copilot Data Exposure Model, Tested

**Book:** Chapter 6, section "6.2 How a Locked File Stays Reachable"
**Difficulty:** Level 4 (Secure)
**Platform:** Local (pytest)
**Effort:** 45 minutes
**Cloud tenant needed:** No
**API key needed:** No
**Data:** synthetic only (Harbourline Group is fictional; domain harbourline.example)

## What You Will Build
A teaching retriever and six pytest tests covering access, discovery, protection and processing layers.

## Why This Matters
Tests make the model precise. If a statement about a layer cannot be written as a test, it is not yet understood.

## Enterprise Scenario
Harbourline's CISO asks: 'If we put RCD on the restructure site, can anyone still open it?'

## Learning Objectives
- Show RCD hides from search but not from direct open
- Show EXTRACT rights limit summarisation
- Prove no layer ever grants access

## Prerequisites
- Python 3.11 or later and `pip install -r requirements.txt` from the repository root
- Lab 0.1 completed (you know how to read an evidence pack)
- The book section above read first: the lab tests the decision, not the reading

## Architecture
The lab follows the repository pattern: your inputs in `starter/`, a shared engine in `shared/playbook/`, and evidence written to `evidence/`.

```
inputs (YAML, CSV, JSON)  -->  run.py  -->  shared/playbook engine  -->  evidence/result.json, report.md, manifest.json
```

Core concept: The five exposure layers, tested.

## Repository Structure
```
chapter-06/lab-02-exposure-model-retrieval/
  README.md
  lab.json
  starter/
    retrieval.yaml
    run.py
    test_layers.py
  solution/
    retrieval.yaml
  lab-changes/
    retrieval.yaml
```

## Steps

### Step 1. Environment Setup
From the repository root:
```
python shared/scripts/start-lab.py 6.2
cd workspace/lab-6.2
```
This copies `starter/` into a workspace folder that git ignores, so you can break things freely.

### Step 2. Configure
Inspect retrieval.yaml and test_layers.py. The starter is a compliant baseline: your first run should PASS.
```
python run.py
```

### Step 3. Build
Add a test for the lifecycle layer of your own design. To compare with the reference, apply the solution:
```
python ../../shared/scripts/start-lab.py 6.2 --apply solution
```

### Step 4. Test
```
python run.py
```
Expected: `PASS`. Open `evidence/report.md` and `evidence/result.json`.

### Step 5. Secure
INTENTIONALLY INSECURE configuration in lab-changes/ is for lab use only. Confirm `evidence/manifest.json` lists a SHA-256 hash for every evidence file.

### Step 6. Break It Safely
lab-changes/ disables permission trimming ('trimming hurts relevance'). Apply it:
```
python ../../shared/scripts/start-lab.py 6.2 --apply lab-changes
```
Anything marked INTENTIONALLY INSECURE is for lab use only.

### Step 7. Observe
```
python run.py
```
Expected: `FAIL` with a blocking finding `layer-test-failed`. Read the message: it names what changed and why it matters.

### Step 8. Remediate
Restore prefilter access control.
```
python ../../shared/scripts/start-lab.py 6.2 --apply solution
```

### Step 9. Validate
```
python run.py
```
Expected: `PASS`. Prove the fix from the repository root as well:
```
python -m pytest -q "tests/test_lab_sequences.py::test_lab_sequence[6.2]"
```

## Expected Results
| Stage | Expected status |
|---|---|
| Starter | PASS |
| After your build or the solution | PASS |
| After lab-changes (break it safely) | FAIL (layer-test-failed) |
| After remediation | PASS |

## Evidence
pytest output in report.md. Keep the whole `evidence/` folder; the manifest lets a reviewer confirm nothing was edited after the run.

## Common Problems
- Run tests from the lab folder or via run.py.

## Security Considerations
INTENTIONALLY INSECURE configuration in lab-changes/ is for lab use only.

## Enterprise Application
Use the tests to explain controls to auditors in plain behaviour.

## Production Considerations
Equivalent behaviour tests belong in any custom retrieval (RAG) build.

## Cleanup
Delete `workspace/lab-6.2`. No cloud resources are created by the local lab.

## Further Challenge
Add a test for a guest user and an org-wide link.

---
Validation status: LOCALLY VALIDATED: the full sequence (starter, solution, break it safely, prove the fix) passed on 2026-10-07 with Python 3.13.16, pytest 8.4.2, PyYAML 6.0.3, using synthetic data only. GitHub Actions workflow: STATICALLY VALIDATED (actionlint 1.7.12); EXECUTION VALIDATION REQUIRED on a hosted runner.

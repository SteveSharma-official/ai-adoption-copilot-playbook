# Lab 0.1 Quick Start: Your First Evidence Pack

**Book:** Introduction, section "How the book, templates and labs work together"
**Difficulty:** Level 1 (Explore)
**Platform:** Local (Python 3.11+)
**Effort:** 15 minutes
**Cloud tenant needed:** No
**API key needed:** No
**Data:** synthetic only (Harbourline Group is fictional; domain harbourline.example)

## What You Will Build
An environment check that confirms the synthetic Harbourline datasets are present and writes your first evidence pack.

## Why This Matters
Every later lab ends in the same evidence shape. Learning it once, with nothing at stake, makes the rest of the book practical.

## Enterprise Scenario
You have joined the Harbourline Group (fictional) Copilot programme as its governance lead. The first thing the programme director asks for is proof that the tooling works.

## Learning Objectives
- Run a lab from its starter folder
- Read a PASS or FAIL result and its findings
- Explain why each evidence pack has a named owner and a hash manifest

## Prerequisites
- Python 3.11 or later and `pip install -r requirements.txt` from the repository root
- Lab 0.1 completed (you know how to read an evidence pack)
- The book section above read first: the lab tests the decision, not the reading

## Architecture
The lab follows the repository pattern: your inputs in `starter/`, a shared engine in `shared/playbook/`, and evidence written to `evidence/`.

```
inputs (YAML, CSV, JSON)  -->  run.py  -->  shared/playbook engine  -->  evidence/result.json, report.md, manifest.json
```

Core concept: Evidence-first lab method.

## Repository Structure
```
chapter-00/lab-01-quick-start/
  README.md
  lab.json
  starter/
    lab.yaml
    run.py
  solution/
    lab.yaml
  lab-changes/
    lab.yaml
```

## Steps

### Step 1. Environment Setup
From the repository root:
```
python shared/scripts/start-lab.py 0.1
cd workspace/lab-0.1
```
This copies `starter/` into a workspace folder that git ignores, so you can break things freely.

### Step 2. Configure
Inspect lab.yaml (evidence owner) and shared/datasets/harbourline. The starter is a compliant baseline: your first run should PASS.
```
python run.py
```

### Step 3. Build
Set evidence_owner in lab.yaml to your own name. To compare with the reference, apply the solution:
```
python ../../shared/scripts/start-lab.py 0.1 --apply solution
```

### Step 4. Test
```
python run.py
```
Expected: `PASS`. Open `evidence/report.md` and `evidence/result.json`.

### Step 5. Secure
Synthetic data only. Never copy tenant exports into the public repository. Confirm `evidence/manifest.json` lists a SHA-256 hash for every evidence file.

### Step 6. Break It Safely
lab-changes/ blanks the evidence owner. Apply it:
```
python ../../shared/scripts/start-lab.py 0.1 --apply lab-changes
```
Anything marked INTENTIONALLY INSECURE is for lab use only.

### Step 7. Observe
```
python run.py
```
Expected: `FAIL` with a blocking finding `no-evidence-owner`. Read the message: it names what changed and why it matters.

### Step 8. Remediate
Restore a named evidence owner.
```
python ../../shared/scripts/start-lab.py 0.1 --apply solution
```

### Step 9. Validate
```
python run.py
```
Expected: `PASS`. Prove the fix from the repository root as well:
```
python -m pytest -q "tests/test_lab_sequences.py::test_lab_sequence[0.1]"
```

## Expected Results
| Stage | Expected status |
|---|---|
| Starter | PASS |
| After your build or the solution | PASS |
| After lab-changes (break it safely) | FAIL (no-evidence-owner) |
| After remediation | PASS |

## Evidence
result.json, report.md, manifest.json (SHA-256). Keep the whole `evidence/` folder; the manifest lets a reviewer confirm nothing was edited after the run.

## Common Problems
- ModuleNotFoundError: yaml. Run pip install -r requirements.txt.
- Datasets missing. Run python shared/scripts/generate_datasets.py.

## Security Considerations
Synthetic data only. Never copy tenant exports into the public repository.

## Enterprise Application
Agree a single evidence format for the programme before the first pilot.

## Production Considerations
Store evidence packs in a records system with retention, not on laptops.

## Cleanup
Delete `workspace/lab-0.1`. No cloud resources are created by the local lab.

## Further Challenge
Add a check that fails if any file in your evidence folder contains a real email domain.

---
Validation status: LOCALLY VALIDATED: the full sequence (starter, solution, break it safely, prove the fix) passed on 2026-10-07 with Python 3.13.16, pytest 8.4.2, PyYAML 6.0.3, using synthetic data only. GitHub Actions workflow: STATICALLY VALIDATED (actionlint 1.7.12); EXECUTION VALIDATION REQUIRED on a hosted runner.

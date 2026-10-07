# Lab 4.1 Workload-to-Platform Decision Ladder

**Book:** Chapter 4, section "4.2 The AI Adoption Decision Ladder"
**Difficulty:** Level 2 (Build)
**Platform:** Local
**Effort:** 30 minutes
**Cloud tenant needed:** No
**API key needed:** No
**Data:** synthetic only (Harbourline Group is fictional; domain harbourline.example)

## What You Will Build
A ladder engine that computes the minimum rung for each workload and flags unjustified climbs and under-scoping.

## Why This Matters
Every rung up adds cost, ownership and risk. The ladder makes that trade explicit.

## Enterprise Scenario
A Harbourline team proposes building a custom app for meeting recaps that Copilot already provides.

## Learning Objectives
- Derive the minimum rung from requirements
- Detect an unjustified climb
- Flag consumption-billed surfaces

## Prerequisites
- Python 3.11 or later and `pip install -r requirements.txt` from the repository root
- Lab 0.1 completed (you know how to read an evidence pack)
- The book section above read first: the lab tests the decision, not the reading

## Architecture
The lab follows the repository pattern: your inputs in `starter/`, a shared engine in `shared/playbook/`, and evidence written to `evidence/`.

```
inputs (YAML, CSV, JSON)  -->  run.py  -->  shared/playbook engine  -->  evidence/result.json, report.md, manifest.json
```

Core concept: AI Adoption Decision Ladder (Buy, Configure, Integrate, Build, Host).

## Repository Structure
```
chapter-04/lab-01-decision-ladder/
  README.md
  lab.json
  starter/
    run.py
    workloads.yaml
  solution/
    workloads.yaml
  lab-changes/
    workloads.yaml
```

## Steps

### Step 1. Environment Setup
From the repository root:
```
python shared/scripts/start-lab.py 4.1
cd workspace/lab-4.1
```
This copies `starter/` into a workspace folder that git ignores, so you can break things freely.

### Step 2. Configure
Inspect workloads.yaml. The starter is a compliant baseline: your first run should PASS.
```
python run.py
```

### Step 3. Build
Add requirements flags for one workload of your own. To compare with the reference, apply the solution:
```
python ../../shared/scripts/start-lab.py 4.1 --apply solution
```

### Step 4. Test
```
python run.py
```
Expected: `PASS`. Open `evidence/report.md` and `evidence/result.json`.

### Step 5. Secure
Higher rungs need their own threat model (Lab 8.2). Confirm `evidence/manifest.json` lists a SHA-256 hash for every evidence file.

### Step 6. Break It Safely
lab-changes/ moves Meeting recap to Build. Apply it:
```
python ../../shared/scripts/start-lab.py 4.1 --apply lab-changes
```
Anything marked INTENTIONALLY INSECURE is for lab use only.

### Step 7. Observe
```
python run.py
```
Expected: `FAIL` with a blocking finding `unjustified-climb`. Read the message: it names what changed and why it matters.

### Step 8. Remediate
Return it to Buy.
```
python ../../shared/scripts/start-lab.py 4.1 --apply solution
```

### Step 9. Validate
```
python run.py
```
Expected: `PASS`. Prove the fix from the repository root as well:
```
python -m pytest -q "tests/test_lab_sequences.py::test_lab_sequence[4.1]"
```

## Expected Results
| Stage | Expected status |
|---|---|
| Starter | PASS |
| After your build or the solution | PASS |
| After lab-changes (break it safely) | FAIL (unjustified-climb) |
| After remediation | PASS |

## Evidence
Ladder report. Keep the whole `evidence/` folder; the manifest lets a reviewer confirm nothing was edited after the run.

## Common Problems
- Unknown rung names fail validation; use the five rung names exactly.

## Security Considerations
Higher rungs need their own threat model (Lab 8.2).

## Enterprise Application
Make the ladder result a required field on the AI intake form.

## Production Considerations
Revisit when platform capability changes; a Build may become a Configure.

## Cleanup
Delete `workspace/lab-4.1`. No cloud resources are created by the local lab.

## Further Challenge
Add Host-rung triggers for data residency or model control.

---
Validation status: LOCALLY VALIDATED: the full sequence (starter, solution, break it safely, prove the fix) passed on 2026-10-07 with Python 3.13.16, pytest 8.4.2, PyYAML 6.0.3, using synthetic data only. GitHub Actions workflow: STATICALLY VALIDATED (actionlint 1.7.12); EXECUTION VALIDATION REQUIRED on a hosted runner.

# Lab 17.2 Agent Change Pipeline: No Release Without Evaluation (Tenant)

**Book:** Chapter 17, section "17.3 Change Management for Autonomous Systems"
**Difficulty:** Level 7 (Deploy)
**Platform:** Power Platform pipelines (tenant) plus local checker
**Effort:** 2 hours (tenant)
**Cloud tenant needed:** Yes
**API key needed:** No
**Data:** synthetic only (Harbourline Group is fictional; domain harbourline.example)

> **Tenant required for the build steps.** Use a non-production Microsoft 365 or Power Platform environment you are authorised to change. Licensing and preview features vary; confirm against current Microsoft documentation. The synthetic sample in starter/ lets you complete the local checker without a tenant.

## What You Will Build
A release pipeline for an agent (in your own tenant) and a checker that every change cites an evaluation run.

## Why This Matters
A prompt is code. Changing it without a test is a production change without a test.

## Enterprise Scenario
A Friday-afternoon prompt hotfix for Harbourline's AP agent goes out without evaluation.

## Learning Objectives
- Promote agents through environments
- Record approval and evaluation per change
- Block unevaluated releases

## Prerequisites
- Python 3.11 or later and `pip install -r requirements.txt` from the repository root
- Lab 0.1 completed (you know how to read an evidence pack)
- The book section above read first: the lab tests the decision, not the reading

## Architecture
The lab follows the repository pattern: your inputs in `starter/`, a shared engine in `shared/playbook/`, and evidence written to `evidence/`.

```
inputs (YAML, CSV, JSON)  -->  run.py  -->  shared/playbook engine  -->  evidence/result.json, report.md, manifest.json
```

Core concept: Agent change pipeline.

## Repository Structure
```
chapter-17/lab-02-agent-change-pipeline/
  README.md
  lab.json
  starter/
    change-log.csv
    run.py
  solution/
    change-log.csv
  lab-changes/
    change-log.csv
```

## Steps

### Step 1. Environment Setup
From the repository root:
```
python shared/scripts/start-lab.py 17.2
cd workspace/lab-17.2
```
This copies `starter/` into a workspace folder that git ignores, so you can break things freely.

### Step 2. Configure
Inspect change-log.csv (synthetic sample). The starter is a compliant baseline: your first run should PASS.
```
python run.py
```

### Step 3. Build
In a non-production tenant, configure a pipeline and export the change log. To compare with the reference, apply the solution:
```
python ../../shared/scripts/start-lab.py 17.2 --apply solution
```

### Step 4. Test
```
python run.py
```
Expected: `PASS`. Open `evidence/report.md` and `evidence/result.json`.

### Step 5. Secure
Use separate environments with data policies. Confirm `evidence/manifest.json` lists a SHA-256 hash for every evidence file.

### Step 6. Break It Safely
lab-changes/ adds a hotfix with no evaluation run. Apply it:
```
python ../../shared/scripts/start-lab.py 17.2 --apply lab-changes
```
Anything marked INTENTIONALLY INSECURE is for lab use only.

### Step 7. Observe
```
python run.py
```
Expected: `FAIL` with a blocking finding `no-evaluation-run`. Read the message: it names what changed and why it matters.

### Step 8. Remediate
Run Lab 12.1 against the change and record its ID.
```
python ../../shared/scripts/start-lab.py 17.2 --apply solution
```

### Step 9. Validate
```
python run.py
```
Expected: `PASS`. Prove the fix from the repository root as well:
```
python -m pytest -q "tests/test_lab_sequences.py::test_lab_sequence[17.2]"
```

## Expected Results
| Stage | Expected status |
|---|---|
| Starter | PASS |
| After your build or the solution | PASS |
| After lab-changes (break it safely) | FAIL (no-evaluation-run) |
| After remediation | PASS |

## Evidence
Change-log check. Keep the whole `evidence/` folder; the manifest lets a reviewer confirm nothing was edited after the run.

## Common Problems
- Pipeline features vary by licence and region; confirm before building.

## Security Considerations
Use separate environments with data policies.

## Enterprise Application
Change advisory board accepts the evaluation ID as evidence.

## Production Considerations
Make the evaluation ID a required pipeline parameter.

## Cleanup
Delete `workspace/lab-17.2`. No cloud resources are created by the local lab. If you built the tenant steps, delete the test agent, flow and environment you created, and remove any test users or connections.

## Further Challenge
Add automatic rollback when post-release monitoring fails.

---
Validation status: LOCALLY VALIDATED: the full sequence (starter, solution, break it safely, prove the fix) passed on 2026-10-07 with Python 3.13.16, pytest 8.4.2, PyYAML 6.0.3, using synthetic data only. Tenant steps (building in Microsoft 365 or Power Platform): CLOUD VALIDATION REQUIRED. GitHub Actions workflow: STATICALLY VALIDATED (actionlint 1.7.12); EXECUTION VALIDATION REQUIRED on a hosted runner.

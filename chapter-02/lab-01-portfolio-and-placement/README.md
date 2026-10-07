# Lab 2.1 Enterprise AI Portfolio Map and Workload Placement

**Book:** Chapter 2, section "2.2 Defining the Workload Placement Map"
**Difficulty:** Level 2 (Build)
**Platform:** Local
**Effort:** 45 minutes
**Cloud tenant needed:** No
**API key needed:** No
**Data:** synthetic only (Harbourline Group is fictional; domain harbourline.example)

## What You Will Build
A placement engine that recommends a zone for each workload and flags forced fits and shadow AI.

## Why This Matters
Copilot is one part of the AI estate. Placement decisions made on data and autonomy avoid expensive rework.

## Enterprise Scenario
Harbourline's analytics team wants telemetry sentiment analysis 'in Copilot'. The data lives in a data platform outside Microsoft 365.

## Learning Objectives
- Score a workload on three placement dimensions
- Detect a forced fit
- Report shadow AI without blame

## Prerequisites
- Python 3.11 or later and `pip install -r requirements.txt` from the repository root
- Lab 0.1 completed (you know how to read an evidence pack)
- The book section above read first: the lab tests the decision, not the reading

## Architecture
The lab follows the repository pattern: your inputs in `starter/`, a shared engine in `shared/playbook/`, and evidence written to `evidence/`.

```
inputs (YAML, CSV, JSON)  -->  run.py  -->  shared/playbook engine  -->  evidence/result.json, report.md, manifest.json
```

Core concept: Workload Placement Map and enterprise AI portfolio.

## Repository Structure
```
chapter-02/lab-01-portfolio-and-placement/
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
python shared/scripts/start-lab.py 2.1
cd workspace/lab-2.1
```
This copies `starter/` into a workspace folder that git ignores, so you can break things freely.

### Step 2. Configure
Inspect workloads.yaml and the synthetic proxy summary. The starter is a compliant baseline: your first run should PASS.
```
python run.py
```

### Step 3. Build
Add one of your own workloads with its data boundary and autonomy. To compare with the reference, apply the solution:
```
python ../../shared/scripts/start-lab.py 2.1 --apply solution
```

### Step 4. Test
```
python run.py
```
Expected: `PASS`. Open `evidence/report.md` and `evidence/result.json`.

### Step 5. Secure
Proxy summaries can identify individuals; aggregate before sharing. Confirm `evidence/manifest.json` lists a SHA-256 hash for every evidence file.

### Step 6. Break It Safely
lab-changes/ moves the telemetry workload onto Microsoft 365 Copilot. Apply it:
```
python ../../shared/scripts/start-lab.py 2.1 --apply lab-changes
```
Anything marked INTENTIONALLY INSECURE is for lab use only.

### Step 7. Observe
```
python run.py
```
Expected: `FAIL` with a blocking finding `forced-fit`. Read the message: it names what changed and why it matters.

### Step 8. Remediate
Place the workload on the platform where the data lives.
```
python ../../shared/scripts/start-lab.py 2.1 --apply solution
```

### Step 9. Validate
```
python run.py
```
Expected: `PASS`. Prove the fix from the repository root as well:
```
python -m pytest -q "tests/test_lab_sequences.py::test_lab_sequence[2.1]"
```

## Expected Results
| Stage | Expected status |
|---|---|
| Starter | PASS |
| After your build or the solution | PASS |
| After lab-changes (break it safely) | FAIL (forced-fit) |
| After remediation | PASS |

## Evidence
Placement report, shadow-AI summary. Keep the whole `evidence/` folder; the manifest lets a reviewer confirm nothing was edited after the run.

## Common Problems
- approved_exception must name a review and date to count.

## Security Considerations
Proxy summaries can identify individuals; aggregate before sharing.

## Enterprise Application
Bring the map to the architecture board with every new AI request.

## Production Considerations
Refresh shadow-AI data monthly; treat new tools as demand signals.

## Cleanup
Delete `workspace/lab-2.1`. No cloud resources are created by the local lab.

## Further Challenge
Add a cost dimension and flag workloads whose placement doubles data egress.

---
Validation status: LOCALLY VALIDATED: the full sequence (starter, solution, break it safely, prove the fix) passed on 2026-10-07 with Python 3.13.16, pytest 8.4.2, PyYAML 6.0.3, using synthetic data only. GitHub Actions workflow: STATICALLY VALIDATED (actionlint 1.7.12); EXECUTION VALIDATION REQUIRED on a hosted runner.

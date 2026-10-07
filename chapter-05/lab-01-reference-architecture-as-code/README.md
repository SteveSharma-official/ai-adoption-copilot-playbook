# Lab 5.1 Enterprise AI Reference Architecture as Code

**Book:** Chapter 5, section "5.3 The Microsoft Agent Control Plane"
**Difficulty:** Level 3 (Integrate)
**Platform:** Local
**Effort:** 60 minutes
**Cloud tenant needed:** No
**API key needed:** No
**Data:** synthetic only (Harbourline Group is fictional; domain harbourline.example)

## What You Will Build
A YAML architecture for the AP supplier query agent, validated for accountability, boundary controls and control-plane coverage, rendered as Mermaid.

## Why This Matters
If the architecture is data, review becomes a test and drift becomes a failing build.

## Enterprise Scenario
Harbourline's architecture board wants to approve the AP agent design before any connector is built.

## Learning Objectives
- Model components, zones and flows
- Detect an uncontrolled boundary crossing
- Check all five control-plane domains are covered

## Prerequisites
- Python 3.11 or later and `pip install -r requirements.txt` from the repository root
- Lab 0.1 completed (you know how to read an evidence pack)
- The book section above read first: the lab tests the decision, not the reading

## Architecture
The lab follows the repository pattern: your inputs in `starter/`, a shared engine in `shared/playbook/`, and evidence written to `evidence/`.

```
inputs (YAML, CSV, JSON)  -->  run.py  -->  shared/playbook engine  -->  evidence/result.json, report.md, manifest.json
```

Core concept: Reference architecture as code, Microsoft Agent Control Plane.

## Repository Structure
```
chapter-05/lab-01-reference-architecture-as-code/
  README.md
  lab.json
  starter/
    architecture.yaml
    run.py
  solution/
    architecture.yaml
  lab-changes/
    architecture.yaml
```

## Steps

### Step 1. Environment Setup
From the repository root:
```
python shared/scripts/start-lab.py 5.1
cd workspace/lab-5.1
```
This copies `starter/` into a workspace folder that git ignores, so you can break things freely.

### Step 2. Configure
Inspect architecture.yaml. The starter is a compliant baseline: your first run should PASS.
```
python run.py
```

### Step 3. Build
Add a component and flow for one more data source with its controls. To compare with the reference, apply the solution:
```
python ../../shared/scripts/start-lab.py 5.1 --apply solution
```

### Step 4. Test
```
python run.py
```
Expected: `PASS`. Open `evidence/report.md` and `evidence/result.json`.

### Step 5. Secure
Never let a diagram show a control that is not configured; link each control to evidence. Confirm `evidence/manifest.json` lists a SHA-256 hash for every evidence file.

### Step 6. Break It Safely
lab-changes/ adds an agent write to the ERP supplier master with no approval control. Apply it:
```
python ../../shared/scripts/start-lab.py 5.1 --apply lab-changes
```
Anything marked INTENTIONALLY INSECURE is for lab use only.

### Step 7. Observe
```
python run.py
```
Expected: `FAIL` with a blocking finding `write-without-approval`. Read the message: it names what changed and why it matters.

### Step 8. Remediate
Remove the write or add a human-approval control and an authority-matrix entry.
```
python ../../shared/scripts/start-lab.py 5.1 --apply solution
```

### Step 9. Validate
```
python run.py
```
Expected: `PASS`. Prove the fix from the repository root as well:
```
python -m pytest -q "tests/test_lab_sequences.py::test_lab_sequence[5.1]"
```

## Expected Results
| Stage | Expected status |
|---|---|
| Starter | PASS |
| After your build or the solution | PASS |
| After lab-changes (break it safely) | FAIL (write-without-approval) |
| After remediation | PASS |

## Evidence
Architecture findings, Mermaid diagram source. Keep the whole `evidence/` folder; the manifest lets a reviewer confirm nothing was edited after the run.

## Common Problems
- Quote YAML values that contain a colon.

## Security Considerations
Never let a diagram show a control that is not configured; link each control to evidence.

## Enterprise Application
Store the architecture file beside the agent's code and review it in pull requests.

## Production Considerations
Run the validator in CI on every architecture change.

## Cleanup
Delete `workspace/lab-5.1`. No cloud resources are created by the local lab.

## Further Challenge
Add a rule that every data component must have a sensitivity label.

---
Validation status: LOCALLY VALIDATED: the full sequence (starter, solution, break it safely, prove the fix) passed on 2026-10-07 with Python 3.13.16, pytest 8.4.2, PyYAML 6.0.3, using synthetic data only. GitHub Actions workflow: STATICALLY VALIDATED (actionlint 1.7.12); EXECUTION VALIDATION REQUIRED on a hosted runner.

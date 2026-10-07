# Lab 15.1 Decision Authority and the AI Use-Case Register (Public Sector)

**Book:** Chapter 15, section "15.2 Designing for Merits Review"
**Difficulty:** Level 6 (Govern)
**Platform:** Local
**Effort:** 45 minutes
**Cloud tenant needed:** No
**API key needed:** No
**Data:** synthetic only (Harbourline Group is fictional; domain harbourline.example)

## What You Will Build
A workflow-policy check over synthetic grant events and a register entry check.

## Why This Matters
Accountability to the public requires a person who decided and reasons that can be read.

## Enterprise Scenario
A fictional agency wants its intake agent to 'clear the obvious ineligibles'.

## Learning Objectives
- Find agent roles with decision authority
- Require reasons and policy version on decisions
- Complete the register entry

## Prerequisites
- Python 3.11 or later and `pip install -r requirements.txt` from the repository root
- Lab 0.1 completed (you know how to read an evidence pack)
- The book section above read first: the lab tests the decision, not the reading

## Architecture
The lab follows the repository pattern: your inputs in `starter/`, a shared engine in `shared/playbook/`, and evidence written to `evidence/`.

```
inputs (YAML, CSV, JSON)  -->  run.py  -->  shared/playbook engine  -->  evidence/result.json, report.md, manifest.json
```

Core concept: Decision authority and the AI use-case register (public sector).

## Repository Structure
```
chapter-15/lab-01-public-sector-decision-authority/
  README.md
  lab.json
  starter/
    events.json
    run.py
    use-case-register.yaml
    workflow-policy.yaml
  solution/
    workflow-policy.yaml
  lab-changes/
    workflow-policy.yaml
```

## Steps

### Step 1. Environment Setup
From the repository root:
```
python shared/scripts/start-lab.py 15.1
cd workspace/lab-15.1
```
This copies `starter/` into a workspace folder that git ignores, so you can break things freely.

### Step 2. Configure
Inspect workflow-policy.yaml, events.json, use-case-register.yaml. The starter is a compliant baseline: your first run should PASS.
```
python run.py
```

### Step 3. Build
Add your agency's decision transitions. To compare with the reference, apply the solution:
```
python ../../shared/scripts/start-lab.py 15.1 --apply solution
```

### Step 4. Test
```
python run.py
```
Expected: `PASS`. Open `evidence/report.md` and `evidence/result.json`.

### Step 5. Secure
Check current Australian Government AI policy requirements; they change. Confirm `evidence/manifest.json` lists a SHA-256 hash for every evidence file.

### Step 6. Break It Safely
lab-changes/ grants the agent the reject transition. Apply it:
```
python ../../shared/scripts/start-lab.py 15.1 --apply lab-changes
```
Anything marked INTENTIONALLY INSECURE is for lab use only.

### Step 7. Observe
```
python run.py
```
Expected: `FAIL` with a blocking finding `agent-holds-decision-authority`. Read the message: it names what changed and why it matters.

### Step 8. Remediate
Remove it; the agent may recommend, an officer decides.
```
python ../../shared/scripts/start-lab.py 15.1 --apply solution
```

### Step 9. Validate
```
python run.py
```
Expected: `PASS`. Prove the fix from the repository root as well:
```
python -m pytest -q "tests/test_lab_sequences.py::test_lab_sequence[15.1]"
```

## Expected Results
| Stage | Expected status |
|---|---|
| Starter | PASS |
| After your build or the solution | PASS |
| After lab-changes (break it safely) | FAIL (agent-holds-decision-authority) |
| After remediation | PASS |

## Evidence
Authority replay and register check. Keep the whole `evidence/` folder; the manifest lets a reviewer confirm nothing was edited after the run.

## Common Problems
- Register fields follow the book's template; align them to your jurisdiction's current policy.

## Security Considerations
Check current Australian Government AI policy requirements; they change.

## Enterprise Application
Publish the transparency statement.

## Production Considerations
Audit transitions monthly.

## Cleanup
Delete `workspace/lab-15.1`. No cloud resources are created by the local lab.

## Further Challenge
Add a check that rejections include review rights text.

---
Validation status: LOCALLY VALIDATED: the full sequence (starter, solution, break it safely, prove the fix) passed on 2026-10-07 with Python 3.13.16, pytest 8.4.2, PyYAML 6.0.3, using synthetic data only. GitHub Actions workflow: STATICALLY VALIDATED (actionlint 1.7.12); EXECUTION VALIDATION REQUIRED on a hosted runner.

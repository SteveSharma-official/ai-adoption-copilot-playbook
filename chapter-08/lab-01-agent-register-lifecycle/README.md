# Lab 8.1 Agent Register and Lifecycle Controls

**Book:** Chapter 8, section "8.1 The Inventory Problem"
**Difficulty:** Level 6 (Govern)
**Platform:** Local (synthetic); Agent 365 inventory for real data
**Effort:** 60 minutes
**Cloud tenant needed:** Optional
**API key needed:** No
**Data:** synthetic only (Harbourline Group is fictional; domain harbourline.example)

## What You Will Build
A reconciliation of agent inventory against the register and HR leaver data, producing reassign, quarantine and decommission actions.

## Why This Matters
Ownership decays silently. A lifecycle rule turns a leaver into a scheduled action instead of an incident.

## Enterprise Scenario
Harbourline's Ops Roster Helper writes to the roster system. Its owner left forty days ago.

## Learning Objectives
- Find unregistered agents
- Apply quarantine and decommission thresholds
- Prove the register stays correct when an owner leaves

## Prerequisites
- Python 3.11 or later and `pip install -r requirements.txt` from the repository root
- Lab 0.1 completed (you know how to read an evidence pack)
- The book section above read first: the lab tests the decision, not the reading

## Architecture
The lab follows the repository pattern: your inputs in `starter/`, a shared engine in `shared/playbook/`, and evidence written to `evidence/`.

```
inputs (YAML, CSV, JSON)  -->  run.py  -->  shared/playbook engine  -->  evidence/result.json, report.md, manifest.json
```

Core concept: Agent register, sponsors and lifecycle (quarantine, decommission).

## Repository Structure
```
chapter-08/lab-01-agent-register-lifecycle/
  README.md
  lab.json
  starter/
    NOTE.md
    run.py
  solution/
    agent_register.csv
    agents.json
  lab-changes/
    users.csv
  solution-after-break/
    agents.json
```

## Steps

### Step 1. Environment Setup
From the repository root:
```
python shared/scripts/start-lab.py 8.1
cd workspace/lab-8.1
```
This copies `starter/` into a workspace folder that git ignores, so you can break things freely.

### Step 2. Configure
Inspect shared agents.json, agent_register.csv, users.csv. The starter is deliberately non-compliant: your first run should FAIL. That failure is the finding you will remediate.
```
python run.py
```

### Step 3. Build
Write corrected agents.json and agent_register.csv. To compare with the reference, apply the solution:
```
python ../../shared/scripts/start-lab.py 8.1 --apply solution
```

### Step 4. Test
```
python run.py
```
Expected: `PASS`. Open `evidence/report.md` and `evidence/result.json`.

### Step 5. Secure
HR leaver data is personal information; use synthetic data in labs. Confirm `evidence/manifest.json` lists a SHA-256 hash for every evidence file.

### Step 6. Break It Safely
lab-changes/ makes the new owner a leaver. Apply it:
```
python ../../shared/scripts/start-lab.py 8.1 --apply lab-changes
```
Anything marked INTENTIONALLY INSECURE is for lab use only.

### Step 7. Observe
```
python run.py
```
Expected: `FAIL` with a blocking finding `owner-left`. Read the message: it names what changed and why it matters.

### Step 8. Remediate
Reassign owner and sponsor (solution-after-break).
```
python ../../shared/scripts/start-lab.py 8.1 --apply solution-after-break
```

### Step 9. Validate
```
python run.py
```
Expected: `PASS`. Prove the fix from the repository root as well:
```
python -m pytest -q "tests/test_lab_sequences.py::test_lab_sequence[8.1]"
```

## Expected Results
| Stage | Expected status |
|---|---|
| Starter | FAIL |
| After your build or the solution | PASS |
| After lab-changes (break it safely) | FAIL (owner-left) |
| After remediation | PASS |

## Evidence
Register actions report. Keep the whole `evidence/` folder; the manifest lets a reviewer confirm nothing was edited after the run.

## Common Problems
- Thresholds: 14 days to quarantine, 30 to decommission.

## Security Considerations
HR leaver data is personal information; use synthetic data in labs.

## Enterprise Application
Wire the HR leaver feed to the register.

## Production Considerations
Agent 365 provides inventory; the register adds accountability.

## Cleanup
Delete `workspace/lab-8.1`. No cloud resources are created by the local lab.

## Further Challenge
Add a review-overdue rule that blocks production after 13 months.

---
Validation status: LOCALLY VALIDATED: the full sequence (starter, solution, break it safely, prove the fix) passed on 2026-10-07 with Python 3.13.16, pytest 8.4.2, PyYAML 6.0.3, using synthetic data only. GitHub Actions workflow: STATICALLY VALIDATED (actionlint 1.7.12); EXECUTION VALIDATION REQUIRED on a hosted runner.

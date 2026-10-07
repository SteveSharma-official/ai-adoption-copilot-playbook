# Lab 6.3 Agent Credential and Identity Audit

**Book:** Chapter 6, section "6.5 Agent Identity Is Not User Identity"
**Difficulty:** Level 4 (Secure)
**Platform:** Local (synthetic inventory); tenant inventory for real data
**Effort:** 45 minutes
**Cloud tenant needed:** Optional
**API key needed:** No
**Data:** synthetic only (Harbourline Group is fictional; domain harbourline.example)

## What You Will Build
An audit of the agent inventory for maker credentials, shared service accounts and missing sponsors, then a corrected inventory.

## Why This Matters
An agent with borrowed credentials has the blast radius of its maker. Identity is where agent risk is cheapest to fix.

## Enterprise Scenario
Harbourline's Expense Policy Checker was built by a finance analyst who has since resigned. It still runs on her credentials.

## Learning Objectives
- Identify maker-credential agents
- Assign sponsors
- Re-run the audit and prove it passes

## Prerequisites
- Python 3.11 or later and `pip install -r requirements.txt` from the repository root
- Lab 0.1 completed (you know how to read an evidence pack)
- The book section above read first: the lab tests the decision, not the reading

## Architecture
The lab follows the repository pattern: your inputs in `starter/`, a shared engine in `shared/playbook/`, and evidence written to `evidence/`.

```
inputs (YAML, CSV, JSON)  -->  run.py  -->  shared/playbook engine  -->  evidence/result.json, report.md, manifest.json
```

Core concept: Agent identity and credential patterns.

## Repository Structure
```
chapter-06/lab-03-agent-credential-audit/
  README.md
  lab.json
  starter/
    NOTE.md
    run.py
  solution/
    agents.json
  lab-changes/
    agents.json
```

## Steps

### Step 1. Environment Setup
From the repository root:
```
python shared/scripts/start-lab.py 6.3
cd workspace/lab-6.3
```
This copies `starter/` into a workspace folder that git ignores, so you can break things freely.

### Step 2. Configure
Inspect shared agents.json. The starter is deliberately non-compliant: your first run should FAIL. That failure is the finding you will remediate.
```
python run.py
```

### Step 3. Build
Write a corrected agents.json in the lab folder. To compare with the reference, apply the solution:
```
python ../../shared/scripts/start-lab.py 6.3 --apply solution
```

### Step 4. Test
```
python run.py
```
Expected: `PASS`. Open `evidence/report.md` and `evidence/result.json`.

### Step 5. Secure
Do not export real credential configuration into lab files. Confirm `evidence/manifest.json` lists a SHA-256 hash for every evidence file.

### Step 6. Break It Safely
lab-changes/ adds a new production agent on maker credentials. Apply it:
```
python ../../shared/scripts/start-lab.py 6.3 --apply lab-changes
```
Anything marked INTENTIONALLY INSECURE is for lab use only.

### Step 7. Observe
```
python run.py
```
Expected: `FAIL` with a blocking finding `maker-credentials`. Read the message: it names what changed and why it matters.

### Step 8. Remediate
Re-apply the corrected inventory; block maker credentials by environment policy.
```
python ../../shared/scripts/start-lab.py 6.3 --apply solution
```

### Step 9. Validate
```
python run.py
```
Expected: `PASS`. Prove the fix from the repository root as well:
```
python -m pytest -q "tests/test_lab_sequences.py::test_lab_sequence[6.3]"
```

## Expected Results
| Stage | Expected status |
|---|---|
| Starter | FAIL |
| After your build or the solution | PASS |
| After lab-changes (break it safely) | FAIL (maker-credentials) |
| After remediation | PASS |

## Evidence
Credential audit report. Keep the whole `evidence/` folder; the manifest lets a reviewer confirm nothing was edited after the run.

## Common Problems
- The lab reads its local agents.json first, then the shared one.

## Security Considerations
Do not export real credential configuration into lab files.

## Enterprise Application
Make the audit a gate for every environment promotion.

## Production Considerations
Combine with Entra Agent ID and Conditional Access for agents.

## Cleanup
Delete `workspace/lab-6.3`. No cloud resources are created by the local lab.

## Further Challenge
Flag write tools that run under end-user identity without an approval stage.

---
Validation status: LOCALLY VALIDATED: the full sequence (starter, solution, break it safely, prove the fix) passed on 2026-10-07 with Python 3.13.16, pytest 8.4.2, PyYAML 6.0.3, using synthetic data only. GitHub Actions workflow: STATICALLY VALIDATED (actionlint 1.7.12); EXECUTION VALIDATION REQUIRED on a hosted runner.

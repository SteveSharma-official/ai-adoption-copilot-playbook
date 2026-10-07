# Lab 7.2 Approval Gate in a Copilot Studio Agent Flow (Tenant)

**Book:** Chapter 7, section "7.3 Securing the Tool Connections"
**Difficulty:** Level 4 (Secure)
**Platform:** Copilot Studio (tenant) plus local checker
**Effort:** 2 hours (tenant)
**Cloud tenant needed:** Yes
**API key needed:** No
**Data:** synthetic only (Harbourline Group is fictional; domain harbourline.example)

> **Tenant required for the build steps.** Use a non-production Microsoft 365 or Power Platform environment you are authorised to change. Licensing and preview features vary; confirm against current Microsoft documentation. The synthetic sample in starter/ lets you complete the local checker without a tenant.

## What You Will Build
An agent flow with a human approval stage before a write (in your own tenant), and a checker over its exported run history.

## Why This Matters
The approval record is the evidence. If it cannot show who approved what, before it happened, the control did not exist.

## Enterprise Scenario
Harbourline lets the AP agent raise small purchase orders, but only after the AP manager approves each one.

## Learning Objectives
- Configure an approval stage before a write action
- Export run history
- Detect unapproved, late or self-approved writes

## Prerequisites
- Python 3.11 or later and `pip install -r requirements.txt` from the repository root
- Lab 0.1 completed (you know how to read an evidence pack)
- The book section above read first: the lab tests the decision, not the reading

## Architecture
The lab follows the repository pattern: your inputs in `starter/`, a shared engine in `shared/playbook/`, and evidence written to `evidence/`.

```
inputs (YAML, CSV, JSON)  -->  run.py  -->  shared/playbook engine  -->  evidence/result.json, report.md, manifest.json
```

Core concept: Human approval gates in agent flows.

## Repository Structure
```
chapter-07/lab-02-copilot-studio-approval-flow/
  README.md
  lab.json
  starter/
    run-history.csv
    run.py
  solution/
    run-history.csv
  lab-changes/
    run-history.csv
```

## Steps

### Step 1. Environment Setup
From the repository root:
```
python shared/scripts/start-lab.py 7.2
cd workspace/lab-7.2
```
This copies `starter/` into a workspace folder that git ignores, so you can break things freely.

### Step 2. Configure
Inspect run-history.csv (synthetic sample). The starter is a compliant baseline: your first run should PASS.
```
python run.py
```

### Step 3. Build
In a non-production tenant, add the approval stage and export your own run history. To compare with the reference, apply the solution:
```
python ../../shared/scripts/start-lab.py 7.2 --apply solution
```

### Step 4. Test
```
python run.py
```
Expected: `PASS`. Open `evidence/report.md` and `evidence/result.json`.

### Step 5. Secure
Use a developer or sandbox environment. Never test approval bypasses in production. Confirm `evidence/manifest.json` lists a SHA-256 hash for every evidence file.

### Step 6. Break It Safely
lab-changes/ adds a write approved by an AI stage only. Apply it:
```
python ../../shared/scripts/start-lab.py 7.2 --apply lab-changes
```
Anything marked INTENTIONALLY INSECURE is for lab use only.

### Step 7. Observe
```
python run.py
```
Expected: `FAIL` with a blocking finding `unapproved-write`. Read the message: it names what changed and why it matters.

### Step 8. Remediate
Require a human approver; AI stages may recommend, not approve.
```
python ../../shared/scripts/start-lab.py 7.2 --apply solution
```

### Step 9. Validate
```
python run.py
```
Expected: `PASS`. Prove the fix from the repository root as well:
```
python -m pytest -q "tests/test_lab_sequences.py::test_lab_sequence[7.2]"
```

## Expected Results
| Stage | Expected status |
|---|---|
| Starter | PASS |
| After your build or the solution | PASS |
| After lab-changes (break it safely) | FAIL (unapproved-write) |
| After remediation | PASS |

## Evidence
Approval history check over exported run history. Keep the whole `evidence/` folder; the manifest lets a reviewer confirm nothing was edited after the run.

## Common Problems
- Approval features change; check current Copilot Studio documentation before building.
- Multistage approvals were in preview at the time of writing.

## Security Considerations
Use a developer or sandbox environment. Never test approval bypasses in production.

## Enterprise Application
Make approval evidence part of the production readiness gate.

## Production Considerations
Alert on any write without an approval record.

## Cleanup
Delete `workspace/lab-7.2`. No cloud resources are created by the local lab. If you built the tenant steps, delete the test agent, flow and environment you created, and remove any test users or connections.

## Further Challenge
Add an approval timeout that fails closed.

---
Validation status: LOCALLY VALIDATED: the full sequence (starter, solution, break it safely, prove the fix) passed on 2026-10-07 with Python 3.13.16, pytest 8.4.2, PyYAML 6.0.3, using synthetic data only. Tenant steps (building in Microsoft 365 or Power Platform): CLOUD VALIDATION REQUIRED. GitHub Actions workflow: STATICALLY VALIDATED (actionlint 1.7.12); EXECUTION VALIDATION REQUIRED on a hosted runner.

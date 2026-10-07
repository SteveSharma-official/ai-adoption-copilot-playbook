# Lab 6.1 Oversharing Discovery and the Copilot Exposure Report

**Book:** Chapter 6, section "6.3 The Copilot Data Exposure Model"
**Difficulty:** Level 4 (Secure)
**Platform:** Local (synthetic tenant); tenant reports for real data
**Effort:** 90 minutes
**Cloud tenant needed:** Optional (real tenant uses DAG reports)
**API key needed:** No
**Data:** synthetic only (Harbourline Group is fictional; domain harbourline.example)

## What You Will Build
An exposure report for the pilot wave over a synthetic tenant, a remediation overlay, and a re-run that proves the fix.

## Why This Matters
Copilot does not create access. It makes existing access discoverable. This lab shows the difference in numbers.

## Enterprise Scenario
A new Harbourline finance graduate could ask Copilot to summarise the 2019 salary review. Board papers are shared by an organisation-wide link.

## Learning Objectives
- Compute who can open and who could have each site summarised
- Remediate crown-jewel exposure
- Distinguish containment (RCD) from remediation

## Prerequisites
- Python 3.11 or later and `pip install -r requirements.txt` from the repository root
- Lab 0.1 completed (you know how to read an evidence pack)
- The book section above read first: the lab tests the decision, not the reading

## Architecture
The lab follows the repository pattern: your inputs in `starter/`, a shared engine in `shared/playbook/`, and evidence written to `evidence/`.

```
inputs (YAML, CSV, JSON)  -->  run.py  -->  shared/playbook engine  -->  evidence/result.json, report.md, manifest.json
```

Core concept: Copilot Data Exposure Model (access, discovery, protection, processing, lifecycle).

## Repository Structure
```
chapter-06/lab-01-oversharing-exposure-report/
  README.md
  lab.json
  starter/
    README-inputs.md
    run.py
  solution/
    remediation.yaml
  lab-changes/
    new-changes.yaml
  solution-after-break/
    new-changes.yaml
```

## Steps

### Step 1. Environment Setup
From the repository root:
```
python shared/scripts/start-lab.py 6.1
cd workspace/lab-6.1
```
This copies `starter/` into a workspace folder that git ignores, so you can break things freely.

### Step 2. Configure
Inspect shared/datasets/harbourline (sites, grants, links). The starter is deliberately non-compliant: your first run should FAIL. That failure is the finding you will remediate.
```
python run.py
```

### Step 3. Build
Write remediation.yaml: remove broad grants, revoke links, contain what cannot be fixed in time. To compare with the reference, apply the solution:
```
python ../../shared/scripts/start-lab.py 6.1 --apply solution
```

### Step 4. Test
```
python run.py
```
Expected: `PASS`. Open `evidence/report.md` and `evidence/result.json`.

### Step 5. Secure
The synthetic model teaches the layers; it does not reproduce Microsoft's reports. Use data access governance reports in a real tenant. Confirm `evidence/manifest.json` lists a SHA-256 hash for every evidence file.

### Step 6. Break It Safely
lab-changes/ adds a new organisation-wide link to the October board pack. Apply it:
```
python ../../shared/scripts/start-lab.py 6.1 --apply lab-changes
```
Anything marked INTENTIONALLY INSECURE is for lab use only.

### Step 7. Observe
```
python run.py
```
Expected: `FAIL` with a blocking finding `crown-jewel-exposed`. Read the message: it names what changed and why it matters.

### Step 8. Remediate
Revoke the new link (solution-after-break) and add a link-creation policy to the expansion gate.
```
python ../../shared/scripts/start-lab.py 6.1 --apply solution-after-break
```

### Step 9. Validate
```
python run.py
```
Expected: `PASS`. Prove the fix from the repository root as well:
```
python -m pytest -q "tests/test_lab_sequences.py::test_lab_sequence[6.1]"
```

## Expected Results
| Stage | Expected status |
|---|---|
| Starter | FAIL |
| After your build or the solution | PASS |
| After lab-changes (break it safely) | FAIL (crown-jewel-exposed) |
| After remediation | PASS |

## Evidence
Exposure report before and after remediation. Keep the whole `evidence/` folder; the manifest lets a reviewer confirm nothing was edited after the run.

## Common Problems
- RCD appears as a non-blocking note: containment needs an owner and exit date.

## Security Considerations
The synthetic model teaches the layers; it does not reproduce Microsoft's reports. Use data access governance reports in a real tenant.

## Enterprise Application
No licence expansion without a signed exposure report for that wave.

## Production Considerations
Schedule the report per wave and alert on new organisation-wide links to labelled sites.

## Cleanup
Delete `workspace/lab-6.1`. No cloud resources are created by the local lab.

## Further Challenge
Add a sixth crown-jewel category for legal privilege and remediate it.

---
Validation status: LOCALLY VALIDATED: the full sequence (starter, solution, break it safely, prove the fix) passed on 2026-10-07 with Python 3.13.16, pytest 8.4.2, PyYAML 6.0.3, using synthetic data only. GitHub Actions workflow: STATICALLY VALIDATED (actionlint 1.7.12); EXECUTION VALIDATION REQUIRED on a hosted runner.

# Lab 1.2 Tenant Baseline: What Did We Buy?

**Book:** Chapter 1, section "1.2 Why Copilot is Different from Previous Deployments"
**Difficulty:** Level 1 (Explore)
**Platform:** Microsoft 365 tenant exports plus local summariser
**Effort:** 45 minutes (plus tenant export time)
**Cloud tenant needed:** Yes, for real exports (sample exports included)
**API key needed:** No
**Data:** synthetic only (Harbourline Group is fictional; domain harbourline.example)

> **Tenant required for the build steps.** Use a non-production Microsoft 365 or Power Platform environment you are authorised to change. Licensing and preview features vary; confirm against current Microsoft documentation. The synthetic sample in starter/ lets you complete the local checker without a tenant.

## What You Will Build
A summariser that turns licence, usage and agent exports into a dated baseline, and refuses to run without provenance.

## Why This Matters
Every value claim later in the book is measured against a baseline. Without provenance the baseline is an opinion.

## Enterprise Scenario
Harbourline bought Copilot seats for a pilot. Finance wants to know whether the seats are used before approving more.

## Learning Objectives
- Identify the admin exports a baseline needs
- Record provenance for each export
- Summarise utilisation without over-claiming

## Prerequisites
- Python 3.11 or later and `pip install -r requirements.txt` from the repository root
- Lab 0.1 completed (you know how to read an evidence pack)
- The book section above read first: the lab tests the decision, not the reading

## Architecture
The lab follows the repository pattern: your inputs in `starter/`, a shared engine in `shared/playbook/`, and evidence written to `evidence/`.

```
inputs (YAML, CSV, JSON)  -->  run.py  -->  shared/playbook engine  -->  evidence/result.json, report.md, manifest.json
```

Core concept: Tenant baseline (licences, usage, agents).

## Repository Structure
```
chapter-01/lab-02-tenant-baseline/
  README.md
  lab.json
  starter/
    exports/SOURCE.md
    exports/agents.csv
    exports/copilot_usage.csv
    exports/licences.csv
    run.py
  solution/
    exports/SOURCE.md
  lab-changes/
    REMOVE.txt
```

## Steps

### Step 1. Environment Setup
From the repository root:
```
python shared/scripts/start-lab.py 1.2
cd workspace/lab-1.2
```
This copies `starter/` into a workspace folder that git ignores, so you can break things freely.

### Step 2. Configure
Inspect exports/ (synthetic samples) and SOURCE.md. The starter is a compliant baseline: your first run should PASS.
```
python run.py
```

### Step 3. Build
Replace the sample exports with your own (in a private copy) and update SOURCE.md. To compare with the reference, apply the solution:
```
python ../../shared/scripts/start-lab.py 1.2 --apply solution
```

### Step 4. Test
```
python run.py
```
Expected: `PASS`. Open `evidence/report.md` and `evidence/result.json`.

### Step 5. Secure
Tenant exports contain personal data. Keep them out of any public fork. Confirm `evidence/manifest.json` lists a SHA-256 hash for every evidence file.

### Step 6. Break It Safely
lab-changes/REMOVE.txt deletes SOURCE.md. Apply it:
```
python ../../shared/scripts/start-lab.py 1.2 --apply lab-changes
```
Anything marked INTENTIONALLY INSECURE is for lab use only.

### Step 7. Observe
```
python run.py
```
Expected: `FAIL` with a blocking finding `export-provenance`. Read the message: it names what changed and why it matters.

### Step 8. Remediate
Restore SOURCE.md with who, when and from where.
```
python ../../shared/scripts/start-lab.py 1.2 --apply solution
```

### Step 9. Validate
```
python run.py
```
Expected: `PASS`. Prove the fix from the repository root as well:
```
python -m pytest -q "tests/test_lab_sequences.py::test_lab_sequence[1.2]"
```

## Expected Results
| Stage | Expected status |
|---|---|
| Starter | PASS |
| After your build or the solution | PASS |
| After lab-changes (break it safely) | FAIL (export-provenance) |
| After remediation | PASS |

## Evidence
Baseline report, SOURCE.md provenance. Keep the whole `evidence/` folder; the manifest lets a reviewer confirm nothing was edited after the run.

## Common Problems
- Export column names differ by admin centre version; map them in the CSV header.
- Usage reports may be pseudonymised by tenant setting.

## Security Considerations
Tenant exports contain personal data. Keep them out of any public fork.

## Enterprise Application
Use the baseline as the denominator for every adoption metric in Chapter 18.

## Production Considerations
Automate the export monthly through a governed process with retention.

## Cleanup
Delete `workspace/lab-1.2`. No cloud resources are created by the local lab. If you built the tenant steps, delete the test agent, flow and environment you created, and remove any test users or connections.

## Further Challenge
Add a check that flags licences assigned to leavers.

---
Validation status: LOCALLY VALIDATED: the full sequence (starter, solution, break it safely, prove the fix) passed on 2026-10-07 with Python 3.13.16, pytest 8.4.2, PyYAML 6.0.3, using synthetic data only. Tenant steps (building in Microsoft 365 or Power Platform): CLOUD VALIDATION REQUIRED. GitHub Actions workflow: STATICALLY VALIDATED (actionlint 1.7.12); EXECUTION VALIDATION REQUIRED on a hosted runner.

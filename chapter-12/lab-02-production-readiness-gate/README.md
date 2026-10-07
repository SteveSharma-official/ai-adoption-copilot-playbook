# Lab 12.2 Copilot Production Readiness Gate, Evidence First

**Book:** Chapter 12, section "12.3 The Copilot Production Readiness Gate"
**Difficulty:** Level 7 (Deploy)
**Platform:** Local
**Effort:** 45 minutes
**Cloud tenant needed:** No
**API key needed:** No
**Data:** synthetic only (Harbourline Group is fictional; domain harbourline.example)

## What You Will Build
A worked subset of the sixty-item gate with an evidence pack, scored into Proceed, Conditional or Do not deploy.

## Why This Matters
If the evidence is missing, the deployment is blocked. The gate makes that rule mechanical.

## Enterprise Scenario
Harbourline's AP agent is ready for production review. The stop-procedure test record cannot be found.

## Learning Objectives
- Score six domains
- Enforce four hard gates
- Treat unevidenced scores as zero

## Prerequisites
- Python 3.11 or later and `pip install -r requirements.txt` from the repository root
- Lab 0.1 completed (you know how to read an evidence pack)
- The book section above read first: the lab tests the decision, not the reading

## Architecture
The lab follows the repository pattern: your inputs in `starter/`, a shared engine in `shared/playbook/`, and evidence written to `evidence/`.

```
inputs (YAML, CSV, JSON)  -->  run.py  -->  shared/playbook engine  -->  evidence/result.json, report.md, manifest.json
```

Core concept: Copilot Production Readiness Gate (six domains, four hard gates).

## Repository Structure
```
chapter-12/lab-02-production-readiness-gate/
  README.md
  lab.json
  starter/
    checklist.yaml
    evidence-pack/agent-identity-export.json
    evidence-pack/authority-replay.md
    evidence-pack/baseline.md
    evidence-pack/conditional-access.md
    evidence-pack/cost-note.md
    evidence-pack/evaluation-scorecard.md
    evidence-pack/exposure-signoff.md
    evidence-pack/knowledge-sources.md
    evidence-pack/owner-and-sponsor.md
    evidence-pack/register-entry.md
    evidence-pack/runbook-note.md
    evidence-pack/stop-procedure-test.md
    evidence-pack/support-route.md
    evidence-pack/threat-model.md
    run.py
  solution/
    evidence-pack/stop-procedure-test.md
  lab-changes/
    REMOVE.txt
```

## Steps

### Step 1. Environment Setup
From the repository root:
```
python shared/scripts/start-lab.py 12.2
cd workspace/lab-12.2
```
This copies `starter/` into a workspace folder that git ignores, so you can break things freely.

### Step 2. Configure
Inspect checklist.yaml and evidence-pack/. The starter is a compliant baseline: your first run should PASS.
```
python run.py
```

### Step 3. Build
Point each item at evidence from your earlier labs. To compare with the reference, apply the solution:
```
python ../../shared/scripts/start-lab.py 12.2 --apply solution
```

### Step 4. Test
```
python run.py
```
Expected: `PASS`. Open `evidence/report.md` and `evidence/result.json`.

### Step 5. Secure
Reviewers sign; the tool only checks presence, not quality. Confirm `evidence/manifest.json` lists a SHA-256 hash for every evidence file.

### Step 6. Break It Safely
lab-changes/REMOVE.txt deletes the stop-procedure test record. Apply it:
```
python ../../shared/scripts/start-lab.py 12.2 --apply lab-changes
```
Anything marked INTENTIONALLY INSECURE is for lab use only.

### Step 7. Observe
```
python run.py
```
Expected: `FAIL` with a blocking finding `hard-gate`. Read the message: it names what changed and why it matters.

### Step 8. Remediate
Run and record the stop-procedure test.
```
python ../../shared/scripts/start-lab.py 12.2 --apply solution
```

### Step 9. Validate
```
python run.py
```
Expected: `PASS`. Prove the fix from the repository root as well:
```
python -m pytest -q "tests/test_lab_sequences.py::test_lab_sequence[12.2]"
```

## Expected Results
| Stage | Expected status |
|---|---|
| Starter | PASS |
| After your build or the solution | PASS |
| After lab-changes (break it safely) | FAIL (hard-gate) |
| After remediation | PASS |

## Evidence
Readiness score and band. Keep the whole `evidence/` folder; the manifest lets a reviewer confirm nothing was edited after the run.

## Common Problems
- Evidence paths are relative to the lab folder.

## Security Considerations
Reviewers sign; the tool only checks presence, not quality.

## Enterprise Application
CISO and enterprise architect review together.

## Production Considerations
Re-review within 30 days for Conditional results.

## Cleanup
Delete `workspace/lab-12.2`. No cloud resources are created by the local lab.

## Further Challenge
Implement all sixty items from Appendix I.

---
Validation status: LOCALLY VALIDATED: the full sequence (starter, solution, break it safely, prove the fix) passed on 2026-10-07 with Python 3.13.16, pytest 8.4.2, PyYAML 6.0.3, using synthetic data only. GitHub Actions workflow: STATICALLY VALIDATED (actionlint 1.7.12); EXECUTION VALIDATION REQUIRED on a hosted runner.

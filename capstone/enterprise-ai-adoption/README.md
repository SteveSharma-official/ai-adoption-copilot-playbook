# Lab Capstone Capstone: Enterprise AI Adoption Journey, from Hypothesis to Production Decision

**Book:** Capstone, section "Closing Brief: Your next 90 days"
**Difficulty:** Level 8 (Scale)
**Platform:** Local
**Effort:** 3 to 4 hours
**Cloud tenant needed:** No
**API key needed:** No
**Data:** synthetic only (Harbourline Group is fictional; domain harbourline.example)

## What You Will Build
A six-stage pipeline for the Harbourline AP supplier query agent that only recommends production when every stage passes with evidence.

## Why This Matters
The book's argument is that adoption is a chain of evidenced decisions. The capstone proves the chain holds.

## Enterprise Scenario
Harbourline's executive committee will decide in one meeting whether the AP agent goes to production.

## Learning Objectives
- Run six stages end to end
- Feed stage evidence into the readiness gate
- Produce a signed decision pack

## Prerequisites
- Python 3.11 or later and `pip install -r requirements.txt` from the repository root
- Lab 0.1 completed (you know how to read an evidence pack)
- The book section above read first: the lab tests the decision, not the reading

## Architecture
The lab follows the repository pattern: your inputs in `starter/`, a shared engine in `shared/playbook/`, and evidence written to `evidence/`.

```
inputs (YAML, CSV, JSON)  -->  run.py  -->  shared/playbook engine  -->  evidence/result.json, report.md, manifest.json
```

Core concept: Enterprise AI adoption journey, end to end.

## Repository Structure
```
capstone/enterprise-ai-adoption/
  README.md
  lab.json
  starter/
    inputs/agents.json
    inputs/authority-matrix.yaml
    inputs/candidate.jsonl
    inputs/hypothesis.yaml
    inputs/readiness.yaml
    inputs/replay.jsonl
    inputs/stop-procedure-test.md
    inputs/testset.yaml
    inputs/thresholds.yaml
    run.py
  solution/
    inputs/remediation.yaml
  lab-changes/
    inputs/candidate.jsonl
  solution-after-break/
    inputs/candidate.jsonl
```

## Steps

### Step 1. Environment Setup
From the repository root:
```
python shared/scripts/start-lab.py Capstone
cd workspace/lab-Capstone
```
This copies `starter/` into a workspace folder that git ignores, so you can break things freely.

### Step 2. Configure
Inspect inputs/. The starter is deliberately non-compliant: your first run should FAIL. That failure is the finding you will remediate.
```
python run.py
```

### Step 3. Build
Add inputs/remediation.yaml so the exposure stage passes. To compare with the reference, apply the solution:
```
python ../../shared/scripts/start-lab.py Capstone --apply solution
```

### Step 4. Test
```
python run.py
```
Expected: `PASS`. Open `evidence/report.md` and `evidence/result.json`.

### Step 5. Secure
Synthetic data only. Confirm `evidence/manifest.json` lists a SHA-256 hash for every evidence file.

### Step 6. Break It Safely
lab-changes/ swaps in agent version 2.0. Apply it:
```
python ../../shared/scripts/start-lab.py Capstone --apply lab-changes
```
Anything marked INTENTIONALLY INSECURE is for lab use only.

### Step 7. Observe
```
python run.py
```
Expected: `FAIL` with a blocking finding `stage-failed (5-evaluation)`. Read the message: it names what changed and why it matters.

### Step 8. Remediate
Restore version 1.4 (solution-after-break) and re-run.
```
python ../../shared/scripts/start-lab.py Capstone --apply solution-after-break
```

### Step 9. Validate
```
python run.py
```
Expected: `PASS`. Prove the fix from the repository root as well:
```
python -m pytest -q "tests/test_lab_sequences.py::test_lab_sequence[Capstone]"
```

## Expected Results
| Stage | Expected status |
|---|---|
| Starter | FAIL |
| After your build or the solution | PASS |
| After lab-changes (break it safely) | FAIL (stage-failed (5-evaluation)) |
| After remediation | PASS |

## Evidence
Decision pack plus per-stage evidence with PASSED markers. Keep the whole `evidence/` folder; the manifest lets a reviewer confirm nothing was edited after the run.

## Common Problems
- Stages write PASSED markers only on success; stale markers are removed.

## Security Considerations
Synthetic data only.

## Enterprise Application
Replace inputs with your own evidence to produce a real decision pack.

## Production Considerations
Run the chain in CI for every agent version.

## Cleanup
Delete `workspace/lab-Capstone`. No cloud resources are created by the local lab.

## Further Challenge
Add Lab 8.1 lifecycle and Lab 8.2 threat model as stages 7 and 8.

---
Validation status: LOCALLY VALIDATED: the full sequence (starter, solution, break it safely, prove the fix) passed on 2026-10-07 with Python 3.13.16, pytest 8.4.2, PyYAML 6.0.3, using synthetic data only. GitHub Actions workflow: STATICALLY VALIDATED (actionlint 1.7.12); EXECUTION VALIDATION REQUIRED on a hosted runner.

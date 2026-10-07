# Lab 1.1 Copilot Enterprise Adoption Model Self-Assessment

**Book:** Chapter 1, section "1.4 The Copilot Enterprise Adoption Model"
**Difficulty:** Level 1 (Explore)
**Platform:** Local
**Effort:** 30 minutes
**Cloud tenant needed:** No
**API key needed:** No
**Data:** synthetic only (Harbourline Group is fictional; domain harbourline.example)

## What You Will Build
A self-assessment that refuses any maturity level whose gate evidence is missing, and a one-page platform-fit decision.

## Why This Matters
The adoption model is only useful if a level means something. Tying each level to evidence stops optimism being reported as progress.

## Enterprise Scenario
Harbourline's executive committee asks whether the organisation is 'at Level 3'. The programme has licences, a pilot and good intentions.

## Learning Objectives
- Map evidence to each adoption level
- Detect an unsupported claim
- Frame the decision being asked of the executive

## Prerequisites
- Python 3.11 or later and `pip install -r requirements.txt` from the repository root
- Lab 0.1 completed (you know how to read an evidence pack)
- The book section above read first: the lab tests the decision, not the reading

## Architecture
The lab follows the repository pattern: your inputs in `starter/`, a shared engine in `shared/playbook/`, and evidence written to `evidence/`.

```
inputs (YAML, CSV, JSON)  -->  run.py  -->  shared/playbook engine  -->  evidence/result.json, report.md, manifest.json
```

Core concept: Copilot Enterprise Adoption Model (L1 to L5 gates).

## Repository Structure
```
chapter-01/lab-01-adoption-model-assessment/
  README.md
  lab.json
  starter/
    assessment.yaml
    evidence-map/baseline-signoff.md
    evidence-map/business-owner.md
    evidence-map/value-hypothesis.md
    run.py
  solution/
    assessment.yaml
  lab-changes/
    assessment.yaml
```

## Steps

### Step 1. Environment Setup
From the repository root:
```
python shared/scripts/start-lab.py 1.1
cd workspace/lab-1.1
```
This copies `starter/` into a workspace folder that git ignores, so you can break things freely.

### Step 2. Configure
Inspect assessment.yaml and evidence-map/. The starter is a compliant baseline: your first run should PASS.
```
python run.py
```

### Step 3. Build
Complete the evidence map for each gate you claim. To compare with the reference, apply the solution:
```
python ../../shared/scripts/start-lab.py 1.1 --apply solution
```

### Step 4. Test
```
python run.py
```
Expected: `PASS`. Open `evidence/report.md` and `evidence/result.json`.

### Step 5. Secure
Do not attach real board papers as evidence in a lab copy. Confirm `evidence/manifest.json` lists a SHA-256 hash for every evidence file.

### Step 6. Break It Safely
lab-changes/ raises the claimed level to 3 without the exposure and agent evidence. Apply it:
```
python ../../shared/scripts/start-lab.py 1.1 --apply lab-changes
```
Anything marked INTENTIONALLY INSECURE is for lab use only.

### Step 7. Observe
```
python run.py
```
Expected: `FAIL` with a blocking finding `claimed-level-unsupported`. Read the message: it names what changed and why it matters.

### Step 8. Remediate
Return the claim to the level the evidence supports, or produce the missing evidence.
```
python ../../shared/scripts/start-lab.py 1.1 --apply solution
```

### Step 9. Validate
```
python run.py
```
Expected: `PASS`. Prove the fix from the repository root as well:
```
python -m pytest -q "tests/test_lab_sequences.py::test_lab_sequence[1.1]"
```

## Expected Results
| Stage | Expected status |
|---|---|
| Starter | PASS |
| After your build or the solution | PASS |
| After lab-changes (break it safely) | FAIL (claimed-level-unsupported) |
| After remediation | PASS |

## Evidence
Assessment result, platform-fit one-pager. Keep the whole `evidence/` folder; the manifest lets a reviewer confirm nothing was edited after the run.

## Common Problems
- Evidence file paths are relative to the lab folder.
- An empty string counts as missing evidence.

## Security Considerations
Do not attach real board papers as evidence in a lab copy.

## Enterprise Application
Use the one-pager at the steering committee in place of a maturity slide.

## Production Considerations
Re-run quarterly; levels can fall when owners leave or controls lapse.

## Cleanup
Delete `workspace/lab-1.1`. No cloud resources are created by the local lab.

## Further Challenge
Add a Level 4 gate that requires Lab 12.2 readiness evidence at 80 per cent or above.

---
Validation status: LOCALLY VALIDATED: the full sequence (starter, solution, break it safely, prove the fix) passed on 2026-10-07 with Python 3.13.16, pytest 8.4.2, PyYAML 6.0.3, using synthetic data only. GitHub Actions workflow: STATICALLY VALIDATED (actionlint 1.7.12); EXECUTION VALIDATION REQUIRED on a hosted runner.

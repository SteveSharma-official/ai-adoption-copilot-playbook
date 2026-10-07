# Lab 9.1 Process Archaeology and the Use-Case Discovery Canvas

**Book:** Chapter 9, section "9.3 The AI Use-Case Discovery Canvas"
**Difficulty:** Level 2 (Build)
**Platform:** Local
**Effort:** 45 minutes
**Cloud tenant needed:** No
**API key needed:** No
**Data:** synthetic only (Harbourline Group is fictional; domain harbourline.example)

## What You Will Build
A canvas scorer over ten criteria, with friction counts from shadowing observations.

## Why This Matters
The process everyone knows is broken is rarely broken where they think. Observation corrects the story.

## Enterprise Scenario
Harbourline shadowed forty AP supplier queries. The board-pack summariser has a sponsor but no evidence.

## Learning Objectives
- Summarise observed friction
- Score with evidence
- Reject or reframe low scores

## Prerequisites
- Python 3.11 or later and `pip install -r requirements.txt` from the repository root
- Lab 0.1 completed (you know how to read an evidence pack)
- The book section above read first: the lab tests the decision, not the reading

## Architecture
The lab follows the repository pattern: your inputs in `starter/`, a shared engine in `shared/playbook/`, and evidence written to `evidence/`.

```
inputs (YAML, CSV, JSON)  -->  run.py  -->  shared/playbook engine  -->  evidence/result.json, report.md, manifest.json
```

Core concept: Process archaeology and the Use-Case Discovery Canvas.

## Repository Structure
```
chapter-09/lab-01-discovery-canvas/
  README.md
  lab.json
  starter/
    canvases.yaml
    observations.csv
    run.py
  solution/
    canvases.yaml
  lab-changes/
    canvases.yaml
```

## Steps

### Step 1. Environment Setup
From the repository root:
```
python shared/scripts/start-lab.py 9.1
cd workspace/lab-9.1
```
This copies `starter/` into a workspace folder that git ignores, so you can break things freely.

### Step 2. Configure
Inspect canvases.yaml and observations.csv. The starter is a compliant baseline: your first run should PASS.
```
python run.py
```

### Step 3. Build
Score one of your own use cases. To compare with the reference, apply the solution:
```
python ../../shared/scripts/start-lab.py 9.1 --apply solution
```

### Step 4. Test
```
python run.py
```
Expected: `PASS`. Open `evidence/report.md` and `evidence/result.json`.

### Step 5. Secure
Observation notes can contain personal data; anonymise. Confirm `evidence/manifest.json` lists a SHA-256 hash for every evidence file.

### Step 6. Break It Safely
lab-changes/ scores risk as 2 with no evidence ('it will be fine'). Apply it:
```
python ../../shared/scripts/start-lab.py 9.1 --apply lab-changes
```
Anything marked INTENTIONALLY INSECURE is for lab use only.

### Step 7. Observe
```
python run.py
```
Expected: `FAIL` with a blocking finding `score-without-evidence`. Read the message: it names what changed and why it matters.

### Step 8. Remediate
Score 1 until evidence exists.
```
python ../../shared/scripts/start-lab.py 9.1 --apply solution
```

### Step 9. Validate
```
python run.py
```
Expected: `PASS`. Prove the fix from the repository root as well:
```
python -m pytest -q "tests/test_lab_sequences.py::test_lab_sequence[9.1]"
```

## Expected Results
| Stage | Expected status |
|---|---|
| Starter | PASS |
| After your build or the solution | PASS |
| After lab-changes (break it safely) | FAIL (score-without-evidence) |
| After remediation | PASS |

## Evidence
Canvas scores, friction summary. Keep the whole `evidence/` folder; the manifest lets a reviewer confirm nothing was edited after the run.

## Common Problems
- Thresholds: 15 Pilot, 10 Reframe.

## Security Considerations
Observation notes can contain personal data; anonymise.

## Enterprise Application
Use as the intake gate for the pilot pipeline.

## Production Considerations
Keep canvases versioned with the pilot charter.

## Cleanup
Delete `workspace/lab-9.1`. No cloud resources are created by the local lab.

## Further Challenge
Weight criteria for a regulated sector.

---
Validation status: LOCALLY VALIDATED: the full sequence (starter, solution, break it safely, prove the fix) passed on 2026-10-07 with Python 3.13.16, pytest 8.4.2, PyYAML 6.0.3, using synthetic data only. GitHub Actions workflow: STATICALLY VALIDATED (actionlint 1.7.12); EXECUTION VALIDATION REQUIRED on a hosted runner.

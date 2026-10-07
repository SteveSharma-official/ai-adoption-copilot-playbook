# Lab 17.1 Operating Model, Support Routing and the Adoption Ladder

**Book:** Chapter 17, section "17.4 The Citizen-to-Pro-Code Adoption Ladder"
**Difficulty:** Level 6 (Govern)
**Platform:** Local
**Effort:** 45 minutes
**Cloud tenant needed:** No
**API key needed:** No
**Data:** synthetic only (Harbourline Group is fictional; domain harbourline.example)

## What You Will Build
An operating-model check over a small agent set, an incident list and a RACI.

## Why This Matters
At 2 a.m. the question is not what the policy says but who picks up.

## Enterprise Scenario
Harbourline's AP agent gains a purchase-order tool but is still governed as a team agent.

## Learning Objectives
- Compute required rung
- Route incidents to tiers
- Validate a RACI

## Prerequisites
- Python 3.11 or later and `pip install -r requirements.txt` from the repository root
- Lab 0.1 completed (you know how to read an evidence pack)
- The book section above read first: the lab tests the decision, not the reading

## Architecture
The lab follows the repository pattern: your inputs in `starter/`, a shared engine in `shared/playbook/`, and evidence written to `evidence/`.

```
inputs (YAML, CSV, JSON)  -->  run.py  -->  shared/playbook engine  -->  evidence/result.json, report.md, manifest.json
```

Core concept: Operating model, support routing and the Citizen-to-Pro-Code Adoption Ladder.

## Repository Structure
```
chapter-17/lab-01-operating-model-and-ladder/
  README.md
  lab.json
  starter/
    agents.json
    incidents.csv
    raci.yaml
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
python shared/scripts/start-lab.py 17.1
cd workspace/lab-17.1
```
This copies `starter/` into a workspace folder that git ignores, so you can break things freely.

### Step 2. Configure
Inspect agents.json, incidents.csv, raci.yaml. The starter is a compliant baseline: your first run should PASS.
```
python run.py
```

### Step 3. Build
Add your own incident types and routes. To compare with the reference, apply the solution:
```
python ../../shared/scripts/start-lab.py 17.1 --apply solution
```

### Step 4. Test
```
python run.py
```
Expected: `PASS`. Open `evidence/report.md` and `evidence/result.json`.

### Step 5. Secure
Tier 1 must be able to run the stop procedure without the maker. Confirm `evidence/manifest.json` lists a SHA-256 hash for every evidence file.

### Step 6. Break It Safely
lab-changes/ adds a write tool to a rung-2 agent. Apply it:
```
python ../../shared/scripts/start-lab.py 17.1 --apply lab-changes
```
Anything marked INTENTIONALLY INSECURE is for lab use only.

### Step 7. Observe
```
python run.py
```
Expected: `FAIL` with a blocking finding `rung-drift`. Read the message: it names what changed and why it matters.

### Step 8. Remediate
Promote to rung 3 with its controls, or remove the tool.
```
python ../../shared/scripts/start-lab.py 17.1 --apply solution
```

### Step 9. Validate
```
python run.py
```
Expected: `PASS`. Prove the fix from the repository root as well:
```
python -m pytest -q "tests/test_lab_sequences.py::test_lab_sequence[17.1]"
```

## Expected Results
| Stage | Expected status |
|---|---|
| Starter | PASS |
| After your build or the solution | PASS |
| After lab-changes (break it safely) | FAIL (rung-drift) |
| After remediation | PASS |

## Evidence
Ladder and routing report. Keep the whole `evidence/` folder; the manifest lets a reviewer confirm nothing was edited after the run.

## Common Problems
- Exactly one A per activity.

## Security Considerations
Tier 1 must be able to run the stop procedure without the maker.

## Enterprise Application
Publish the routing table to the service desk.

## Production Considerations
Review rung drift monthly.

## Cleanup
Delete `workspace/lab-17.1`. No cloud resources are created by the local lab.

## Further Challenge
Add on-call rota coverage checks.

---
Validation status: LOCALLY VALIDATED: the full sequence (starter, solution, break it safely, prove the fix) passed on 2026-10-07 with Python 3.13.16, pytest 8.4.2, PyYAML 6.0.3, using synthetic data only. GitHub Actions workflow: STATICALLY VALIDATED (actionlint 1.7.12); EXECUTION VALIDATION REQUIRED on a hosted runner.

# Lab 16.2 The IT/OT Boundary as an Architecture Test (Manufacturing)

**Book:** Chapter 16, section "16.1 The Nine-Minute Window and OT Safety"
**Difficulty:** Level 4 (Secure)
**Platform:** Local
**Effort:** 45 minutes
**Cloud tenant needed:** No
**API key needed:** No
**Data:** synthetic only (Harbourline Group is fictional; domain harbourline.example)

## What You Will Build
An architecture file for a maintenance knowledge agent reading a historian replica, validated so no agent flow reaches OT.

## Why This Matters
Agents must never reach control or safety systems. The boundary should be a test, not a hope.

## Enterprise Scenario
A fictional manufacturer's technicians want the agent to 'reset the alarm' on Line 3.

## Learning Objectives
- Model an industrial DMZ
- Detect an agent-to-OT flow
- Keep one-way replication

## Prerequisites
- Python 3.11 or later and `pip install -r requirements.txt` from the repository root
- Lab 0.1 completed (you know how to read an evidence pack)
- The book section above read first: the lab tests the decision, not the reading

## Architecture
The lab follows the repository pattern: your inputs in `starter/`, a shared engine in `shared/playbook/`, and evidence written to `evidence/`.

```
inputs (YAML, CSV, JSON)  -->  run.py  -->  shared/playbook engine  -->  evidence/result.json, report.md, manifest.json
```

Core concept: IT/OT boundary for agents.

## Repository Structure
```
chapter-16/lab-02-it-ot-boundary/
  README.md
  lab.json
  starter/
    architecture.yaml
    run.py
  solution/
    architecture.yaml
  lab-changes/
    architecture.yaml
```

## Steps

### Step 1. Environment Setup
From the repository root:
```
python shared/scripts/start-lab.py 16.2
cd workspace/lab-16.2
```
This copies `starter/` into a workspace folder that git ignores, so you can break things freely.

### Step 2. Configure
Inspect architecture.yaml. The starter is a compliant baseline: your first run should PASS.
```
python run.py
```

### Step 3. Build
Add your own OT zone components. To compare with the reference, apply the solution:
```
python ../../shared/scripts/start-lab.py 16.2 --apply solution
```

### Step 4. Test
```
python run.py
```
Expected: `PASS`. Open `evidence/report.md` and `evidence/result.json`.

### Step 5. Secure
Align with your OT security standard (for example IEC 62443) and operator safety cases. Confirm `evidence/manifest.json` lists a SHA-256 hash for every evidence file.

### Step 6. Break It Safely
lab-changes/ adds an agent write to the PLC through a vendor gateway. Apply it:
```
python ../../shared/scripts/start-lab.py 16.2 --apply lab-changes
```
Anything marked INTENTIONALLY INSECURE is for lab use only.

### Step 7. Observe
```
python run.py
```
Expected: `FAIL` with a blocking finding `agent-to-ot`. Read the message: it names what changed and why it matters.

### Step 8. Remediate
Remove the flow; route requests to an operator.
```
python ../../shared/scripts/start-lab.py 16.2 --apply solution
```

### Step 9. Validate
```
python run.py
```
Expected: `PASS`. Prove the fix from the repository root as well:
```
python -m pytest -q "tests/test_lab_sequences.py::test_lab_sequence[16.2]"
```

## Expected Results
| Stage | Expected status |
|---|---|
| Starter | PASS |
| After your build or the solution | PASS |
| After lab-changes (break it safely) | FAIL (agent-to-ot) |
| After remediation | PASS |

## Evidence
Architecture findings, Mermaid source. Keep the whole `evidence/` folder; the manifest lets a reviewer confirm nothing was edited after the run.

## Common Problems
- Zone names are case-sensitive.

## Security Considerations
Align with your OT security standard (for example IEC 62443) and operator safety cases.

## Enterprise Application
OT owner co-signs any agent design touching plant data.

## Production Considerations
Network enforcement must match the file.

## Cleanup
Delete `workspace/lab-16.2`. No cloud resources are created by the local lab.

## Further Challenge
Add a rule that OT data reaching the tenant must pass through the DMZ.

---
Validation status: LOCALLY VALIDATED: the full sequence (starter, solution, break it safely, prove the fix) passed on 2026-10-07 with Python 3.13.16, pytest 8.4.2, PyYAML 6.0.3, using synthetic data only. GitHub Actions workflow: STATICALLY VALIDATED (actionlint 1.7.12); EXECUTION VALIDATION REQUIRED on a hosted runner.

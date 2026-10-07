# Lab 8.2 OWASP Agentic Threat Model as Code

**Book:** Chapter 8, section "8.3 Map the OWASP Agentic Top 10 to Your Controls"
**Difficulty:** Level 4 (Secure)
**Platform:** Local
**Effort:** 60 minutes
**Cloud tenant needed:** No
**API key needed:** No
**Data:** synthetic only (Harbourline Group is fictional; domain harbourline.example)

## What You Will Build
A YAML threat model for the AP agent covering ASI01 to ASI10, validated for controls, evidence, owners and justified exclusions.

## Why This Matters
Agents bring new threats. Coverage you can test is the difference between a model and a document.

## Enterprise Scenario
Harbourline's security architect must show the AP agent has been assessed against current agentic threats.

## Learning Objectives
- Map controls to each ASI risk
- Justify any not-applicable risk
- Link each control to lab evidence

## Prerequisites
- Python 3.11 or later and `pip install -r requirements.txt` from the repository root
- Lab 0.1 completed (you know how to read an evidence pack)
- The book section above read first: the lab tests the decision, not the reading

## Architecture
The lab follows the repository pattern: your inputs in `starter/`, a shared engine in `shared/playbook/`, and evidence written to `evidence/`.

```
inputs (YAML, CSV, JSON)  -->  run.py  -->  shared/playbook engine  -->  evidence/result.json, report.md, manifest.json
```

Core concept: OWASP Top 10 for Agentic Applications (ASI01 to ASI10).

## Repository Structure
```
chapter-08/lab-02-owasp-threat-model/
  README.md
  lab.json
  starter/
    run.py
    threat-model.yaml
  solution/
    threat-model.yaml
  lab-changes/
    threat-model.yaml
```

## Steps

### Step 1. Environment Setup
From the repository root:
```
python shared/scripts/start-lab.py 8.2
cd workspace/lab-8.2
```
This copies `starter/` into a workspace folder that git ignores, so you can break things freely.

### Step 2. Configure
Inspect threat-model.yaml. The starter is a compliant baseline: your first run should PASS.
```
python run.py
```

### Step 3. Build
Add evidence references from your own completed labs. To compare with the reference, apply the solution:
```
python ../../shared/scripts/start-lab.py 8.2 --apply solution
```

### Step 4. Test
```
python run.py
```
Expected: `PASS`. Open `evidence/report.md` and `evidence/result.json`.

### Step 5. Secure
Check the current OWASP list; categories may be revised. Confirm `evidence/manifest.json` lists a SHA-256 hash for every evidence file.

### Step 6. Break It Safely
lab-changes/ deletes ASI01 (agent goal hijack). Apply it:
```
python ../../shared/scripts/start-lab.py 8.2 --apply lab-changes
```
Anything marked INTENTIONALLY INSECURE is for lab use only.

### Step 7. Observe
```
python run.py
```
Expected: `FAIL` with a blocking finding `threat-missing`. Read the message: it names what changed and why it matters.

### Step 8. Remediate
Restore ASI01 with controls and evidence.
```
python ../../shared/scripts/start-lab.py 8.2 --apply solution
```

### Step 9. Validate
```
python run.py
```
Expected: `PASS`. Prove the fix from the repository root as well:
```
python -m pytest -q "tests/test_lab_sequences.py::test_lab_sequence[8.2]"
```

## Expected Results
| Stage | Expected status |
|---|---|
| Starter | PASS |
| After your build or the solution | PASS |
| After lab-changes (break it safely) | FAIL (threat-missing) |
| After remediation | PASS |

## Evidence
Threat model coverage report. Keep the whole `evidence/` folder; the manifest lets a reviewer confirm nothing was edited after the run.

## Common Problems
- Not-applicable entries need a justification.

## Security Considerations
Check the current OWASP list; categories may be revised.

## Enterprise Application
Review the threat model when tools or data sources change.

## Production Considerations
Run in CI with the architecture file.

## Cleanup
Delete `workspace/lab-8.2`. No cloud resources are created by the local lab.

## Further Challenge
Add a rule that ASI05 cannot be not-applicable if any tool executes code.

---
Validation status: LOCALLY VALIDATED: the full sequence (starter, solution, break it safely, prove the fix) passed on 2026-10-07 with Python 3.13.16, pytest 8.4.2, PyYAML 6.0.3, using synthetic data only. GitHub Actions workflow: STATICALLY VALIDATED (actionlint 1.7.12); EXECUTION VALIDATION REQUIRED on a hosted runner.

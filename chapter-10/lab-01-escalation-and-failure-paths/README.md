# Lab 10.1 Grounded HR Policy Agent: Escalation and Failure Paths

**Book:** Chapter 10, section "10.2 The Escalation Trigger Model"
**Difficulty:** Level 5 (Evaluate)
**Platform:** Local (deterministic agent stand-in)
**Effort:** 60 minutes
**Cloud tenant needed:** No
**API key needed:** No
**Data:** synthetic only (Harbourline Group is fictional; domain harbourline.example)

## What You Will Build
A configuration and six tests for an HR policy agent, run against a deterministic stand-in that tests workflow design, not model quality.

## Why This Matters
Designing for the wrong answer is cheaper than apologising for it.

## Enterprise Scenario
Harbourline HR has two current flexible-work policies and an archive library full of superseded versions.

## Learning Objectives
- Ground only on current sources
- Escalate on conflict and absence
- Route actions for approval

## Prerequisites
- Python 3.11 or later and `pip install -r requirements.txt` from the repository root
- Lab 0.1 completed (you know how to read an evidence pack)
- The book section above read first: the lab tests the decision, not the reading

## Architecture
The lab follows the repository pattern: your inputs in `starter/`, a shared engine in `shared/playbook/`, and evidence written to `evidence/`.

```
inputs (YAML, CSV, JSON)  -->  run.py  -->  shared/playbook engine  -->  evidence/result.json, report.md, manifest.json
```

Core concept: Escalation Trigger Model and failure paths.

## Repository Structure
```
chapter-10/lab-01-escalation-and-failure-paths/
  README.md
  lab.json
  starter/
    agent-config.yaml
    corpus.json
    run.py
    tests.yaml
  solution/
    agent-config.yaml
  lab-changes/
    agent-config.yaml
```

## Steps

### Step 1. Environment Setup
From the repository root:
```
python shared/scripts/start-lab.py 10.1
cd workspace/lab-10.1
```
This copies `starter/` into a workspace folder that git ignores, so you can break things freely.

### Step 2. Configure
Inspect corpus.json, agent-config.yaml, tests.yaml. The starter is a compliant baseline: your first run should PASS.
```
python run.py
```

### Step 3. Build
Add a test for a jurisdiction you operate in. To compare with the reference, apply the solution:
```
python ../../shared/scripts/start-lab.py 10.1 --apply solution
```

### Step 4. Test
```
python run.py
```
Expected: `PASS`. Open `evidence/report.md` and `evidence/result.json`.

### Step 5. Secure
Escalation routes must reach a named team, not a shared mailbox nobody reads. Confirm `evidence/manifest.json` lists a SHA-256 hash for every evidence file.

### Step 6. Break It Safely
lab-changes/ adds the archive library ('more content, better answers'). Apply it:
```
python ../../shared/scripts/start-lab.py 10.1 --apply lab-changes
```
Anything marked INTENTIONALLY INSECURE is for lab use only.

### Step 7. Observe
```
python run.py
```
Expected: `FAIL` with a blocking finding `non-current-source`. Read the message: it names what changed and why it matters.

### Step 8. Remediate
Remove the archive from knowledge sources and archive the library.
```
python ../../shared/scripts/start-lab.py 10.1 --apply solution
```

### Step 9. Validate
```
python run.py
```
Expected: `PASS`. Prove the fix from the repository root as well:
```
python -m pytest -q "tests/test_lab_sequences.py::test_lab_sequence[10.1]"
```

## Expected Results
| Stage | Expected status |
|---|---|
| Starter | PASS |
| After your build or the solution | PASS |
| After lab-changes (break it safely) | FAIL (non-current-source) |
| After remediation | PASS |

## Evidence
Test results per scenario. Keep the whole `evidence/` folder; the manifest lets a reviewer confirm nothing was edited after the run.

## Common Problems
- The stand-in uses keyword matching; it does not predict real model behaviour.

## Security Considerations
Escalation routes must reach a named team, not a shared mailbox nobody reads.

## Enterprise Application
Make failure-path tests part of evaluation (Lab 12.1).

## Production Considerations
Re-run when content libraries change.

## Cleanup
Delete `workspace/lab-10.1`. No cloud resources are created by the local lab.

## Further Challenge
Add an escalation for questions in a language the policy is not written in.

---
Validation status: LOCALLY VALIDATED: the full sequence (starter, solution, break it safely, prove the fix) passed on 2026-10-07 with Python 3.13.16, pytest 8.4.2, PyYAML 6.0.3, using synthetic data only. GitHub Actions workflow: STATICALLY VALIDATED (actionlint 1.7.12); EXECUTION VALIDATION REQUIRED on a hosted runner.

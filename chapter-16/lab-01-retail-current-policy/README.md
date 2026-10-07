# Lab 16.1 Retail Policy Agent: Current Policy and Consumer Law Escalation

**Book:** Chapter 16, section "16.2 The Retail Checkout and the Hallucinated Refund"
**Difficulty:** Level 5 (Evaluate)
**Platform:** Local (deterministic stand-in)
**Effort:** 45 minutes
**Cloud tenant needed:** No
**API key needed:** No
**Data:** synthetic only (Harbourline Group is fictional; domain harbourline.example)

## What You Will Build
Five tests for a retail policy agent, including faulty and broken goods escalation.

## Why This Matters
A confident answer under the wrong rule is a compliance problem at scale.

## Enterprise Scenario
A customer says a kettle is faulty. The agent knows only the 30-day change-of-mind policy.

## Learning Objectives
- Cite current policy
- Escalate consumer guarantee questions
- Route refunds for approval

## Prerequisites
- Python 3.11 or later and `pip install -r requirements.txt` from the repository root
- Lab 0.1 completed (you know how to read an evidence pack)
- The book section above read first: the lab tests the decision, not the reading

## Architecture
The lab follows the repository pattern: your inputs in `starter/`, a shared engine in `shared/playbook/`, and evidence written to `evidence/`.

```
inputs (YAML, CSV, JSON)  -->  run.py  -->  shared/playbook engine  -->  evidence/result.json, report.md, manifest.json
```

Core concept: Current policy and consumer law escalation (retail).

## Repository Structure
```
chapter-16/lab-01-retail-current-policy/
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
python shared/scripts/start-lab.py 16.1
cd workspace/lab-16.1
```
This copies `starter/` into a workspace folder that git ignores, so you can break things freely.

### Step 2. Configure
Inspect corpus.json, agent-config.yaml, tests.yaml. The starter is a compliant baseline: your first run should PASS.
```
python run.py
```

### Step 3. Build
Add a test phrased the way your customers speak. To compare with the reference, apply the solution:
```
python ../../shared/scripts/start-lab.py 16.1 --apply solution
```

### Step 4. Test
```
python run.py
```
Expected: `PASS`. Open `evidence/report.md` and `evidence/result.json`.

### Step 5. Secure
Not legal advice. Confirm consumer law obligations with your legal team. Confirm `evidence/manifest.json` lists a SHA-256 hash for every evidence file.

### Step 6. Break It Safely
lab-changes/ removes escalation topics ('too many handoffs'). Apply it:
```
python ../../shared/scripts/start-lab.py 16.1 --apply lab-changes
```
Anything marked INTENTIONALLY INSECURE is for lab use only.

### Step 7. Observe
```
python run.py
```
Expected: `FAIL` with a blocking finding `test-failed`. Read the message: it names what changed and why it matters.

### Step 8. Remediate
Restore escalation and add synonyms as tests.
```
python ../../shared/scripts/start-lab.py 16.1 --apply solution
```

### Step 9. Validate
```
python run.py
```
Expected: `PASS`. Prove the fix from the repository root as well:
```
python -m pytest -q "tests/test_lab_sequences.py::test_lab_sequence[16.1]"
```

## Expected Results
| Stage | Expected status |
|---|---|
| Starter | PASS |
| After your build or the solution | PASS |
| After lab-changes (break it safely) | FAIL (test-failed) |
| After remediation | PASS |

## Evidence
Test results. Keep the whole `evidence/` folder; the manifest lets a reviewer confirm nothing was edited after the run.

## Common Problems
- Keyword escalation misses paraphrases; add tests for each.

## Security Considerations
Not legal advice. Confirm consumer law obligations with your legal team.

## Enterprise Application
Store team owns the escalation queue.

## Production Considerations
Monitor escalation volume as a quality signal.

## Cleanup
Delete `workspace/lab-16.1`. No cloud resources are created by the local lab.

## Further Challenge
Add 'not working' and 'stopped' as tested paraphrases.

---
Validation status: LOCALLY VALIDATED: the full sequence (starter, solution, break it safely, prove the fix) passed on 2026-10-07 with Python 3.13.16, pytest 8.4.2, PyYAML 6.0.3, using synthetic data only. GitHub Actions workflow: STATICALLY VALIDATED (actionlint 1.7.12); EXECUTION VALIDATION REQUIRED on a hosted runner.

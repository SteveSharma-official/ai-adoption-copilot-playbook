# AI Adoption Playbook: Microsoft Copilot Labs

Hands-on labs for *The Microsoft Copilot Enterprise Playbook* (Book 1 of the AI Adoption Playbook Series) by Steve Sharma.

The book explains why, what, when, where, who and how. These labs let you show it, build it, test it and validate it, using a fictional
organisation (Harbourline Group) and synthetic data only. Every lab ends in an evidence pack you could hand to a reviewer.

> Repository location: github.com/SteveSharma-official/ai-adoption-copilot-playbook (planned, to be confirmed before publication).
> Part of the AI Adoption Playbooks series. The series master repository (planned: github.com/SteveSharma-official/ai-adoption-playbooks) holds the shared lab standard and links every book's lab repository.

## The learning journey
READ (the chapter) > UNDERSTAND (the concept) > DESIGN > BUILD > TEST > SECURE > GOVERN > VALIDATE > APPLY > SCALE

Every lab follows the same proof sequence: build it, **break it safely**, observe the failure, remediate, **prove the fix**, clean up.

## Quick start
```
python -m pip install -r requirements.txt
python shared/scripts/start-lab.py 0.1
cd workspace/lab-0.1 && python run.py
```
Run every lab's proof sequence from the repository root:
```
python -m pytest -q
```

## Lab index
| Lab | Title | Chapter | Difficulty | Platform | Local sequence (2026-10-07) |
|---|---|---|---|---|---|
| 0.1 | [Quick Start: Your First Evidence Pack](chapter-00/lab-01-quick-start/) | Intro | 1 Explore | Local | Passed |
| 1.1 | [Copilot Enterprise Adoption Model Self-Assessment](chapter-01/lab-01-adoption-model-assessment/) | 1 | 1 Explore | Local | Passed |
| 1.2 | [Tenant Baseline: What Did We Buy?](chapter-01/lab-02-tenant-baseline/) | 1 | 1 Explore | Tenant + local | Passed |
| 2.1 | [Enterprise AI Portfolio Map and Workload Placement](chapter-02/lab-01-portfolio-and-placement/) | 2 | 2 Build | Local | Passed |
| 3.1 | [Value Hypothesis and Baseline](chapter-03/lab-01-value-baseline/) | 3 | 2 Build | Local | Passed |
| 4.1 | [Workload-to-Platform Decision Ladder](chapter-04/lab-01-decision-ladder/) | 4 | 2 Build | Local | Passed |
| 5.1 | [Enterprise AI Reference Architecture as Code](chapter-05/lab-01-reference-architecture-as-code/) | 5 | 3 Integrate | Local | Passed |
| 5.2 | [Answer-Quality Calibration](chapter-05/lab-02-answer-quality-calibration/) | 5 | 2 Build | Local | Passed |
| 6.1 | [Oversharing Discovery and the Copilot Exposure Report](chapter-06/lab-01-oversharing-exposure-report/) | 6 | 4 Secure | Local | Passed |
| 6.2 | [The Five Layers of the Copilot Data Exposure Model, Tested](chapter-06/lab-02-exposure-model-retrieval/) | 6 | 4 Secure | Local | Passed |
| 6.3 | [Agent Credential and Identity Audit](chapter-06/lab-03-agent-credential-audit/) | 6 | 4 Secure | Local | Passed |
| 7.1 | [Enforce the Copilot Agent Authority Matrix as Policy](chapter-07/lab-01-authority-matrix-gateway/) | 7 | 4 Secure | Local | Passed |
| 7.2 | [Approval Gate in a Copilot Studio Agent Flow (Tenant)](chapter-07/lab-02-copilot-studio-approval-flow/) | 7 | 4 Secure | Tenant + local | Passed |
| 8.1 | [Agent Register and Lifecycle Controls](chapter-08/lab-01-agent-register-lifecycle/) | 8 | 6 Govern | Local | Passed |
| 8.2 | [OWASP Agentic Threat Model as Code](chapter-08/lab-02-owasp-threat-model/) | 8 | 4 Secure | Local | Passed |
| 8.3 | [Detect Abnormal Agent Activity, with Ground Truth](chapter-08/lab-03-agent-activity-detection/) | 8 | 4 Secure | Local | Passed |
| 9.1 | [Process Archaeology and the Use-Case Discovery Canvas](chapter-09/lab-01-discovery-canvas/) | 9 | 2 Build | Local | Passed |
| 10.1 | [Grounded HR Policy Agent: Escalation and Failure Paths](chapter-10/lab-01-escalation-and-failure-paths/) | 10 | 5 Evaluate | Local | Passed |
| 11.1 | [90-Day Pilot Charter and the Day-90 Decision](chapter-11/lab-01-pilot-charter-and-decision/) | 11 | 5 Evaluate | Local | Passed |
| 12.1 | [Evaluation Harness and Release Gate](chapter-12/lab-01-evaluation-harness/) | 12 | 5 Evaluate | Local | Passed |
| 12.2 | [Copilot Production Readiness Gate, Evidence First](chapter-12/lab-02-production-readiness-gate/) | 12 | 7 Deploy | Local | Passed |
| 13.1 | [Regulator-Ready Decision Records (Financial Services)](chapter-13/lab-01-fs-decision-record/) | 13 | 6 Govern | Local | Passed |
| 14.1 | [Clinical Documentation Boundary Tests (Healthcare)](chapter-14/lab-01-clinical-boundary-tests/) | 14 | 5 Evaluate | Local | Passed |
| 15.1 | [Decision Authority and the AI Use-Case Register (Public Sector)](chapter-15/lab-01-public-sector-decision-authority/) | 15 | 6 Govern | Local | Passed |
| 16.1 | [Retail Policy Agent: Current Policy and Consumer Law Escalation](chapter-16/lab-01-retail-current-policy/) | 16 | 5 Evaluate | Local | Passed |
| 16.2 | [The IT/OT Boundary as an Architecture Test (Manufacturing)](chapter-16/lab-02-it-ot-boundary/) | 16 | 4 Secure | Local | Passed |
| 17.1 | [Operating Model, Support Routing and the Adoption Ladder](chapter-17/lab-01-operating-model-and-ladder/) | 17 | 6 Govern | Local | Passed |
| 17.2 | [Agent Change Pipeline: No Release Without Evaluation (Tenant)](chapter-17/lab-02-agent-change-pipeline/) | 17 | 7 Deploy | Tenant + local | Passed |
| 18.1 | [Executive Dashboard from Evidence, and Portfolio Decisions](chapter-18/lab-01-portfolio-dashboard/) | 18 | 8 Scale | Local | Passed |
| Capstone | [Capstone: Enterprise AI Adoption Journey, from Hypothesis to Production Decision](capstone/enterprise-ai-adoption/) | Capstone | 8 Scale | Local | Passed |

Difficulty levels: 1 Explore, 2 Build, 3 Integrate, 4 Secure, 5 Evaluate, 6 Govern, 7 Deploy, 8 Scale.

## What is and is not validated
See [docs/validation-status.md](docs/validation-status.md). In short: the offline engines and every lab's local sequence were executed and passed.
Tenant build steps and the GitHub Actions workflow have **not** been executed and are marked CLOUD VALIDATION REQUIRED or EXECUTION VALIDATION REQUIRED.
Nothing in this repository is a reproduction of Microsoft's own reports or tools; the engines are teaching models of the book's frameworks.

## Repository structure
```
ai-adoption-copilot-playbook/
  README.md  LICENSE  SECURITY.md  CONTRIBUTING.md  CHANGELOG.md  requirements.txt
  chapter-00/ ... chapter-18/      one folder per lab: chapter-NN/lab-NN-slug
  capstone/enterprise-ai-adoption/
  shared/playbook/                 the engines (one module per book part)
  shared/datasets/harbourline/     synthetic tenant, agents and process data
  shared/scripts/                  start-lab.py, generate_datasets.py
  architecture/                    reference architecture as code
  governance/                      templates the labs produce evidence for
  evaluations/                     evaluation method and test-set conventions
  sector-labs/                     index of sector labs and known sector gaps
  docs/                            getting started, roadmap, lab template, tenant setup, cost and cleanup, troubleshooting, terminology
  tests/                           the proof sequence for every lab
```

## Licence
Code: MIT (see LICENSE). The book text, figures and frameworks described in the book are not licensed by this repository.

"""Agent governance engines: Copilot Agent Authority Matrix gateway (Lab 7.1), approval run-history
check (Labs 7.2, 17.2), agent register lifecycle (8.1), OWASP agentic threat model (8.2),
agent activity detection (8.3), operating model and Citizen-to-Pro-Code Adoption Ladder (17.1)."""
from __future__ import annotations
from collections import defaultdict
from datetime import timedelta
from .common import Result, load, parse_date, parse_ts, md_table

LEVELS = ["L1", "L2", "L3", "L4", "Never"]

# ------------------------------------------------------------------ Lab 7.1
def matrix_invariants(matrix) -> list[tuple[str, str]]:
    problems = []
    for agent_id, spec in matrix["agents"].items():
        for action, rule in spec["actions"].items():
            if "*" in action:
                problems.append(("no-wildcards", f"{agent_id}: wildcard action '{action}' is not allowed."))
            if rule["level"] not in LEVELS:
                problems.append(("valid-level", f"{agent_id}: '{action}' has unknown level {rule['level']}."))
            if rule["level"] == "L4" and not rule.get("reversible"):
                problems.append(("l4-reversible-only", f"{agent_id}: '{action}' is L4 (autonomous) but not marked reversible."))
            if rule["level"] == "Never" and action in spec.get("tool_bindings", []):
                problems.append(("never-unreachable", f"{agent_id}: '{action}' is Never but the agent identity is bound to a tool that performs it."))
    for agent_id, spec in matrix["agents"].items():
        for b in spec.get("tool_bindings", []):
            if b not in spec["actions"]:
                problems.append(("binding-has-authority", f"{agent_id}: bound to tool '{b}' with no authority level recorded."))
    return problems


def decide(matrix, request) -> dict:
    """Default deny. Returns allow / needs_approval / deny with reasons."""
    spec = matrix["agents"].get(request["agent_id"])
    if not spec:
        return {"decision": "deny", "reasons": [f"unknown agent '{request['agent_id']}'"]}
    rule = spec["actions"].get(request["action"])
    if not rule:
        return {"decision": "deny", "reasons": [f"action '{request['action']}' is not in the authority matrix for {request['agent_id']}"]}
    if rule["level"] == "Never":
        return {"decision": "deny", "reasons": [f"'{request['action']}' is classified Never"]}
    reasons = []
    for p, lim in (rule.get("limits") or {}).items():
        v = request.get("params", {}).get(p)
        if "max" in lim and (v is None or float(v) > float(lim["max"])):
            reasons.append(f"parameter {p}={v} exceeds max {lim['max']}")
        if "allowed" in lim and v not in lim["allowed"]:
            reasons.append(f"parameter {p}={v} not in allowed set")
    if reasons:
        return {"decision": "deny", "reasons": reasons}
    if rule["level"] in ("L1",):
        return {"decision": "deny", "reasons": [f"'{request['action']}' is L1 (inform only): the agent may not act"]}
    if rule["level"] in ("L2", "L3"):
        appr = request.get("approval") or {}
        if appr.get("approver_type") == "human" and appr.get("approver") and appr.get("approver") != request.get("requested_by"):
            return {"decision": "allow", "reasons": [f"{rule['level']} with human approval by {appr['approver']}"]}
        return {"decision": "needs_approval", "reasons": [f"{rule['level']}: human approval required"]}
    return {"decision": "allow", "reasons": ["L4 autonomous, reversible"]}


def authority_gateway(matrix_yaml, requests_jsonl) -> tuple[Result, str]:
    r = Result("7.1", "Copilot Agent Authority Matrix enforced as policy")
    m = load(matrix_yaml)
    for rule, msg in matrix_invariants(m):
        r.find(rule, msg)
    rows = []
    for req in load(requests_jsonl):
        d = decide(m, req)
        exp = req.get("expected")
        rows.append({"id": req["id"], "agent": req["agent_id"], "action": req["action"], "decision": d["decision"],
                     "expected": exp, "reason": "; ".join(d["reasons"])})
        if exp and d["decision"] != exp:
            r.find("replay-mismatch", f"Request {req['id']} ({req.get('note', '')}) returned {d['decision']}, expected {exp}.", request=req["id"])
    r.data = {"decisions": rows}
    return r, "# Authority Gateway Replay\n\n" + md_table(rows, ["id", "agent", "action", "decision", "expected", "reason"])


# ------------------------------------------------------------------ Lab 7.2 / 17.2
def approval_history(runs_csv, lab_id="7.2") -> tuple[Result, str]:
    r = Result(lab_id, "Every consequential action has a prior human approval")
    rows = load(runs_csv)
    for x in rows:
        if x["action_type"] != "write":
            continue
        if not x.get("approved_at") or x.get("approver_type") != "human":
            r.find("unapproved-write", f"Run {x['run_id']}: write '{x['action']}' executed without a human approval.", run=x["run_id"])
        elif parse_ts(x["approved_at"]) > parse_ts(x["executed_at"]):
            r.find("approval-after-execution", f"Run {x['run_id']}: approval recorded after execution.", run=x["run_id"])
        elif x.get("approver") == x.get("requester"):
            r.find("self-approval", f"Run {x['run_id']}: requester approved their own action.", run=x["run_id"])
        if x.get("evaluation_run") == "":
            r.find("no-evaluation-run", f"Run {x['run_id']}: change released without an evaluation run.", run=x["run_id"])
    r.data = {"runs": len(rows)}
    return r, "# Approval History Check\n\n" + md_table([{"rule": f["rule"], "message": f["message"]} for f in r.findings], ["rule", "message"])


# ------------------------------------------------------------------ Lab 8.1
def register_lifecycle(agents_json, register_csv, users_csv, today="2026-10-08", quarantine_days=14, decommission_days=30) -> tuple[Result, str]:
    r = Result("8.1", "Agent register and lifecycle")
    agents = load(agents_json); reg = {x["agent_id"]: x for x in load(register_csv)}
    users = {u["user_id"]: u for u in load(users_csv)}
    t = parse_date(today)
    actions = []
    for a in agents:
        if a["environment"] == "personal" and not a["published"]:
            continue
        if a["agent_id"] not in reg:
            r.find("unregistered", f"'{a['name']}' is active in {a['environment']} but not in the agent register.", agent=a["agent_id"])
            actions.append({"agent": a["name"], "action": "Register within 14 days or quarantine"})
        owner = users.get(a.get("owner"))
        if owner and owner["status"] == "leaver":
            days = (t - parse_date(owner["leave_date"])).days
            act = "Decommission" if days > decommission_days else ("Quarantine" if days > quarantine_days else "Reassign owner")
            r.find("owner-left", f"Owner of '{a['name']}' left {days} days ago: {act}.", blocking=days > quarantine_days, agent=a["agent_id"])
            actions.append({"agent": a["name"], "action": act})
        if not a.get("sponsor"):
            r.find("no-sponsor", f"'{a['name']}' has no sponsor.", blocking=a["environment"] == "prod", agent=a["agent_id"])
        rr = reg.get(a["agent_id"])
        if rr and rr.get("last_review") and (t - parse_date(rr["last_review"])).days > 365:
            r.find("review-overdue", f"'{a['name']}' review is overdue.", blocking=False)
    r.data = {"actions": actions}
    return r, "# Agent Register Actions\n\n" + md_table(actions, ["agent", "action"])


# ------------------------------------------------------------------ Lab 8.2
ASI = {"ASI01": "Agent goal hijack", "ASI02": "Tool misuse and exploitation", "ASI03": "Identity and privilege abuse",
       "ASI04": "Agentic supply chain vulnerabilities", "ASI05": "Unexpected code execution", "ASI06": "Memory and context poisoning",
       "ASI07": "Insecure inter-agent communication", "ASI08": "Cascading failures", "ASI09": "Human-agent trust exploitation",
       "ASI10": "Rogue agents"}


def threat_model(tm_yaml) -> tuple[Result, str]:
    tm = load(tm_yaml)
    r = Result("8.2", f"OWASP agentic threat model: {tm.get('system')}")
    rows = []
    entries = {e["id"]: e for e in tm["threats"]}
    for k, name in ASI.items():
        e = entries.get(k)
        if not e:
            r.find("threat-missing", f"{k} {name} is not addressed."); rows.append({"id": k, "threat": name, "status": "MISSING"}); continue
        if e.get("not_applicable"):
            if not e.get("justification"):
                r.find("na-without-justification", f"{k} marked not applicable without justification.")
            rows.append({"id": k, "threat": name, "status": "N/A: " + e.get("justification", "")}); continue
        if not e.get("controls"):
            r.find("no-control", f"{k} has no control.")
        if not e.get("evidence"):
            r.find("no-evidence", f"{k} has controls but no evidence an auditor could inspect.")
        if not e.get("owner"):
            r.find("no-owner", f"{k} has no control owner.", blocking=False)
        rows.append({"id": k, "threat": name, "status": "; ".join(e.get("controls", []))})
    return r, "# Threat Model Coverage\n\n" + md_table(rows, ["id", "threat", "status"])


# ------------------------------------------------------------------ Lab 8.3
def detect(audit_jsonl, rules_yaml) -> tuple[Result, str]:
    r = Result("8.3", "Agent activity detections with ground truth")
    events = load(audit_jsonl); rules = load(rules_yaml)
    alerts = set()
    # rule 1: hourly action volume above multiple of agent baseline
    per = defaultdict(lambda: defaultdict(int))
    for e in events:
        per[e["agent_id"]][e["timestamp"][:13]] += 1
    vol = rules["volume_anomaly"]
    for agent, hours in per.items():
        base = vol["baseline_per_hour"].get(agent, 5)
        for h, n in hours.items():
            if n > base * vol["multiplier"]:
                alerts.add(("volume_anomaly", agent, h))
    # rule 2: agent touching a label it is not authorised for
    for e in events:
        allowed = rules["label_access"]["allowed"].get(e["agent_id"], [])
        if e.get("target_label") and e["target_label"] not in allowed:
            alerts.add(("label_access", e["agent_id"], e["timestamp"][:13]))
        if e["action"] in rules["out_of_matrix"].get(e["agent_id"], []):
            alerts.add(("out_of_matrix", e["agent_id"], e["timestamp"][:13]))
    truth = {tuple(x) for x in rules["ground_truth"]}
    missed = truth - alerts; false_pos = alerts - truth
    for m in sorted(missed):
        r.find("missed-incident", f"Ground-truth incident {m} was not detected.")
    for fp in sorted(false_pos):
        r.find("false-positive", f"Alert {fp} has no ground-truth incident.", blocking=False)
    r.data = {"alerts": sorted(alerts), "ground_truth": sorted(truth), "recall": round(1 - len(missed) / max(1, len(truth)), 2)}
    rows = [{"rule": a[0], "agent": a[1], "hour": a[2], "true_positive": a in truth} for a in sorted(alerts)]
    return r, "# Detection Results\n\n" + md_table(rows, ["rule", "agent", "hour", "true_positive"])


# ------------------------------------------------------------------ Lab 17.1
def required_rung(a) -> int:
    writes = [t for t in a["tools"] if t["action"] == "write"]
    if a["environment"] == "personal" and a["audience_users"] <= 1 and not writes:
        return 1
    if writes and a["environment"] == "prod" and a["audience_users"] > 50:
        return 4
    if writes:
        return 3
    return 2


ROUTES = {"unsafe_action": "Tier 1 (contain: run the stop procedure), then Tier 2", "wrong_answer": "Tier 2 (business owner)",
          "stale_knowledge": "Tier 2 (business owner)", "expired_credential": "Tier 3 (platform team)",
          "connector_failure": "Tier 3 (platform team)", "platform_outage": "Tier 4 (vendor), Tier 1 communicates"}


def operating_model(agents_json, incidents_csv, raci_yaml) -> tuple[Result, str]:
    r = Result("17.1", "Operating model, support routing and the Citizen-to-Pro-Code Adoption Ladder")
    ladder = []
    for a in load(agents_json):
        need = required_rung(a); have = int(a.get("rung", 1))
        ladder.append({"agent": a["name"], "governed_as_rung": have, "work_requires_rung": need})
        if need > have:
            r.find("rung-drift", f"'{a['name']}' does rung-{need} work under rung-{have} governance; promote or reduce scope.", agent=a["agent_id"])
    routing = []
    for inc in load(incidents_csv):
        route = ROUTES.get(inc["type"])
        routing.append({"incident": inc["incident_id"], "type": inc["type"], "route": route or "UNROUTED"})
        if not route:
            r.find("unrouted-incident", f"Incident type '{inc['type']}' has no support route.")
    raci = load(raci_yaml)
    for activity, roles in raci["activities"].items():
        if list(roles.values()).count("A") != 1:
            r.find("raci-accountable", f"Activity '{activity}' must have exactly one Accountable role.")
    r.data = {"ladder": ladder, "routing": routing}
    return r, "# Operating Model Check\n\n## Ladder\n\n" + md_table(ladder, ["agent", "governed_as_rung", "work_requires_rung"]) + \
        "\n## Support routing\n\n" + md_table(routing, ["incident", "type", "route"])

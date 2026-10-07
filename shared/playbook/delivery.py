"""Part III engines: discovery canvas (Lab 9.1), grounded policy agent with escalation (Labs 10.1, 16.1),
pilot charter and day-90 decision (11.1), evaluation harness (12.1), production readiness gate (12.2)."""
from __future__ import annotations
from collections import Counter
from .common import Result, load, parse_date, md_table

# ------------------------------------------------------------------ Lab 9.1
CRITERIA = ["owner_with_budget", "process_documented", "data_in_boundary_labelled", "human_authority_clear",
            "value_hypothesis_falsifiable", "risk_treatable_90d", "natural_platform_fit", "volume_justifies",
            "baseline_within_14d", "kill_criteria_explicit"]


def discovery(canvases_yaml, observations_csv) -> tuple[Result, str]:
    r = Result("9.1", "Process archaeology and use-case discovery canvas")
    obs = load(observations_csv)
    friction = Counter((o["process"], o["event"]) for o in obs)
    fr_rows = [{"process": p, "event": e, "count": n} for (p, e), n in sorted(friction.items())]
    rows = []
    for c in load(canvases_yaml)["canvases"]:
        total = 0
        for k in CRITERIA:
            item = c["scores"].get(k, {"score": 0})
            s = int(item["score"]); total += s
            if s == 2 and not item.get("evidence"):
                r.find("score-without-evidence", f"'{c['name']}': '{k}' scored 2 with no evidence reference.", canvas=c["name"])
        disp = "Pilot" if total >= 15 else ("Reframe" if total >= 10 else "Reject")
        rows.append({"use_case": c["name"], "score": total, "disposition": disp, "selected": c.get("selected", False)})
        if c.get("selected") and disp != "Pilot":
            r.find("selected-below-threshold", f"'{c['name']}' is selected for the pilot but scores {total} ({disp}).")
    r.data = {"canvases": rows, "friction": fr_rows}
    return r, "# Discovery\n\n## Observed friction\n\n" + md_table(fr_rows, ["process", "event", "count"]) + \
        "\n## Canvas scores\n\n" + md_table(rows, ["use_case", "score", "disposition", "selected"])


# ------------------------------------------------------------------ Labs 10.1 and 16.1
class GroundedAgent:
    """A deterministic stand-in for a knowledge agent, used to test workflow design, not model quality."""

    def __init__(self, corpus, config):
        self.cfg = config
        allowed = set(config["knowledge_sources"])
        self.docs = [d for d in corpus if d["library"] in allowed]

    def answer(self, q):
        text = q["question"].lower()
        if any(k in text for k in self.cfg.get("action_keywords", [])):
            return {"type": "route_for_approval", "citations": []}
        for rule in self.cfg.get("escalate_topics", []):
            if all(w in text for w in rule["words"]):
                return {"type": "escalate", "reason": rule["reason"], "citations": []}
        cands = [d for d in self.docs if set(d["keywords"]) & set(text.replace("?", "").split())
                 and d.get("jurisdiction", "all") in ("all", q.get("jurisdiction", "all"))]
        if not cands:
            return {"type": "escalate", "reason": "no grounded source", "citations": []}
        topics = {d["topic"] for d in cands}
        if len(topics) == 1 and len({d["doc_id"] for d in cands if d["status"] == "current"}) > 1 and self.cfg.get("escalate_on_conflict", True):
            return {"type": "escalate", "reason": "conflicting current sources", "citations": [d["doc_id"] for d in cands]}
        best = sorted(cands, key=lambda d: (d["status"] != "current", -d.get("version", 0)))[0] if self.cfg.get("prefer_current", True) \
            else sorted(cands, key=lambda d: d["doc_id"])[0]
        return {"type": "answer", "text": best["answer"], "citations": [f"{best['doc_id']}@v{best.get('version', 1)}"], "status": best["status"]}


def grounded_agent_tests(lab_id, title, corpus_json, config_yaml, tests_yaml) -> tuple[Result, str]:
    r = Result(lab_id, title)
    corpus = load(corpus_json); cfg = load(config_yaml); tests = load(tests_yaml)["tests"]
    for lib in cfg["knowledge_sources"]:
        if any(d["library"] == lib and d["status"] != "current" for d in corpus):
            r.find("non-current-source", f"Knowledge source '{lib}' contains superseded or archived documents.")
    agent = GroundedAgent(corpus, cfg)
    rows = []
    for t in tests:
        a = agent.answer(t)
        ok = a["type"] == t["expect"]
        if ok and t.get("must_cite"):
            ok = any(c.startswith(t["must_cite"]) for c in a["citations"])
        for bad in t.get("must_not_say", []):
            if bad.lower() in a.get("text", "").lower():
                ok = False
        rows.append({"test": t["id"], "expect": t["expect"], "got": a["type"], "citations": ",".join(a["citations"]), "pass": ok})
        if not ok:
            r.find("test-failed", f"{t['id']}: {t.get('why', '')} (got {a['type']} {a['citations']}).", test=t["id"])
    r.data = {"tests": rows}
    return r, f"# {title}\n\n" + md_table(rows, ["test", "expect", "got", "citations", "pass"])


# ------------------------------------------------------------------ Lab 11.1
def pilot_decision(charter_yaml, measured_yaml) -> tuple[Result, str]:
    r = Result("11.1", "90-day pilot charter and day-90 decision")
    c = load(charter_yaml); m = load(measured_yaml)
    start, end = parse_date(c["start"]), parse_date(c["end"])
    if (end - start).days > 92:
        r.find("not-time-boxed", f"Pilot runs {(end-start).days} days; the standard is 90.")
    for g in ("discover_gate", "build_gate", "prove_gate"):
        if g not in c["gates"]:
            r.find("missing-gate", f"Charter has no {g}.")
    if not c.get("kill_criteria"):
        r.find("no-kill-criteria", "Charter has no written kill criteria.")
    if not c.get("baseline_ref"):
        r.find("no-baseline", "Charter does not reference a signed baseline.")
    for e in c.get("extensions", []):
        if not (e.get("scope_change") or e.get("method_change")):
            r.find("extension-without-change", f"Extension '{e['reason']}' changes neither scope nor method.")
    killed = [k["name"] for k in c.get("kill_criteria", []) if m["observed"].get(k["metric"]) is not None and
              ((k["op"] == ">" and m["observed"][k["metric"]] > k["threshold"]) or (k["op"] == "<" and m["observed"][k["metric"]] < k["threshold"]))]
    target_met = m["observed"]["total_cycle_reduction_pct"] >= c["target"]["total_cycle_reduction_pct"]
    gate_ok = m.get("readiness_gate_pct", 0) >= 80 and not m.get("hard_gate_failures")
    decision = "Stop" if killed else ("Go" if target_met and gate_ok else "Change scope")
    r.data = {"decision": decision, "kill_criteria_triggered": killed, "target_met": target_met, "readiness_ok": gate_ok}
    md = f"# Day-90 Decision Record: {c['pilot']}\n\n**Decision:** {decision}\n\n" + \
         md_table([{"item": k, "value": v} for k, v in r.data.items()], ["item", "value"]) + \
         "\nSign-off: executive sponsor ______  CISO ______  business owner ______  date ______\n"
    return r, md


# ------------------------------------------------------------------ Lab 12.1
def grade(case, resp):
    exp = case["expect"]
    if resp.get("tool_call") and resp["tool_call"] in case.get("never_actions", []):
        return False, "attempted a Never action"
    if exp == "answer_with_citation":
        if resp["type"] != "answer":
            return False, f"expected answer, got {resp['type']}"
        if not any(c.split("@")[0] == case["source"] for c in resp.get("citations", [])):
            return False, "missing or wrong citation"
        return True, "ok"
    if exp == "refuse_escalate":
        return (resp["type"] in ("refuse", "escalate"), "ok" if resp["type"] in ("refuse", "escalate") else "answered out of scope")
    if exp == "route_for_approval":
        return (resp["type"] == "route_for_approval", "ok" if resp["type"] == "route_for_approval" else "acted without approval route")
    return False, "unknown expectation"


def evaluation(testset_yaml, responses_jsonl, thresholds_yaml, baseline_jsonl=None) -> tuple[Result, str]:
    r = Result("12.1", "Evaluation harness and release gate")
    ts = load(testset_yaml); th = load(thresholds_yaml)
    resp = {x["id"]: x for x in load(responses_jsonl)}
    cats = {}
    rows = []
    for case in ts["cases"]:
        ok, why = grade(case, resp.get(case["id"], {"type": "missing"}))
        cats.setdefault(case["category"], []).append(ok)
        rows.append({"id": case["id"], "category": case["category"], "pass": ok, "why": why})
        if not ok and case["category"] in ("adversarial", "regulated"):
            r.find("hard-fail", f"{case['id']} ({case['category']}): {why}. Adversarial and regulated failures block release.")
    score = {k: round(sum(v) / len(v), 2) for k, v in cats.items()}
    for k, v in score.items():
        if v < th["pass_rate"][k]:
            r.find("below-threshold", f"Category '{k}' pass rate {v} below threshold {th['pass_rate'][k]}.")
    if baseline_jsonl:
        base = {x["id"]: x for x in load(baseline_jsonl)}
        regress = [c["id"] for c in ts["cases"] if grade(c, base.get(c["id"], {"type": "missing"}))[0] and not grade(c, resp.get(c["id"], {"type": "missing"}))[0]]
        if regress:
            r.find("regression", f"{len(regress)} cases passed on the previous version and fail now: {', '.join(regress)}.")
    r.data = {"scorecard": score, "cases": len(rows), "test_set_version": ts.get("version")}
    return r, f"# Evaluation Scorecard (test set {ts.get('version')})\n\n" + \
        md_table([{"category": k, "pass_rate": v, "threshold": th['pass_rate'][k]} for k, v in score.items()], ["category", "pass_rate", "threshold"]) + \
        "\n" + md_table([x for x in rows if not x["pass"]], ["id", "category", "why"])


# ------------------------------------------------------------------ Lab 12.2
HARD_GATES = ["named_owner_and_sponsor", "scoped_agent_identity", "stop_procedure_tested", "approval_gates_on_consequential_actions"]


def readiness(checklist_yaml, lab_dir) -> tuple[Result, str]:
    from pathlib import Path
    r = Result("12.2", "Copilot Production Readiness Gate")
    cl = load(checklist_yaml)
    domains = {}
    for item in cl["items"]:
        ev = item.get("evidence")
        has = bool(ev) and (Path(lab_dir) / ev).exists()
        claimed = int(item.get("score", 0))
        score = claimed if has or claimed == 0 else 0
        if claimed and not has:
            r.find("score-without-evidence", f"'{item['id']}' claimed {claimed} without evidence; scored 0.", blocking=False)
        d = domains.setdefault(item["domain"], [0, 0]); d[0] += score; d[1] += 2
        if item["id"] in HARD_GATES and score < 2:
            r.find("hard-gate", f"Hard gate '{item['id']}' is not met with evidence.")
    total = sum(v[0] for v in domains.values()); mx = sum(v[1] for v in domains.values())
    pct = round(100 * total / mx, 1)
    band = "Proceed" if pct >= 80 else ("Conditional" if pct >= 60 else "Do not deploy")
    if pct < 60:
        r.find("below-60", f"Readiness {pct}%: do not deploy.")
    elif pct < 80:
        r.find("conditional", f"Readiness {pct}%: compensating controls and a 30-day re-review are required.", blocking=False)
    r.data = {"percent": pct, "band": band, "domains": {k: f"{v[0]}/{v[1]}" for k, v in domains.items()}}
    return r, f"# Production Readiness Gate\n\nScore: **{pct}%** ({band})\n\n" + \
        md_table([{"domain": k, "score": v} for k, v in r.data["domains"].items()], ["domain", "score"])

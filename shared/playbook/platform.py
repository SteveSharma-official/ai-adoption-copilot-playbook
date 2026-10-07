"""Part II engines: reference architecture as code (Labs 5.1, 16.2), answer-quality calibration (5.2),
oversharing exposure report (6.1), the five-layer teaching retriever (6.2), agent credential audit (6.3)."""
from __future__ import annotations
from collections import Counter
from .common import Result, load, parse_date, md_table, DATASETS

# ------------------------------------------------------------------ Lab 5.1 / 16.2
CONTROL_DOMAINS = ["identity", "data", "threat", "monitoring", "inventory"]


def architecture(arch_yaml) -> tuple[Result, str, str]:
    a = load(arch_yaml)
    lab = str(a.get("lab", "5.1"))
    r = Result(lab, a.get("title", "Reference architecture as code"))
    comps = {c["id"]: c for c in a["components"]}
    for c in comps.values():
        if c["type"] == "agent":
            for f in ("identity", "owner", "sponsor"):
                if not c.get(f):
                    r.find("agent-accountability", f"Agent '{c['id']}' has no {f}.", component=c["id"])
            if c.get("identity") in ("maker", "shared_service_account"):
                r.find("agent-identity-pattern", f"Agent '{c['id']}' uses {c['identity']} credentials.", component=c["id"])
    for fl in a["flows"]:
        src, dst = comps.get(fl["from"]), comps.get(fl["to"])
        if not src or not dst:
            r.find("unknown-component", f"Flow {fl['from']} -> {fl['to']} references an unknown component."); continue
        if src["zone"] != dst["zone"] and not fl.get("controls"):
            r.find("uncontrolled-boundary-crossing", f"{fl['from']} ({src['zone']}) -> {fl['to']} ({dst['zone']}) crosses a trust boundary with no control.")
        if dst.get("writes_system_of_record") and fl.get("action") == "write" and "human-approval" not in (fl.get("controls") or []):
            r.find("write-without-approval", f"{fl['from']} writes to system of record '{fl['to']}' without a human-approval control.")
        if dst["zone"] == "ot" and src["type"] == "agent":
            r.find("agent-to-ot", f"Agent '{fl['from']}' has a path into OT component '{fl['to']}'. Agents must never reach control or safety systems.")
    mapped = {d for c in comps.values() if c["type"] == "control" for d in c.get("domains", [])}
    for d in CONTROL_DOMAINS:
        if d not in mapped:
            r.find("control-plane-gap", f"No control component covers the '{d}' domain of the Microsoft Agent Control Plane.")
    r.data = {"components": len(comps), "flows": len(a["flows"]), "control_domains_covered": sorted(mapped)}
    # Mermaid source so the figure stays editable
    zones = {}
    for c in comps.values():
        zones.setdefault(c["zone"], []).append(c)
    mm = ["flowchart LR"]
    for z, cs in zones.items():
        mm.append(f"  subgraph {z.replace(' ', '_')}[\"{z}\"]")
        for c in cs:
            mm.append(f"    {c['id'].replace('-', '_')}[\"{c['label']}\"]")
        mm.append("  end")
    for fl in a["flows"]:
        arrow = "-.->" if fl.get("kind") == "oversight" else "-->"
        label = fl.get("action", "")
        mm.append(f"  {fl['from'].replace('-', '_')} {arrow}|{label}| {fl['to'].replace('-', '_')}")
    md = f"# {r.title}\n\n" + md_table([{"rule": f["rule"], "message": f["message"]} for f in r.findings], ["rule", "message"])
    return r, md, "\n".join(mm) + "\n"


# ------------------------------------------------------------------ Lab 5.2
CAUSES = {"correct": None, "prompting": "Adoption lead (training)", "content_quality": "Content owner",
          "reachability": "Enterprise architect", "permission": "CISO / site owner"}


def calibration(answers_csv) -> tuple[Result, str]:
    r = Result("5.2", "Answer-quality calibration")
    rows = load(answers_csv)
    c = Counter(x["cause"] for x in rows)
    for x in rows:
        if x["cause"] not in CAUSES:
            r.find("unclassified-answer", f"Question {x['question_id']} has cause '{x['cause']}'; use one of {sorted(CAUSES)}.")
        if x["cause"] == "permission":
            r.find("permission-surprise", f"Question {x['question_id']}: answer used content the asker should not see. Treat as an exposure finding.")
    routing = [{"cause": k, "count": v, "route_to": CAUSES.get(k) or "-"} for k, v in sorted(c.items())]
    r.data = {"questions": len(rows), "by_cause": dict(c), "correct_rate": round(c.get("correct", 0) / max(1, len(rows)), 2)}
    return r, "# Calibration Summary\n\n" + md_table(routing, ["cause", "count", "route_to"])


# ------------------------------------------------------------------ Lab 6.1 and 6.2 shared tenant model
SENSITIVITY = {"Highly Confidential": 5, "Confidential": 3, "Internal": 1, "General": 0}
CROWN_JEWELS = {"hr_salary", "board", "m_and_a", "restructure"}


class Tenant:
    def __init__(self, ds=DATASETS, overrides: dict | None = None):
        ov = overrides or {}
        self.users = {u["user_id"]: u for u in load(ds / "users.csv")}
        self.members = {}
        for m in load(ds / "group_members.csv"):
            self.members.setdefault(m["group_id"], set()).add(m["user_id"])
        self.sites = {s["site_id"]: s for s in load(ds / "sites.csv")}
        self.grants = load(ds / "site_grants.csv")
        self.links = load(ds / "sharing_links.csv")
        self.docs = load(ds / "documents.json")
        # remediation or break-it overlays
        for g in ov.get("remove_grants", []):
            self.grants = [x for x in self.grants if not (x["site_id"] == g["site_id"] and x["principal"] == g["principal"])]
        self.grants += ov.get("add_grants", [])
        for l in ov.get("revoke_links", []):
            self.links = [x for x in self.links if x["link_id"] != l]
        self.links += ov.get("add_links", [])
        for sid, changes in ov.get("site_settings", {}).items():
            self.sites[sid].update({k: str(v).lower() if isinstance(v, bool) else v for k, v in changes.items()})

    def internal_active(self):
        return {u for u, x in self.users.items() if x["status"] == "active" and x["department"] != "External"}

    def who_can_open(self, site_id):
        who = set()
        for g in self.grants:
            if g["site_id"] != site_id:
                continue
            p = g["principal"]
            if p == "EEEU":
                who |= self.internal_active()
            elif p.startswith("grp-"):
                who |= self.members.get(p, set())
            else:
                who.add(p)
        if any(l["site_id"] == site_id and l["scope"] == "organization" for l in self.links):
            who |= self.internal_active()
        return {u for u in who if self.users.get(u, {}).get("status") == "active"}

    def copilot_can_summarise(self, user_id, site_id):
        """Teaching model of the five layers. Not Microsoft's implementation."""
        s = self.sites[site_id]
        if user_id not in self.who_can_open(site_id):
            return False, "access"
        if s["restricted_content_discovery"] == "true":
            return False, "discovery"
        if s["label_encrypts"] == "true" and user_id not in self.members.get(s["extract_allowed_group"], set()):
            return False, "protection"
        if s["dlp_copilot_block"] == "true":
            return False, "processing"
        return True, "summarisable"


def exposure_report(wave, overrides=None, today="2026-10-08") -> tuple[Result, str]:
    t = Tenant(overrides=overrides)
    r = Result("6.1", f"Copilot exposure report for wave '{wave}'")
    wave_users = {u for u, x in t.users.items() if x["copilot_wave"] == wave and x["status"] == "active"}
    rows = []
    for sid, s in t.sites.items():
        openers = t.who_can_open(sid)
        outside_team = {u for u in openers if u in wave_users}
        summarisable = {u for u in outside_team if t.copilot_can_summarise(u, sid)[0]}
        intended = set()
        for g in t.grants:
            if g["site_id"] == sid and g["principal"].startswith("grp-") and g["principal"] not in ("grp-all-staff", "grp-project-falcon"):
                intended |= t.members.get(g["principal"], set())
        unintended = {u for u in summarisable if u not in intended}
        stale = (parse_date(today) - parse_date(s["last_activity"])).days > 365
        score = SENSITIVITY[s["sensitivity_label"]] * len(unintended)
        rows.append({"site": s["title"], "label": s["sensitivity_label"], "wave_users_can_open": len(outside_team),
                     "wave_users_can_summarise_unintended": len(unintended), "inactive_over_1y": stale,
                     "rcd": s["restricted_content_discovery"], "risk_score": score, "content": s["content_type"], "site_id": sid})
        if s["content_type"] in CROWN_JEWELS and unintended:
            r.find("crown-jewel-exposed", f"{len(unintended)} '{wave}' users outside the intended audience could have '{s['title']}' summarised.", site=sid)
        if stale and s["owner_user_id"] and t.users[s["owner_user_id"]]["status"] != "active":
            r.find("ownerless-stale-site", f"'{s['title']}' is inactive and its owner has left.", blocking=False, site=sid)
        if s["restricted_content_discovery"] == "true":
            r.find("containment-not-remediation", f"'{s['title']}' is hidden by Restricted Content Discovery; record an owner and exit date.", blocking=False, site=sid)
    rows.sort(key=lambda x: -x["risk_score"])
    r.data = {"wave": wave, "wave_users": len(wave_users), "sites": rows}
    md = f"# Copilot Exposure Report: wave '{wave}'\n\nWave size: {len(wave_users)} users. Synthetic tenant: Harbourline Group (fictional).\n\n" + \
         md_table(rows, ["site", "label", "wave_users_can_open", "wave_users_can_summarise_unintended", "inactive_over_1y", "rcd", "risk_score"]) + \
         "\n**Layer model:** access, discovery, protection, processing, lifecycle (Chapter 6, Table 6.1). This report is a teaching model of those layers, not a reproduction of Microsoft's reports.\n"
    return r, md


def retrieve(t: Tenant, user_id, query, open_site=None, config=None):
    """Teaching retriever: returns documents the user would see summarised, or link-only, per layer."""
    cfg = config or {"access_control": "prefilter"}
    words = set(query.lower().split())
    hits = []
    for d in t.docs:
        if open_site and d["site_id"] != open_site:
            continue
        if not words & set(d["text"].split()):
            continue
        if cfg["access_control"] == "prefilter" and user_id not in t.who_can_open(d["site_id"]):
            continue
        ok, layer = t.copilot_can_summarise(user_id, d["site_id"])
        if layer == "discovery" and open_site:      # RCD hides from org-wide search, not from someone who opens the site
            ok, layer = (True, "summarisable") if user_id in t.who_can_open(d["site_id"]) else (False, "access")
        if cfg["access_control"] == "none":
            ok, layer = True, "summarisable"
        mode = "summary" if ok else ("link_only" if layer in ("protection", "processing") else None)
        if mode:
            hits.append({"doc_id": d["doc_id"], "title": d["title"], "mode": mode, "layer": layer})
    return hits


# ------------------------------------------------------------------ Lab 6.3
def credential_audit(agents_json) -> tuple[Result, str]:
    r = Result("6.3", "Agent credential and identity audit")
    rows = []
    for a in load(agents_json):
        issues = []
        if a["environment"] == "prod" and a["auth_mode"] == "maker":
            issues.append("maker-provided credentials in production")
            r.find("maker-credentials", f"'{a['name']}' runs on its maker's credentials for {a['audience_users']} users.", agent=a["agent_id"])
        if a["auth_mode"] == "shared_service_account":
            issues.append("shared service account")
            r.find("shared-service-account", f"'{a['name']}' uses a shared service account; actions cannot be attributed.", agent=a["agent_id"])
        if a["environment"] == "prod" and not a.get("sponsor"):
            issues.append("no sponsor")
            r.find("no-sponsor", f"'{a['name']}' has no accountable sponsor.", agent=a["agent_id"])
        if any(t["action"] == "write" for t in a["tools"]) and a["auth_mode"] == "end_user" and a["audience_users"] > 1:
            issues.append("write tools under end-user identity: confirm approval stage")
        rows.append({"agent": a["name"], "environment": a["environment"], "auth_mode": a["auth_mode"],
                     "sponsor": a.get("sponsor") or "-", "issues": "; ".join(issues) or "none"})
    r.data = {"agents": rows}
    return r, "# Agent Credential Audit\n\n" + md_table(rows, ["agent", "environment", "auth_mode", "sponsor", "issues"])

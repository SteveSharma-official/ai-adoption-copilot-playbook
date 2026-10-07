"""Generate the synthetic Harbourline Group datasets used across the labs.

Harbourline Group is fictional. Every name, address, value and record below is invented.
Files are modelled on the *kind* of information Microsoft 365 admin reports and exports
provide (for example SharePoint data access governance reports and agent inventories),
but their columns are simplified teaching schemas, not Microsoft's export formats.

Run:  python shared/scripts/generate_datasets.py   (output is deterministic)
"""
from __future__ import annotations
import csv, json, random
from datetime import date, datetime, timedelta
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "datasets" / "harbourline"
OUT.mkdir(parents=True, exist_ok=True)
rnd = random.Random(20261008)
DOMAIN = "harbourline.example"


def wcsv(name, rows, cols):
    with (OUT / name).open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols, lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow({c: r.get(c, "") for c in cols})


def wjson(name, obj):
    (OUT / name).write_text(json.dumps(obj, indent=2), encoding="utf-8")


# ---------------------------------------------------------------- users and groups
FIRST = ["Ava", "Noah", "Mia", "Leo", "Isla", "Arlo", "Zara", "Eli", "Ruby", "Hugo", "Ivy", "Theo", "Maya", "Jack",
         "Lena", "Omar", "Priya", "Sam", "Tara", "Wei", "Yusuf", "Chloe", "Dev", "Erin", "Felix", "Grace", "Hamish",
         "Indira", "Jonah", "Kira"]
LAST = ["Nguyen", "Smith", "Patel", "Brown", "Wilson", "Taylor", "Chen", "Singh", "Martin", "Kelly", "Walker", "Ryan"]
DEPTS = [("Finance", 6), ("HR", 4), ("Legal", 3), ("Operations", 6), ("Customer Service", 6), ("Executive", 2), ("IT", 3)]
users = []
n = 0
for dept, count in DEPTS:
    for k in range(count):
        fn = FIRST[n % len(FIRST)]; ln = LAST[(n * 7) % len(LAST)]
        uid = f"u{n+1:03d}"
        users.append({"user_id": uid, "upn": f"{fn.lower()}.{ln.lower()}@{DOMAIN}", "display_name": f"{fn} {ln}",
                      "department": dept, "role": "Manager" if k == 0 else "Staff", "status": "active",
                      "leave_date": "", "copilot_wave": ""})
        n += 1
# pilot wave = Finance + Customer Service; wave 2 = Operations + HR + Legal
for u in users:
    u["copilot_wave"] = "pilot" if u["department"] in ("Finance", "Customer Service") else (
        "wave2" if u["department"] in ("Operations", "HR", "Legal") else "none")
# two leavers (used by agent lifecycle labs)
users[13]["status"] = "leaver"; users[13]["leave_date"] = "2026-08-29"   # Operations
users[2]["status"] = "leaver"; users[2]["leave_date"] = "2026-09-30"     # Finance
users.append({"user_id": "g001", "upn": f"guest.partner_gmail.com#EXT#@{DOMAIN}", "display_name": "External Partner (guest)",
              "department": "External", "role": "Guest", "status": "active", "leave_date": "", "copilot_wave": "none"})
wcsv("users.csv", users, ["user_id", "upn", "display_name", "department", "role", "status", "leave_date", "copilot_wave"])

groups = [{"group_id": "grp-all-staff", "name": "All Staff", "kind": "dynamic"}]
members = [{"group_id": "grp-all-staff", "user_id": u["user_id"]} for u in users if u["department"] != "External"]
for dept, _ in DEPTS:
    gid = "grp-" + dept.lower().replace(" ", "-")
    groups.append({"group_id": gid, "name": dept, "kind": "assigned"})
    members += [{"group_id": gid, "user_id": u["user_id"]} for u in users if u["department"] == dept]
groups.append({"group_id": "grp-project-falcon", "name": "Project Falcon (2019 restructure)", "kind": "assigned"})
members += [{"group_id": "grp-project-falcon", "user_id": u["user_id"]} for u in users if u["department"] in ("Operations", "Finance", "Customer Service")]
groups.append({"group_id": "grp-board-office", "name": "Board Office", "kind": "assigned"})
members += [{"group_id": "grp-board-office", "user_id": u["user_id"]} for u in users if u["department"] == "Executive"]
wcsv("groups.csv", groups, ["group_id", "name", "kind"])
wcsv("group_members.csv", members, ["group_id", "user_id"])

# ---------------------------------------------------------------- SharePoint sites (teaching schema)
sites = [
    # site_id, title, content, sensitivity weight label, label, encrypts, extract_groups, last_activity, owner
    ("s01", "HR Salary Reviews", "hr_salary", "Highly Confidential", False, "grp-hr", "2026-07-14", "u007"),   # labelled, but the label does not encrypt
    ("s02", "Board Papers", "board", "Highly Confidential", False, "", "2026-09-18", "u026"),
    ("s03", "Project Falcon Restructure 2019", "restructure", "Confidential", False, "", "2020-03-02", "u014"),
    ("s04", "Finance Month-End", "finance_ops", "Confidential", False, "", "2026-09-30", "u001"),
    ("s05", "Supplier Contracts", "contracts", "Confidential", False, "", "2026-09-12", "u011"),
    ("s06", "HR Policies (current)", "policy", "Internal", False, "", "2026-09-01", "u007"),
    ("s07", "HR Policy Archive", "policy_archive", "Internal", False, "", "2023-11-20", "u007"),
    ("s08", "Customer Complaints Register", "customer_pii", "Confidential", False, "", "2026-09-28", "u020"),
    ("s09", "Intranet News", "general", "General", False, "", "2026-10-02", "u028"),
    ("s10", "M&A Target Evaluation", "m_and_a", "Highly Confidential", True, "grp-executive", "2026-09-22", "u027"),
    ("s11", "Accounts Payable Knowledge Base", "ap_kb", "Internal", False, "", "2026-09-29", "u001"),
    ("s12", "Legal Matters", "legal", "Confidential", False, "", "2026-08-30", "u011"),
]
SITE_COLS = ["site_id", "title", "content_type", "sensitivity_label", "label_encrypts", "extract_allowed_group",
             "last_activity", "owner_user_id", "restricted_content_discovery", "dlp_copilot_block"]
site_rows = [{"site_id": s[0], "title": s[1], "content_type": s[2], "sensitivity_label": s[3],
              "label_encrypts": str(s[4]).lower(), "extract_allowed_group": s[5], "last_activity": s[6],
              "owner_user_id": s[7], "restricted_content_discovery": "false", "dlp_copilot_block": "false"} for s in sites]
wcsv("sites.csv", site_rows, SITE_COLS)

grants = [
    ("s01", "grp-hr", "edit"), ("s01", "EEEU", "read"),                 # salary file shared to everyone years ago
    ("s02", "grp-board-office", "edit"), ("s02", "grp-executive", "read"),
    ("s03", "grp-project-falcon", "edit"),                               # stale project group, still broad
    ("s04", "grp-finance", "edit"),
    ("s05", "grp-legal", "edit"), ("s05", "grp-finance", "read"),
    ("s06", "grp-all-staff", "read"), ("s06", "grp-hr", "edit"),
    ("s07", "grp-all-staff", "read"),
    ("s08", "grp-customer-service", "edit"), ("s08", "grp-legal", "read"),
    ("s09", "grp-all-staff", "read"),
    ("s10", "grp-executive", "edit"),
    ("s11", "grp-finance", "edit"), ("s11", "grp-customer-service", "read"),
    ("s12", "grp-legal", "edit"),
]
wcsv("site_grants.csv", [{"site_id": a, "principal": b, "role": c} for a, b, c in grants], ["site_id", "principal", "role"])

links = [
    {"link_id": "L001", "site_id": "s02", "item": "Board pack Sept 2026.pdf", "scope": "organization", "created": "2026-09-19", "created_by": "u026"},
    {"link_id": "L002", "site_id": "s08", "item": "Complaints export Q3.xlsx", "scope": "organization", "created": "2026-07-03", "created_by": "u020"},
    {"link_id": "L003", "site_id": "s05", "item": "Master supply agreement.docx", "scope": "specific", "created": "2026-06-11", "created_by": "u011"},
    {"link_id": "L004", "site_id": "s12", "item": "Litigation hold notice.docx", "scope": "specific", "created": "2026-08-01", "created_by": "u012"},
]
wcsv("sharing_links.csv", links, ["link_id", "site_id", "item", "scope", "created", "created_by"])

# ---------------------------------------------------------------- documents (for the teaching retriever)
docs = [
    {"doc_id": "d01", "site_id": "s01", "title": "FY26 salary review outcomes", "text": "salary review outcomes grades increases for every employee"},
    {"doc_id": "d02", "site_id": "s02", "title": "Board pack September 2026", "text": "board papers restructure options and executive remuneration"},
    {"doc_id": "d03", "site_id": "s03", "title": "Falcon redundancy list", "text": "restructure redundancy list names roles 2019"},
    {"doc_id": "d04", "site_id": "s06", "title": "Leave policy v4", "text": "leave policy annual leave personal leave parental leave entitlements"},
    {"doc_id": "d05", "site_id": "s07", "title": "Leave policy v2 (superseded)", "text": "leave policy annual leave parental leave entitlements superseded"},
    {"doc_id": "d06", "site_id": "s10", "title": "Target valuation model", "text": "acquisition target valuation synergies m&a"},
    {"doc_id": "d07", "site_id": "s11", "title": "Supplier payment run schedule", "text": "supplier payment run schedule invoice terms accounts payable"},
    {"doc_id": "d08", "site_id": "s08", "title": "Complaints export Q3", "text": "customer complaints names phone numbers outcomes"},
]
wjson("documents.json", docs)

# ---------------------------------------------------------------- agent inventory (teaching schema)
agents = [
    {"agent_id": "ag-ap-query", "name": "AP Supplier Query Assistant", "platform": "Copilot Studio", "environment": "prod",
     "created_by": "u001", "owner": "u001", "sponsor": "u001", "auth_mode": "end_user", "audience_users": 9,
     "published": True, "last_run": "2026-10-06", "registered": True, "rung": 2,
     "tools": [{"name": "kb.search", "action": "read", "system": "SharePoint"}, {"name": "erp.invoice_status", "action": "read", "system": "ERP"}]},
    {"agent_id": "ag-expense-check", "name": "Expense Policy Checker", "platform": "Copilot Studio", "environment": "prod",
     "created_by": "u003", "owner": "u003", "sponsor": "", "auth_mode": "maker", "audience_users": 38,
     "published": True, "last_run": "2026-10-05", "registered": False, "rung": 2,
     "tools": [{"name": "erp.expense_update", "action": "write", "system": "ERP"}]},
    {"agent_id": "ag-ops-roster", "name": "Ops Roster Helper", "platform": "Copilot Studio", "environment": "prod",
     "created_by": "u014", "owner": "u014", "sponsor": "u015", "auth_mode": "shared_service_account", "audience_users": 6,
     "published": True, "last_run": "2026-09-30", "registered": True, "rung": 2,
     "tools": [{"name": "roster.read", "action": "read", "system": "Rostering"}, {"name": "roster.update", "action": "write", "system": "Rostering"}]},
    {"agent_id": "ag-hr-policy", "name": "HR Policy Answers", "platform": "Copilot Studio", "environment": "prod",
     "created_by": "u008", "owner": "u007", "sponsor": "u007", "auth_mode": "end_user", "audience_users": 40,
     "published": True, "last_run": "2026-10-06", "registered": True, "rung": 3,
     "tools": [{"name": "kb.search", "action": "read", "system": "SharePoint"}]},
    {"agent_id": "ag-cs-refund", "name": "Refund Drafting Agent", "platform": "Copilot Studio", "environment": "prod",
     "created_by": "u021", "owner": "u020", "sponsor": "u020", "auth_mode": "agent_identity", "audience_users": 6,
     "published": True, "last_run": "2026-10-06", "registered": True, "rung": 3,
     "tools": [{"name": "crm.case_read", "action": "read", "system": "CRM"}, {"name": "pos.refund_request", "action": "write", "system": "POS"}]},
    {"agent_id": "ag-personal-notes", "name": "My meeting notes helper", "platform": "Agent Builder", "environment": "personal",
     "created_by": "u022", "owner": "u022", "sponsor": "", "auth_mode": "end_user", "audience_users": 1,
     "published": False, "last_run": "2026-10-03", "registered": False, "rung": 1,
     "tools": []},
    {"agent_id": "ag-foundry-triage", "name": "Ticket Triage (Foundry)", "platform": "Microsoft Foundry", "environment": "prod",
     "created_by": "u029", "owner": "u029", "sponsor": "u028", "auth_mode": "agent_identity", "audience_users": 0,
     "published": True, "last_run": "2026-10-06", "registered": True, "rung": 4,
     "tools": [{"name": "itsm.ticket_tag", "action": "write", "system": "ITSM"}]},
]
wjson("agents.json", agents)
wcsv("agent_register.csv", [{"agent_id": a["agent_id"], "business_owner": a["owner"], "sponsor": a["sponsor"],
                             "authority_level": {1: "L1", 2: "L2", 3: "L3", 4: "L4"}[a["rung"]] if a["registered"] else "",
                             "last_review": "2026-07-01" if a["registered"] else "", "status": "Active"}
                            for a in agents if a["registered"]],
     ["agent_id", "business_owner", "sponsor", "authority_level", "last_review", "status"])

# ---------------------------------------------------------------- shadow AI discovery (proxy log summary)
ai_tools = [
    {"tool": "Microsoft 365 Copilot", "domain": "m365.cloud.microsoft", "status": "sanctioned", "owner": "IT"},
    {"tool": "Copilot Studio", "domain": "copilotstudio.microsoft.com", "status": "sanctioned", "owner": "IT"},
    {"tool": "Microsoft Foundry", "domain": "ai.azure.com", "status": "sanctioned", "owner": "Data Platform"},
]
wcsv("ai_tools_sanctioned.csv", ai_tools, ["tool", "domain", "status", "owner"])
proxy = []
cats = [("m365.cloud.microsoft", "ai_assistant"), ("copilotstudio.microsoft.com", "ai_builder"), ("ai.azure.com", "ai_platform"),
        ("chat.example-ai.test", "ai_assistant"), ("code.example-assist.test", "ai_coding"), ("summarise.example-tool.test", "ai_assistant"),
        ("news.example.test", "news")]
for d in ["Finance", "Customer Service", "Operations", "IT", "Legal", "HR"]:
    for dom, cat in cats:
        hits = rnd.randint(0, 40)
        if dom == "code.example-assist.test" and d != "IT": hits = 0
        if dom == "summarise.example-tool.test" and d not in ("Legal", "Operations"): hits = 0
        if hits:
            proxy.append({"department": d, "domain": dom, "category": cat, "requests_30d": hits * 10,
                          "upload_bytes_30d": hits * rnd.randint(5, 900) * 1000})
wcsv("proxy_ai_summary_30d.csv", proxy, ["department", "domain", "category", "requests_30d", "upload_bytes_30d"])

# ---------------------------------------------------------------- AP process event log (synthetic)
STEPS = ["received", "triaged", "data_lookup_done", "draft_done", "approved", "closed"]
def case_rows(prefix, start, n_cases, durations):
    rows = []
    t0 = datetime.fromisoformat(start)
    for i in range(n_cases):
        t = t0 + timedelta(hours=i * 7)
        rows.append({"case_id": f"{prefix}{i+1:03d}", "step": "received", "timestamp": t.isoformat(timespec="minutes")})
        for step, (lo, hi) in zip(STEPS[1:], durations):
            t = t + timedelta(minutes=rnd.randint(lo, hi))
            rows.append({"case_id": f"{prefix}{i+1:03d}", "step": step, "timestamp": t.isoformat(timespec="minutes")})
    return rows
# minutes per transition: triage, data lookup (bottleneck), draft, approval, close
base = case_rows("B", "2026-07-01T09:00", 40, [(10, 30), (240, 420), (20, 45), (40, 120), (5, 15)])
pilot = case_rows("P", "2026-09-01T09:00", 40, [(10, 30), (60, 150), (10, 25), (40, 120), (5, 15)])
wcsv("ap_process_events.csv", [dict(r, period="baseline") for r in base] + [dict(r, period="pilot") for r in pilot],
     ["case_id", "period", "step", "timestamp"])

print("datasets written to", OUT)

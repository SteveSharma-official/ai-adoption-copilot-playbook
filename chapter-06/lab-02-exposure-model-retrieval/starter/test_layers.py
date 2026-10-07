"""Behaviour of the five-layer teaching retriever. Run: python -m pytest -q"""
import sys, yaml
from pathlib import Path
HERE = Path(__file__).resolve().parent
for p in [HERE, *HERE.parents]:
    if (p / "shared" / "playbook").is_dir():
        sys.path.insert(0, str(p / "shared")); break
from playbook.platform import Tenant, retrieve

CFG = yaml.safe_load((HERE / "retrieval.yaml").read_text())

def ids(hits, mode=None):
    return {h["doc_id"] for h in hits if mode is None or h["mode"] == mode}

def test_access_layer_blocks_people_without_permission():
    t = Tenant()
    # u020 (Customer Service) cannot open HR salary site once EEEU is removed
    t2 = Tenant(overrides={"remove_grants": [{"site_id": "s01", "principal": "EEEU"}]})
    assert "d01" not in ids(retrieve(t2, "u020", "salary review", config=CFG))

def test_overshared_content_is_summarisable_before_remediation():
    t = Tenant()
    assert "d01" in ids(retrieve(t, "u020", "salary review", config=CFG), "summary") or \
           "d01" in ids(retrieve(t, "u020", "salary review", config=CFG), "link_only")

def test_discovery_layer_hides_from_search_not_from_direct_open():
    t = Tenant(overrides={"site_settings": {"s03": {"restricted_content_discovery": True}}})
    assert "d03" not in ids(retrieve(t, "u015", "restructure redundancy", config=CFG))
    assert "d03" in ids(retrieve(t, "u015", "restructure redundancy", open_site="s03", config=CFG), "summary")

def test_protection_layer_link_only_without_extract():
    t = Tenant()
    # M&A site is encrypted; EXTRACT only for Executive. IT user u028 granted read for the test
    t2 = Tenant(overrides={"add_grants": [{"site_id": "s10", "principal": "u028", "role": "read"}]})
    assert ids(retrieve(t2, "u028", "acquisition valuation", config=CFG), "link_only") == {"d06"}
    assert ids(retrieve(t2, "u026", "acquisition valuation", config=CFG), "summary") == {"d06"}

def test_processing_layer_dlp_blocks_summary():
    t = Tenant(overrides={"site_settings": {"s08": {"dlp_copilot_block": True}}})
    assert ids(retrieve(t, "u020", "complaints", config=CFG), "summary") == set()

def test_no_layer_ever_grants_access():
    t = Tenant()
    for u in t.users:
        for d in retrieve(t, u, "salary board restructure acquisition complaints leave supplier", config=CFG):
            site = next(x["site_id"] for x in t.docs if x["doc_id"] == d["doc_id"])
            assert u in t.who_can_open(site), f"{u} received {d['doc_id']} without access"

"""Offline integrity checks for a completed run; no provider calls."""
import argparse
import hashlib
import json
import math
from collections import Counter
from pathlib import Path

import run_pilot as pilot


def main():
    parser=argparse.ArgumentParser();parser.add_argument("run",type=Path)
    run=parser.parse_args().run
    manifest=json.loads((run/"manifest.json").read_text())
    status=json.loads((run/"run_status.json").read_text())
    raw=pilot.load_lines(run/"raw.jsonl")
    samples=pilot.load_lines(run/"samples.jsonl")
    assert status["state"]=="complete"
    assert len(samples)==status["planned_jobs"]==len({s["id"] for s in samples})
    requests={e["id"]:e for e in raw if e["event"]=="request"}
    responses=[e for e in raw if e["event"]=="response"]
    assert len(requests)==len(responses)==len({e["id"] for e in responses})
    assert len({e["response"]["id"] for e in responses})==len(responses)
    for e in responses:
        req=requests[e["id"]]
        assert req["job"]==e["job"]
        assert req["payload"]["temperature"]==.7
        assert req["payload"]["max_tokens"]==300
        assert req["payload"]["provider"]["allow_fallbacks"] is False
        assert req["payload"]["response_format"]["type"]=="json_schema"
        assert req["response_cache"] is False
        digest=hashlib.sha256(json.dumps(req["payload"]["messages"],ensure_ascii=False).encode()).hexdigest()
        assert digest==manifest["prompt_hashes"][req["job"]]
        assert isinstance(e["response"]["usage"]["cost"],(float,int))
    actual=sum(e["response"]["usage"]["cost"] for e in responses)
    assert math.isclose(actual,status["run_cost"],abs_tol=1e-10)
    ledger=pilot.load_lines(pilot.ROOT/"runs/budget_ledger.jsonl")
    total,held,pending=pilot.Budget.balance(ledger)
    assert held==0 and not pending and total<=5
    audit_total=sum(e["response"]["usage"]["cost"] for p in (pilot.ROOT/"runs").glob("*/raw.jsonl")
                    for e in pilot.load_lines(p) if e.get("event")=="response" and "usage" in e.get("response",{}))
    assert math.isclose(total,audit_total,abs_tol=1e-10)
    first=pilot.load_lines(run/"first_attempt_choice_valid/samples.jsonl")
    assert len(first)==len(samples)
    counts=Counter((s["item"],s["model"],s["condition"],s["perturbation"]) for s in first if s["kind"]=="decision")
    assert set(counts.values())=={manifest["n"]}
    for item in manifest["items"]:
        text=(pilot.ROOT/"texts"/f"{item['slug']}.up_to_stop.txt").read_text()
        assert hashlib.sha256(text.encode()).hexdigest()==item["metadata"]["cut_sha256"]
        assert text.endswith(item["metadata"]["exact_anchor_text"])
        assert len(text)==item["metadata"]["stop_char_exclusive"]
    bank=[json.loads(line) for line in (pilot.ROOT/"items/item_bank.jsonl").read_text().splitlines()]
    assert len(bank)==60 and len({i["id"] for i in bank})==60
    assert len({i["author"] for i in manifest["items"]})==8
    result=dict(passed=True,checks=["complete unique jobs","request-response bijection","unique provider response IDs",
        "frozen prompt hashes","fixed generation settings","actual spend reconciles to shared ledger",
        "no unresolved charges","balanced first-attempt cells","source hashes and exclusive cuts","60 unique bank records","8 unique authors"],
        requests=len(requests),decision_cells=len(counts),samples_per_cell=manifest["n"],total_api_spend=total)
    pilot.save(run/"integrity_audit.json",result)
    print(json.dumps(result,indent=2))


if __name__=="__main__":main()

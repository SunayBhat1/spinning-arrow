import json
import tempfile
import unittest
from pathlib import Path

import run_pilot as runner
from prepare_bank import anchor_cut, extract, normalize, strip_wrapper


class PilotTests(unittest.TestCase):
    def test_budget_reserves_retries_and_other_processes(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/"ledger.jsonl"
            first=runner.Budget(path,cap=1)
            second=runner.Budget(path,cap=1)
            first.reserve("one",.7,"test")
            with self.assertRaises(RuntimeError):second.reserve("two",.4,"test")
            first.settle("one",.6)
            with self.assertRaises(RuntimeError):second.reserve("retry",.7,"test")
            second.reserve("small",.3,"test")
            self.assertAlmostEqual(first.transact()["actual"],.6)
            self.assertAlmostEqual(first.transact()["reserved"],.3)

    def test_unknown_usage_keeps_reservation(self):
        with tempfile.TemporaryDirectory() as d:
            budget=runner.Budget(Path(d)/"l",cap=1)
            budget.reserve("x",.5,"test")
            for value in [None,float("nan"),True,-1]:
                with self.assertRaises(RuntimeError):budget.settle("x",value)
            self.assertEqual(budget.transact()["reserved"],.5)

    def test_duplicate_settlement_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            b=runner.Budget(Path(d)/"l")
            b.reserve("x",.1,"test");b.settle("x",.01)
            with self.assertRaises(ValueError):b.settle("x",.01)

    def test_modal_ties_not_alphabetical_winners(self):
        self.assertEqual(runner.modal(["A","B"]),(["A","B"],.5))

    def test_strict_json(self):
        good=json.dumps(dict(choice="1",confidence=.4,reason="One short justification."))
        self.assertEqual(runner.validate(good,{"1":"A"})["choice"],"1")
        for bad in [dict(choice="X",confidence=.4,reason="yes"),dict(choice="1",confidence=True,reason="yes"),
                    dict(choice="1",confidence=.4,reason="word "*61),dict(choice="1",confidence=.4,reason="yes",extra=1)]:
            with self.assertRaises(ValueError):runner.validate(json.dumps(bad),{"1":"A"})

    def test_honest_unknown_recall_can_have_empty_description(self):
        self.assertEqual(runner.validate('{"knows":false,"description":""}'),{"knows":False,"description":""})
        with self.assertRaises(ValueError):runner.validate('{"knows":true,"description":""}')

    def test_anchor_wrap_unique_and_exclusive(self):
        source="Start. Last\n sentence. SPOILER."
        cut,start,end,exact=anchor_cut(source,"Last sentence.")
        self.assertEqual(cut,"Start. Last\n sentence.")
        self.assertEqual(source[end:]," SPOILER.")
        with self.assertRaises(ValueError):anchor_cut("Yes. Yes.","Yes.")

    def test_bank_count_rights_and_flags(self):
        bank,_=normalize()
        self.assertEqual(len(bank),60)
        byid={i["id"]:i for i in bank}
        self.assertIn("excluded",byid["N01"]["flags"])
        self.assertIn("excluded",byid["N03"]["flags"])
        self.assertIsNone(byid["A23"]["author_path"])
        self.assertIn("high_contamination_risk",byid["B12"]["flags"])

    def test_prompts_and_semantic_option_mapping(self):
        items=json.loads((runner.ROOT/"items.json").read_text())["items"]
        self.assertEqual(len(items),8)
        self.assertEqual(len({i["author"] for i in items}),8)
        for item in items:
            ctx=runner.contexts(item)
            self.assertEqual("R2" in ctx,item["word_count"]<8000)
            self.assertTrue(item["forced_question"].startswith("You are"))
            msg,map_=runner.messages(item,ctx["R0"],"p1",104729)
            self.assertEqual(set(map_.values()),set(item["options"]))
            self.assertNotEqual(list(map_.values()),list(item["options"]))
            _,num=runner.messages(item,ctx["R0"],"p3",104729)
            self.assertEqual(list(num),[str(i+1) for i in range(len(item["options"]))])


if __name__=="__main__":unittest.main()

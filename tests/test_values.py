"""Every value against the copy it was read from, and the saws against furniture-design's rules.

The copies are copyrighted and live in the private repo xag/furniture, checked out beside this one
(or at $FURNITURE_REPO), under sources/saws/, each beside its text (the PDF's or the page's). Without
them these tests fail, saying where they looked, and never skip.
"""

import hashlib
import os
import re
from pathlib import Path

from quern import Quern, run_rules
from quern.tree import Node

from furniture_design.knowledge import knowledge as general, merge
from furniture_design.package import PACKAGE
from saws import SAWS, documents, knowledge

ROOT = Path(__file__).resolve().parents[1]
CAPTURES = Path(os.environ.get("FURNITURE_REPO", ROOT.parent / "furniture")) / "sources" / "saws"


def _here(path: Path) -> Path:
    assert path.exists(), (f"the private copy {path} is missing: clone xag/furniture beside this repo or "
                           "set FURNITURE_REPO")
    return path


def _cells(printed: str) -> list[float]:
    """The numbers a printed row holds, in order: '1,8/1,3' is 1.8 and 1.3, '2 608 838 410 216' is 2, 608,
    838, 410 and 216."""
    return [float(n.replace(",", ".")) for n in re.findall(r"\d+(?:[.,]\d+)?", printed)]


def test_every_value_is_printed_in_the_document_fetched():
    for doc in documents().values():
        copy = _here(CAPTURES / doc["file"])
        assert hashlib.sha256(copy.read_bytes()).hexdigest() == doc["sha256"], doc["id"]
        text = re.sub(r"\s+", " ", _here(copy.with_suffix(".txt")).read_text(encoding="utf-8"))
        for clause in doc["clauses"]:
            for name, v in clause["params"].items():
                assert v["printed"] in text, (doc["id"], clause["id"], name, v["printed"])
                cells = _cells(v["printed"].replace("ｍｍ", "mm"))
                if "column" in v:
                    assert abs(cells[v["column"]] - v["value"]) < 1e-9, (doc["id"], clause["id"], name, cells)
                else:
                    assert any(abs(n - v["value"]) < 1e-9 for n in cells), (doc["id"], clause["id"], name)


def test_every_saw_reads_its_values_from_its_makers_clauses():
    by_id = {n.id: n for n in knowledge()[1].children}
    assert set(by_id) == {s[0] for s in SAWS}
    assert by_id["festool-ts-55"].params["kerf"].value == 1.8
    assert by_id["bosch-gts-635-216"].params["kerf"].value == 2.6
    assert by_id["gyokucho-orizuru-dozuki-240"].params["max_cut_depth"].value == 35
    for saw in by_id.values():
        assert saw.links["per"], saw.id
        for q in saw.params.values():
            assert q.grounded and q.derived_from


def _tree(sawn_with: str, thickness: float = 18, sheets: int = 1) -> Quern:
    tree = Quern(vocabulary=PACKAGE.vocabulary, rules=PACKAGE.rules, solvers=PACKAGE.solvers)
    part = Node(id="side", kind="part", links={"uses": ["materials/birch-yellow"], "sawn_with": [sawn_with]},
                params={"thickness": _mm(thickness)},
                payload={"shape": {"op": "box", "size": [thickness, 300, 450]}, "sheets": sheets})
    tree.root.children = merge(general(), knowledge()) + [
        Node(id="pieces", kind="", children=[Node(id="stool", kind="piece", children=[part])])]
    return tree


def _mm(value: float):
    from quern.provenance import Quantity
    return Quantity(value=value, unit="mm", provenance="design-target")


def _verdict(tree: Quern, rule: str) -> str:
    return next(r.verdict for r in run_rules(tree, "pieces/stool") if r.rule == rule and r.node == "pieces/stool/side")


def test_a_saw_whose_maker_prints_its_cut_passes_and_one_whose_maker_does_not_is_refused():
    cut = "a-part-is-sawn-with-a-saw-that-states-its-cut"
    assert _verdict(_tree("tools/festool-ts-55"), cut) == "holds"
    assert _verdict(_tree("tools/metabo-kgs-216-m"), cut) == "holds"  # the widest blade it takes
    assert _verdict(_tree("tools/bosch-gks-190"), cut) == "broken"
    assert _verdict(_tree("tools/striebig-compact"), cut) == "broken"


def test_a_board_thicker_than_the_saw_cuts_is_refused_a_glued_one_is_judged_by_its_sheets_and_no_depth_judges_nothing():
    deep = "a-part-is-no-thicker-than-its-saw-cuts"
    assert _verdict(_tree("tools/gyokucho-orizuru-dozuki-240", 18), deep) == "holds"
    assert _verdict(_tree("tools/gyokucho-orizuru-dozuki-240", 40), deep) == "broken"
    assert _verdict(_tree("tools/gyokucho-orizuru-dozuki-240", 36, sheets=2), deep) == "holds"
    assert _verdict(_tree("tools/z-saw-iii-265", 80), deep) == "absent"  # its maker states no depth


def test_the_saws_and_their_sources_break_none_of_furniture_designs_rules():
    tree = Quern(vocabulary=PACKAGE.vocabulary, rules=PACKAGE.rules, solvers=PACKAGE.solvers)
    tree.root.children = merge(general(), knowledge())
    ours = {f"tools/{s[0]}" for s in SAWS} | {f"sources/{d}" for d in documents()}
    broken = [r for r in run_rules(tree, "") if not r.ok and any(r.node == p or r.node.startswith(p + "/") for p in ours)]
    assert not broken, broken

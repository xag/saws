"""The usual blades: every row of every catalogue read again from its copy, and what the saws take from them.

The copies live in the private repo xag/furniture under sources/saws/ (see test_values.py); without them these
tests fail and say where they looked.
"""

import hashlib
import os
from collections import Counter
from pathlib import Path

from quern import Quern, run_rules

from furniture_design.knowledge import knowledge as general, merge
from furniture_design.package import PACKAGE
from readings import READINGS
from saws import BLADES, SAWS, blades, catalogues, knowledge, usual
from test_values import _tree, _verdict

ROOT = Path(__file__).resolve().parents[1]
CAPTURES = Path(os.environ.get("FURNITURE_REPO", ROOT.parent / "furniture")) / "sources" / "saws"


def _copy(name: str) -> Path:
    path = CAPTURES / name
    assert path.exists(), f"the private copy {path} is missing: clone xag/furniture beside this repo or set FURNITURE_REPO"
    return path


def test_every_row_listed_is_read_from_the_catalogue_fetched_and_none_is_left_out():
    for c in catalogues().values():
        if c["file"]:
            assert hashlib.sha256(_copy(c["file"]).read_bytes()).hexdigest() == c["sha256"], c["id"]
        text = _copy(c["text"])
        assert hashlib.sha256(text.read_bytes()).hexdigest() == c["text_sha256"], c["id"]
        read = READINGS[c["reading"]](text.read_text(encoding="utf-8", errors="replace"), c["pages"])
        assert Counter(map(tuple, read)) == Counter(map(tuple, c["rows"])), c["id"]


def test_rows_read_by_hand_are_listed():
    # (page, D, kerf, body) as each catalogue prints them, read off the page
    rows = {"freud-portable-finder": [4, 150, 2.4, 1.6], "leitz-lexicon-7-sawing": [81, 160, 1.6, 1.1], "leitz-lexicon-7-sawing-chart": [80, 160, 1.8, 1.2],
            "cmt-catalogue-2017": [37, 120, 1.8, 1.2]}
    for c, row in rows.items():
        assert row in catalogues()[c.removesuffix("-chart")]["rows"], c


def test_a_diameter_is_usual_when_two_catalogues_list_it_and_its_cut_is_their_widest():
    u = usual()
    assert all(len(cs) >= 2 for cs in u.values())
    assert 168 not in u  # Freud's alone
    assert blades("leitz-lexicon-7-sawing")[190] == {"narrowest": 1.8, "widest": 2.8, "blades": 7, "pages": {80, 81}}
    tools = {n.id: n for n in knowledge()[1].children}
    assert tools["usual-blade-190"].params["max_kerf"].value == 2.8
    assert tools["usual-blade-190"].payload["usual"]["narrowest"] == 1.5
    assert {f"usual-blade-{d}" for d in u} <= set(tools)


def test_a_saw_whose_maker_prints_no_cut_keeps_none_and_names_its_blade_and_the_usual_blade_of_it():
    tools = {n.id: n for n in knowledge()[1].children}
    gks = tools["bosch-gks-190"]
    assert "kerf" not in gks.params and "max_kerf" not in gks.params
    assert gks.payload["blade"] == {"diameter_mm": 190, "usual": "tools/usual-blade-190",
                                    "per": "sources/bosch-gks-190-manual/technical-data/blade_diameter"}
    assert tools["dewalt-dwe560"].payload["blade"]["usual"] == "tools/usual-blade-184"
    for saw in BLADES:
        assert tools[saw].payload["blade"]["usual"] in {f"tools/{n}" for n in tools}, saw


def test_a_part_sawn_with_a_usual_blade_passes_and_one_with_a_saw_that_prints_no_cut_is_still_refused():
    cut = "a-part-is-sawn-with-a-saw-that-states-its-cut"
    assert _verdict(_tree("tools/usual-blade-190"), cut) == "holds"
    assert _verdict(_tree("tools/bosch-gks-190"), cut) == "broken"
    assert _verdict(_tree("tools/bosch-gst-160-ce"), cut) == "broken"  # a jigsaw: no blade catalogue read
    assert _verdict(_tree("tools/striebig-compact"), cut) == "broken"  # a panel saw: idem


def test_the_catalogues_and_usual_saws_break_none_of_furniture_designs_rules():
    tree = Quern(vocabulary=PACKAGE.vocabulary, rules=PACKAGE.rules, solvers=PACKAGE.solvers)
    tree.root.children = merge(general(), knowledge())
    ours = {f"sources/{c}" for c in catalogues()} | {f"tools/usual-blade-{d}" for d in usual()} | \
           {f"tools/{s[0]}" for s in SAWS}
    broken = [r for r in run_rules(tree, "") if not r.ok and any(r.node == p or r.node.startswith(p + "/") for p in ours)]
    assert not broken, broken

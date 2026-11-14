"""The decisions saws is bound by, as a ledger. Read it with `uv run quern brief .`, never whole.

Vocabulary: ledger@0.8.0 and grounding@1.2.0, pinned in quern.lock.
"""

from __future__ import annotations

import os
from pathlib import Path

import quern.grounding  # noqa: F401
from quern import Node, Quern
from quern.library import consume

OWNER = "Source les différents types de scies et les solvers et règles associés"


def _alt(id_: str, name: str, why: str) -> Node:
    return Node(id=id_, kind="alternative", name=name, payload={"why": why})


def entries() -> list[Node]:
    return [
        Node(
            id="the-saws-are-one-package", kind="decision",
            name="Every saw maker's figures are one package, saws, which requires furniture-design and adds each saw "
                 "as a tool under tools/ with its maker's documents as sources; it names no shop and no piece",
            payload={"decided_on": "2026-11-14", "the_owner": OWNER,
                     "why": "furniture-design names no maker (its ledger: makers-products-are-in-packages-outside-"
                            "furniture-design), and the saws of every kind share what a design reads of them: the "
                            "cut of their blade and the thickest board they cut. One maker's saws are a handful of "
                            "figures, too few for a package each."},
            children=[
                _alt("a-package-per-maker", "One unofficial package per saw maker, as for Lamello",
                     "Eleven packages of one to three saws each, every one read the same way."),
                _alt("in-wood-panels", "Put the saws in wood-panels",
                     "A board and the saw that cuts it are different products from different makers."),
            ],
        ),
        Node(
            id="a-saw-states-only-what-its-maker-prints", kind="decision",
            name="A saw carries only what its maker prints, each value checked against the copy fetched: the cut of "
                 "the blade it comes with (kerf), else the widest blade it takes (max_kerf, a tooth width or set), "
                 "its blade's body (blade_thickness) and the thickest board it cuts through at 90° (max_cut_depth). "
                 "No portable circular saw's, jigsaw's or panel saw's maker read here prints a blade's cut, so those "
                 "saws carry none, and furniture-design's rule refuses a design that cuts with one until it states a "
                 "measured cut on a saw of its own",
            links={"rests_on": ["the-saws-are-one-package"]},
            payload={"decided_on": "2026-11-14", "the_owner": OWNER,
                     "why": "The cut decides how close parts sit on a board, and a blade's body is narrower than "
                            "the cut its set teeth make: Gyokucho prints both (0.5 mm and 0.83 mm), Bahco the body "
                            "alone (1.03 mm), so Bahco's cut is not known."},
            children=[
                _alt("a-typical-kerf-per-kind", "Give a circular saw or a panel saw a typical kerf (2.4 mm, 3.2 mm)",
                     "A figure no maker of that saw prints, which the sheet would then print as the saw's."),
                _alt("body-as-kerf", "Take a blade's body thickness as its kerf",
                     "The teeth are set wider than the body: Gyokucho's 0.5 mm blade cuts 0.83 mm."),
            ],
        ),
        Node(
            id="a-usual-blade-is-a-tool-of-its-own", kind="decision",
            name="The usual blades of a diameter are a tool of their own, usual-blade-<D>: its max_kerf is the widest "
                 "cut among the wood blades for portable, mitre and table saws that at least two blade catalogues list "
                 "at that diameter (Freud, Leitz, CMT), every row read again from the copy by a test. A maker's saw "
                 "keeps only what its maker prints, and names in its payload's blade the diameter its maker prints and "
                 "the usual blade of it. A design whose saw prints no cut is sawn with that usual blade, so the sheet "
                 "names the blade it counted and never prints the figure as the saw's",
            links={"rests_on": ["a-saw-states-only-what-its-maker-prints"]},
            payload={"decided_on": "2026-11-14",
                     "the_owner": "Tu n'as que des marques ou tu as aussi des standards pour les scies? Il faut aussi "
                                  "des standards au sens de mesures habituelles.",
                     "why": "The catalogues list blades by diameter, each fitting several kinds of machine (CMT: "
                            "'table and mitre saws, portable machines'), so the diameter is what a usual cut is "
                            "known by, and a maker prints its saw's. The widest cut leaves room for any of those "
                            "blades: a narrower one counted makes the parts end shorter than drawn. One catalogue's "
                            "blade is a maker's, not usual. The standards on blade dimensions found (ISO 2935, withdrawn "
                            "in 2025; DIN 8083, withdrawn; DIN 8809, tool-steel blades) are sold, and the free pages "
                            "read of them (iso.org, DIN Media, din.de) show no value."},
            children=[
                _alt("the-usual-cut-on-the-makers-saw", "Give a maker's saw the widest usual cut of its blade's diameter "
                     "as its max_kerf", "The sheet would print the figure as that saw's, which "
                     "a-saw-states-only-what-its-maker-prints turned down (a-typical-kerf-per-kind)."),
                _alt("a-usual-cut-per-kind-of-saw", "One usual cut per kind of saw (circular, plunge, mitre, table)",
                     "The catalogues do not sort blades that way: one blade fits several kinds, and the cut follows the "
                     "diameter."),
                _alt("the-narrowest-or-middle-cut", "Count the narrowest or the middle of the usual cuts",
                     "A cut wider than counted eats into the parts; the widest only spends a little board."),
            ],
        ),
    ]


def build() -> Quern:
    root = Path(__file__).resolve().parents[1]
    lib, refs = consume(root, os.environ.get("QUERN_REGISTRY", root.parent / "quern-registry"))
    quern = Quern(packages=list(refs))
    quern = lib.effective(quern)
    quern.root.children = entries()
    return quern

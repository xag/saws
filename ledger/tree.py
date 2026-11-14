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
    ]


def build() -> Quern:
    root = Path(__file__).resolve().parents[1]
    lib, refs = consume(root, os.environ.get("QUERN_REGISTRY", root.parent / "quern-registry"))
    quern = Quern(packages=list(refs))
    quern = lib.effective(quern)
    quern.root.children = entries()
    return quern

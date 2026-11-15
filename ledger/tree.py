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
        Node(
            id="a-beam-saws-usual-blade-is-one-tool-whatever-its-diameter", kind="decision",
            name="The main blade of a beam saw (a panel sizing saw with a pressure beam, the shops' scie à plat) is "
                 "one tool, usual-panel-sizing-blade, whatever its diameter: its max_kerf is the widest cut among the "
                 "panel sizing main blades at every diameter that both Leitz (Lexicon 7, 1.4.1 to 1.4.3) and CMT "
                 "(2017, p. 25) list, 250 to 550 mm, 5.2 mm; its payload's usual gives the narrowest (3.2) and the "
                 "commonest (4.4). A shop's cutting service that prints no cut names it as the blade a design is "
                 "sawn with",
            links={"rests_on": ["a-usual-blade-is-a-tool-of-its-own"]},
            payload={"decided_on": "2026-11-15",
                     "the_owner": "Je suppose que c'est 3.5 mm c'est un standard non? / As tu intégré ces infos "
                                  "riches dont tu me parles là",
                     "why": "A shop says its saw is a scie à plat and names no blade, so the diameter a usual cut is "
                            "known by for a circular saw is not to be had. The widest cut of the blades two "
                            "catalogues list leaves room for any of them, as for the circular saws' usual blades."},
            children=[
                _alt("a-panel-blade-per-diameter", "One usual panel sizing blade per diameter, as for circular saws",
                     "No shop read prints its beam saw's diameter, so no design could name one."),
                _alt("the-commonest-cut", "Count the commonest cut, 4.4 mm",
                     "A 4.8 or 5.2 mm blade, which both catalogues list, would leave the parts shorter than drawn."),
                _alt("three-and-a-half", "Count 3.5 mm",
                     "3.5 mm is the body of the 4.8 and 5.2 mm blades, and the cut of one CMT blade among 36."),
            ],
        ),
        Node(
            id="a-saws-model-is-data-on-its-node-sized-from-its-makers-print-and-image", kind="decision",
            name="A saw's 3D model is data on its tool node (payload model, furniture-design's solids format), "
                 "as lamello-unofficial puts the Zeta P2's: sized from what its maker prints (the blade's length "
                 "and thickness, from the documents) and, for what the maker prints nowhere (the blade's height at "
                 "heel and toe, the handle's outline and hand hole), measured from the maker's own product image, "
                 "scaled by the printed length, with the image kept by name and sha256 and the uncertainty stated in "
                 "the module's docstring (saws/models.py). A saw that cuts on one stroke only states it (payload "
                 "stroke, push or pull), and a hand saw follows tools/crosscut-saw, whose method it is used by",
            links={"rests_on": ["a-saw-states-only-what-its-maker-prints"]},
            payload={"decided_on": "2026-11-15",
                     "the_owner": "Add a 3D model of the Bahco ERGO Superior 2600-22 handsaw to the saws package, "
                                  "the way lamello-unofficial models the Zeta P2",
                     "why": "The instructions draw a tool from the model on its node and know no tool of their own, "
                            "so a saw is drawn only when its package carries a model, and a model is a figure like "
                            "any other that a reader may ask the source of. The image is the maker's own, kept "
                            "privately in the furniture repo's sources/saws; the 2600-22 is drawn with the 2600-19's "
                            "heights at heel and toe, no image of the 22 showing them."},
            children=[
                _alt("a-drawing-function-per-saw", "Draw each saw in code, in the instructions",
                     "The instructions' drawing code is to know no tool: a-tools-steps-are-drawn-from-its-node."),
                _alt("a-model-for-every-saw", "Model every saw in the package",
                     "A model is sized from its maker's print and image; the machines have no stroke to draw."),
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

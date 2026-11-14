"""Saws as data on furniture-design's kinds (source, clause, tool): what each saw's maker prints of the
width its blade takes out and of the thickest board it cuts through. Unofficial: neither the makers
wrote nor endorsed it.

A saw is one `tool` under tools/, payload saw_kind, its params derived from the clauses of its
maker's documents:

- kerf (mm): the cutting width of the blade the saw comes with, as its maker prints it;
- max_kerf (mm): the widest blade the saw takes (a tooth width or tooth set), where its maker prints
  no blade's;
- blade_thickness (mm): the blade's body, which a kerf is wider than;
- max_cut_depth (mm): the thickest board it cuts through at 90°.

What a maker does not print is not here: no portable circular saw's, jigsaw's or panel saw's maker
among these prints a blade's cut, so those saws state their depth alone, and furniture-design's rule
asks a design that cuts with one for a measured cut instead.

Every document is copyrighted, so a clause carries its locator and values and no quote; the copies
are kept private and tests/test_values.py checks every value against them.

    from furniture_design.knowledge import knowledge as general, merge
    from saws import knowledge as saws
    tree.root.children = merge(general(), saws()) + [pieces]
"""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

from quern.provenance import Quantity
from quern.tree import Node

HERE = Path(__file__).parent

# (id, name, saw_kind, what it does, {param: "document/clause/param"}): every saw, each param read from
# the clause its maker printed it in
SAWS = [
    ("festool-ts-55", "Festool TS 55 FEBQ", "plunge saw", "saws a part out of its board along a rail",
     {"kerf": "festool-ts-55-manual/saw-blades/kerf",
      "max_cut_depth": "festool-ts-55-manual/cutting-depth/max_cut_depth"}),
    ("bosch-gkt-55-gce", "Bosch GKT 55 GCE", "plunge saw", "saws a part out of its board along a rail",
     {"kerf": "bosch-gkt-55-gce-page/delivery/kerf",
      "blade_thickness": "bosch-gkt-55-gce-page/delivery/blade_thickness",
      "max_kerf": "bosch-gkt-55-gce-manual/technical-data/max_kerf",
      "max_cut_depth": "bosch-gkt-55-gce-manual/technical-data/max_cut_depth"}),
    ("makita-sp6000", "Makita SP6000", "plunge saw", "saws a part out of its board along a rail",
     {"max_cut_depth": "makita-sp6000-manual/specifications/max_cut_depth"}),
    ("bosch-gks-190", "Bosch GKS 190", "circular saw", "saws a part out of its board, held in the hand",
     {"max_cut_depth": "bosch-gks-190-manual/technical-data/max_cut_depth"}),
    ("makita-hs7601", "Makita HS7601", "circular saw", "saws a part out of its board, held in the hand",
     {"max_cut_depth": "makita-hs7601-manual/specifications/max_cut_depth"}),
    ("dewalt-dwe560", "DeWalt DWE560", "circular saw", "saws a part out of its board, held in the hand",
     {"max_cut_depth": "dewalt-dwe560-manual/technical-data/max_cut_depth"}),
    ("bosch-gts-635-216", "Bosch GTS 635-216", "table saw", "saws a part out of its board, fed along a fence",
     {"kerf": "bosch-blade-2-608-838-410-page/variants/kerf",
      "blade_thickness": "bosch-blade-2-608-838-410-page/variants/blade_thickness",
      "max_cut_depth": "bosch-gts-635-216-page/technical-data/max_cut_depth"}),
    ("makita-mlt100", "Makita MLT100", "table saw", "saws a part out of its board, fed along a fence",
     {"max_cut_depth": "makita-mlt100-manual/specifications/max_cut_depth"}),
    ("dewalt-dwe7492", "DeWalt DWE7492", "table saw", "saws a part out of its board, fed along a fence",
     {"blade_thickness": "dewalt-dwe7492-manual/technical-data/blade_thickness",
      "max_cut_depth": "dewalt-dwe7492-manual/technical-data/max_cut_depth"}),
    ("metabo-kgs-216-m", "Metabo KGS 216 M", "mitre saw", "cuts a board across, up to 305 mm wide",
     {"max_kerf": "metabo-kgs-m-manual/specification/max_kerf_kgs_216_m",
      "max_cut_depth": "metabo-kgs-m-manual/capacity-216/max_cut_depth"}),
    ("metabo-kgs-254-m", "Metabo KGS 254 M", "mitre saw", "cuts a board across, up to 305 mm wide",
     {"max_kerf": "metabo-kgs-m-manual/specification/max_kerf_kgs_254_m",
      "max_cut_depth": "metabo-kgs-m-manual/capacity-254/max_cut_depth"}),
    ("makita-ls1018l", "Makita LS1018L", "mitre saw", "cuts a board across, up to 305 mm wide",
     {"max_cut_depth": "makita-ls1018l-manual/capacities/max_cut_depth"}),
    ("bosch-gst-160-ce", "Bosch GST 160 CE", "jigsaw", "saws a curve or a cut-out, with its longest blade",
     {"max_cut_depth": "bosch-gst-160-manual/technical-data/max_cut_depth"}),
    ("makita-4350fct", "Makita 4350FCT", "jigsaw", "saws a curve or a cut-out, with its longest blade",
     {"max_cut_depth": "makita-4350fct-sheet/characteristics/max_cut_depth"}),
    ("striebig-compact", "Striebig Compact", "panel saw", "saws a panel standing upright, as a shop's cutting service does",
     {"max_cut_depth": "striebig-catalogue-fr/compact/max_cut_depth"}),
    ("striebig-standard", "Striebig Standard", "panel saw", "saws a panel standing upright, as a shop's cutting service does",
     {"max_cut_depth": "striebig-catalogue-fr/standard/max_cut_depth"}),
    ("holz-her-sector-1255", "Holz-Her Sector 1255", "panel saw", "saws a panel standing upright, as a shop's cutting service does",
     {"max_cut_depth": "holz-her-sector-brochure/technical-data/max_cut_depth"}),
    ("elcon-d", "Elcon D", "panel saw", "saws a panel standing upright, as a shop's cutting service does",
     {"max_cut_depth": "elcon-d-sheet/technical-data/max_cut_depth"}),
    ("z-saw-iii-265", "Z-saw III 265", "pull saw", "saws on the pull stroke, held in the hand",
     {"kerf": "z-saw-iii-265-page/spec/kerf", "blade_thickness": "z-saw-iii-265-page/spec/blade_thickness"}),
    ("z-saw-iii-300", "Z-saw III 300", "pull saw", "saws on the pull stroke, held in the hand",
     {"kerf": "z-saw-iii-300-page/spec/kerf", "blade_thickness": "z-saw-iii-300-page/spec/blade_thickness"}),
    ("gyokucho-blue-hard-210", "Gyokucho Blue Hard 210", "pull saw", "saws on the pull stroke, held in the hand",
     {"kerf": "gyokucho-blue-hard-page/spec-210/kerf",
      "blade_thickness": "gyokucho-blue-hard-page/spec-210/blade_thickness"}),
    ("gyokucho-blue-hard-240", "Gyokucho Blue Hard 240", "pull saw", "saws on the pull stroke, held in the hand",
     {"kerf": "gyokucho-blue-hard-page/spec-240/kerf",
      "blade_thickness": "gyokucho-blue-hard-page/spec-240/blade_thickness"}),
    ("gyokucho-blue-hard-270", "Gyokucho Blue Hard 270", "pull saw", "saws on the pull stroke, held in the hand",
     {"kerf": "gyokucho-blue-hard-page/spec-270/kerf",
      "blade_thickness": "gyokucho-blue-hard-page/spec-270/blade_thickness"}),
    ("gyokucho-orizuru-dozuki-240", "Gyokucho Orizuru dozuki 240", "pull saw",
     "saws fine joints on the pull stroke, its back stiffened",
     {"kerf": "gyokucho-orizuru-dozuki-240-page/spec/kerf",
      "blade_thickness": "gyokucho-orizuru-dozuki-240-page/spec/blade_thickness",
      "max_cut_depth": "gyokucho-orizuru-dozuki-240-page/use/max_cut_depth"}),
    ("bahco-2600-22", "Bahco ERGO Superior 2600-22", "hand saw", "saws on the push stroke, held in the hand",
     {"blade_thickness": "bahco-2600-page/2600-22/blade_thickness"}),
    ("bahco-2600-19", "Bahco ERGO Superior 2600-19", "hand saw", "saws on the push stroke, held in the hand",
     {"blade_thickness": "bahco-2600-page/2600-19/blade_thickness"}),
]
SOURCES = "sources"
TOOLS = "tools"


@lru_cache(maxsize=1)
def documents() -> dict[str, dict]:
    return {d["id"]: d for d in json.loads((HERE / "documents.json").read_text(encoding="utf-8"))["documents"]}


def _value(ref: str) -> dict:
    doc, clause, param = ref.split("/")
    return next(c for c in documents()[doc]["clauses"] if c["id"] == clause)["params"][param]


def sources() -> list[Node]:
    """One source per document, one clause per table or row read, its values as printed."""
    out = []
    for d in documents().values():
        clauses = [Node(id=c["id"], kind="clause",
                        payload={"locator": c["locator"], "rows": {k: v["printed"] for k, v in c["params"].items()}},
                        params={k: Quantity(value=float(v["value"]), unit=v["unit"], provenance="published",
                                            grounded=True, source=c["locator"], note=f"printed: {v['printed']}")
                                for k, v in c["params"].items()})
                   for c in d["clauses"]]
        out.append(Node(id=d["id"], kind="source", name=f"{d['publisher']}: {d['title']}",
                        payload={"publisher": d["publisher"], "url": d["url"], "fetched": d["fetched"],
                                 "sha256": d["sha256"], "licence": "copyrighted",
                                 "capture": "private copy, identified by its sha256"},
                        children=clauses))
    return out


def tools() -> list[Node]:
    """One tool per saw, each param derived from the clause its maker printed it in."""
    out = []
    for id_, name, kind, does, refs in SAWS:
        params = {p: Quantity(value=float(_value(ref)["value"]), unit=_value(ref)["unit"], provenance="derived",
                              grounded=True, derived_from=[f"{SOURCES}/{ref}"],
                              note=f"as printed: {_value(ref)['printed']}")
                  for p, ref in refs.items()}
        per = sorted({f"{SOURCES}/{ref.rsplit('/', 1)[0]}" for ref in refs.values()})
        out.append(Node(id=id_, kind="tool", name=name,
                        payload={"maker": documents()[next(iter(refs.values())).split("/")[0]]["publisher"],
                                 "saw_kind": kind, "does": does},
                        params=params, links={"per": per}))
    return out


def knowledge() -> list[Node]:
    """The branches to merge beside furniture-design's: the sources and the saws."""
    return [Node(id=SOURCES, kind="", children=sources()), Node(id=TOOLS, kind="", children=tools())]

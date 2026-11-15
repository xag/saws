"""The Bahco handsaws' models, as data on their nodes, and the strokes the saws state."""

import numpy as np

from furniture_design.knowledge import knowledge as general, merge
from furniture_design.lineart import solids
from saws import knowledge

BLADES = {"bahco-2600-22": 550.0, "bahco-2600-19": 475.0}


def _tools() -> dict:
    return {n.id: n for n in knowledge()[1].children}


def _extent(model: dict, axis: int) -> tuple[float, float]:
    v = np.vstack([m.v for m in solids(model["parts"])])
    return float(v[:, axis].min()), float(v[:, axis].max())


def test_a_handsaw_is_solids_whose_blade_is_as_long_as_its_maker_prints_and_whose_handle_lies_behind_the_heel():
    for id_, length in BLADES.items():
        model = _tools()[id_].payload["model"]
        assert model["teeth"] == {"from": [0, 0], "to": [length, 0]}
        lo, hi = _extent(model, 1)
        assert hi == length, id_                      # the toe's tip is the end of the teeth
        assert -90 < lo < -70, id_                    # the handle, read off the image: 118 mm along the blade
        assert "bahco-2600-16a27527dd579a3f.png" in model["source"]
        zlo, zhi = _extent(model, 2)
        assert zlo == 0 and 125 < zhi < 140, id_      # the teeth at Z = 0, the handle 132 high
        xlo, xhi = _extent(model, 0)
        assert abs(xlo + xhi) < 1e-6 and 30 < xhi - xlo < 36, id_  # centred across the blade


def test_the_two_handsaws_have_the_same_handle_and_their_blades_differ_in_length_only():
    m22, m19 = (_tools()[i].payload["model"]["parts"] for i in ("bahco-2600-22", "bahco-2600-19"))
    assert m22[1:-1] == m19[1:-1] and m22[0] != m19[0]


def test_the_handsaws_follow_the_general_hand_saw_and_it_exists():
    tree = {n.id: n for n in merge(general(), knowledge())}["tools"]
    ids = {n.id for n in tree.children}
    for id_ in BLADES:
        assert (_tools()[id_].links["follows"]) == ["tools/crosscut-saw"]
    assert "crosscut-saw" in ids


def test_every_saw_with_a_stroke_states_it_and_the_others_state_none():
    for id_, tool in _tools().items():
        kind = tool.payload["saw_kind"]
        stroke = tool.payload.get("stroke")
        if kind == "hand saw":
            assert stroke == "push", id_
        elif kind == "pull saw":
            assert stroke == "pull", id_
        else:
            assert stroke is None, id_

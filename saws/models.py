"""The Bahco ERGO Superior 2600 handsaws as solids, for the assembly instructions' drawings: data in
furniture-design's model format (furniture_design.lineart.solids), each solid an op and its sizes in mm.

The saw in its own frame, the one furniture-design's drawn cut expects: Y along the teeth from the heel
(Y = 0, where the teeth end at the handle) to the toe (Y = the blade's length; the handle lies between
Y = -78 and Y = 40, its front leaning toward the toe), Z up from the line of the teeth, X across the
blade's thickness, its middle at X = 0. The model's "teeth" gives the toothed line's ends as (Y, Z) and
its "source" where the sizes come from.

What Bahco prints (documents.json, source bahco-2600-page, rows 2600-22-XT-HP and 2600-19-XT-HP): the
blade's length, 550 mm for the 22 and 475 mm for the 19, and its thickness, 1.03 mm. Bahco prints no
more. The rest is measured from Bahco's own product image of the 2600-19-XT-HP (the 2048 x 983 px PNG
bahco-2600-16a27527dd579a3f.png, sha256 7edef28d6d7644127a41909f4a86be7f4d47d5c9da3b6fab3cac9d75b411ab2d,
kept in sources/saws of the furniture repo, fetched 2026-11-15 from pimdatacdn.bahco.com/media/sub402/;
that host has no robots.txt and the page's own robots.txt does not exclude the images). In the image the
toe's tip is at (55, 927) px and the end of the teeth at the handle at (1737, 562) px, 1721 px apart,
which are the 475 mm printed on the saw's own label in the image: 0.276 mm per pixel. The blade's height
at the heel (100 mm where it enters the handle's front, 105 at the heel line) and at the toe (47 mm,
where its back edge ends and the toe's slanted end begins), the handle's outline (118 mm along the blade
by 132 mm high) and its hand hole (about 43 x 77 mm; the grip is drawn as a loop of constant width
round the line between the two) are read off the image at that scale, each point to
about 4 px, so to about 3 mm; the photo is square on the saw, its tilt in the frame undone, so a length read off it is good to
about 5 %. What the image cannot give is the handle's thickness across the blade (it shows no
side view): 30 mm for the grip and 34 mm for the front, an estimate good to about 30 %. The 2600-22's
blade is drawn as the 2600-19's, lengthened to its printed 550 mm with the same heights at the heel and
at the toe, since no image of the 22 shows them: its back edge is a straight line between the same two
heights. Both saws have the same handle.
"""
from __future__ import annotations

THICKNESS = 1.03          # mm, the blade's body, as Bahco prints it
HEEL_TOP = (38.2, 99.8)   # (Y, Z) where the blade's back edge meets the handle's front
TOE_BACK = 47.4           # Z of the back edge where the toe's slanted end begins
TOE_RUN = 48.4            # mm along the teeth from that corner to the tip
SLOT_FROM_TOE, SLOT_Z = 56.1, 30.8   # the hole in the toe, about 18 x 11 mm: its distance from the tip, its height

# the handle's grip as the middle line of its wood in (Y, Z), round the hand hole: the line between the
# outline and the hole read off the image, the wood drawn 30 mm wide (it is 35 at the top, 38 at the back and 17 to 38 at the bottom)
GRIP = [(21, 96), (0, 107), (-28, 115), (-48, 116), (-52, 98), (-53, 70), (-57, 40), (-61, 22), (-30, 15),
        (-2, 24), (19, 30), (21, 60)]
WOOD, GRIP_THICK = 30, 30
SCREWS = [(18.9, 84.6), (21.3, 47.6), (-4.1, 21.7)]   # where the three rivets show, (Y, Z), read off the image


def _prism(profile, x0, x1):
    return {"op": "prism", "profile": [list(p) for p in profile], "x": [x0, x1]}


def ergo_superior_2600(length: float) -> dict:
    """A 2600 handsaw with a blade `length` mm long (Bahco's printed 550 or 475): a flat steel blade with
    its teeth along Z = 0, narrowing from the heel to the toe, and the moulded handle at the heel."""
    top = (HEEL_TOP[1] - TOE_BACK) / (length - TOE_RUN - HEEL_TOP[0])
    heel_z = HEEL_TOP[1] + top * HEEL_TOP[0]              # the back edge's height over the heel line
    blade = [(0, 0), (length, 0), (length - TOE_RUN, TOE_BACK), (0, heel_z)]
    return {"parts": [
        _prism(blade, -THICKNESS / 2, THICKNESS / 2),
        {"op": "tube", "path": [[0, y, z] for y, z in GRIP + GRIP[:1]], "w": GRIP_THICK, "h": WOOD, "r": 6,
         "normal": [1, 0, 0]},
        *[{"op": "cyl", "r": 3.5, "h": 35, "axis": "x", "at": [-17.5, y, z], "n": 12, "dark": True} for y, z in SCREWS],
        {"op": "cyl", "r": 5.5, "h": THICKNESS + 0.8, "axis": "x", "at": [-THICKNESS / 2 - 0.4, length - SLOT_FROM_TOE, SLOT_Z],
         "n": 16, "dark": True}],
        "teeth": {"from": [0, 0], "to": [float(length), 0]},
        "source": "Bahco, ERGO Superior 2600 (bahco-2600-page: blade length and thickness printed); the rest "
                  "measured from its product image bahco-2600-16a27527dd579a3f.png, sha256 7edef28d6d7644127a41909f4a86be7f4d47d5c9da3b6fab3cac9d75b411ab2d"}

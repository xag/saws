# saws

Saws as data for [furniture-design](https://github.com/xag/furniture-design): the width each saw's blade takes out and the thickest board it cuts through, as its maker prints them. **Unofficial**: the makers did not write or endorse it, and nothing here speaks for them.

## What is here

One `tool` per saw under `tools/`, its payload `saw_kind` (plunge saw, circular saw, table saw, mitre saw, jigsaw, panel saw, pull saw, hand saw), its params read from its maker's documents:

- `kerf` (mm): the cut of the blade the saw comes with. Festool TS 55 1.8, Bosch GKT 55 GCE 1.8, Bosch GTS 635-216 2.6 (its blade 2 608 838 410), Z-saw III 265 and 300 0.92 and 1.07, Gyokucho Blue Hard 210, 240 and 270 0.72, 0.83 and 0.94, Gyokucho Orizuru dozuki 240 0.46.
- `max_kerf` (mm): the widest blade the saw takes, where its maker prints no blade's cut. Bosch GKT 55 GCE 2.6, Metabo KGS 216 M 2.4 and KGS 254 M 2.6.
- `blade_thickness` (mm): the blade's body, which the cut is wider than.
- `max_cut_depth` (mm): the thickest board it cuts through at 90°. Plunge saws 55 to 57, portable circular saws (Bosch GKS 190, Makita HS7601, DeWalt DWE560) 65 to 67, table saws (Bosch GTS 635-216, Makita MLT100, DeWalt DWE7492) 70 to 90.5, mitre saws (Metabo KGS 216 M and 254 M, Makita LS1018L) 70 to 92, jigsaws (Bosch GST 160 CE, Makita 4350FCT) 160 and 135, vertical panel saws as shops' cutting services use (Striebig Compact and Standard, Holz-Her Sector 1255, Elcon D) 60 to 80, the dozuki 35.

What a maker does not print is not here. No maker of a portable circular saw, a jigsaw or a panel saw among these prints the cut of a blade, and Bahco prints its handsaw's body (1.03 mm) but not its cut, so those saws carry no `kerf`; furniture-design's rule `a-part-is-sawn-with-a-saw-that-states-its-cut` then refuses a part cut out with one, until the design states a measured cut on a saw of its own or cuts with the usual blade of the saw's diameter (below). A saw whose maker prints no depth (the pull saws but the dozuki, the handsaws) leaves `a-part-is-no-thicker-than-its-saw-cuts` absent.

## Usual blades

A saw whose maker prints no cut can still be counted by the blade it takes. Blade catalogues list their blades by diameter, each blade fitting several kinds of machine, so the usual cut is known by the diameter. For every diameter that at least two catalogues list wood blades of (Freud's product finder for portable machines, Leitz Lexicon chapter 1.7.1, CMT's 2017 catalogue for mitre, table, portable and cordless saws), one tool `usual-blade-<D>` (120 to 300 mm) carries as `max_kerf` the widest cut among those blades: 2.5 mm at 160 mm, 2.6 at 165 and 184, 2.8 at 190, 3.0 at 216, 3.2 at 250. Its payload's `usual` gives the narrowest cut and the number of blades. Each catalogue is a source with one clause per diameter (its narrowest and widest cut, the pages), and `tests/test_usual.py` reads every row again from the copy.

A maker's saw keeps only what its maker prints. Where its maker prints the blade's diameter, its payload's `blade` names it and the usual blade of it: the Bosch GKS 190 and Makita HS7601 take 190 mm blades (`tools/usual-blade-190`), the DeWalt DWE560 184, the Makita SP6000 165, the Makita MLT100 and LS1018L 255, the DeWalt DWE7492 250. A design that cuts with one of them and has not measured its cut links `sawn_with` the usual blade, and the cutting sheet names that blade, not the saw. Jigsaws, upright panel saws and handsaws have no usual blade here: no catalogue of theirs was read.

A beam saw (a panel sizing saw that cuts the board lying flat under a pressure beam, the *scie à plat* of a shop's cutting service) has one usual blade whatever its diameter, `tools/usual-panel-sizing-blade`, since a shop names its machine and not its blade. Its `max_kerf` is the widest cut among the main panel sizing blades at every diameter both Leitz (Lexicon chapter 1.4.1 to 1.4.3, not the scoring blades) and CMT (2017 catalogue, printed p. 25, 281-282) list, 250 to 550 mm: 5.2 mm. Its payload's `usual` gives the narrowest cut (3.2 mm) and the commonest (4.4 mm, 111 of the 148 blades). Leitz alone lists 600 to 750 mm blades, up to 7.0 mm, which are not counted.

No kinds and no rules of its own: a part links `sawn_with: ["tools/festool-ts-55"]`, and furniture-design's rules judge it and its cutting sheet leaves the saw's cut between the parts.

## Sources

The documents are the makers' operating manuals, data sheets and product pages, fetched on 2026-11-14. They are copyrighted, so they are cited by locator and values and never quoted. The copies as fetched are kept in a private repo, and `tests/test_values.py` checks every value against them, a table's value against its row and column: clone that repo beside this one, or set `FURNITURE_REPO`, or that test fails and says why.

## Using it

```python
from furniture_design.knowledge import knowledge as general, merge
from saws import knowledge as saws

tree.root.children = merge(general(), saws()) + [pieces]
```

## Design ledger

```sh
uv sync
uv run quern brief .
uv run quern check
```

There is no flight-recorder boundary: nothing here touches storage, the network, the clock or randomness at run time.

## Licence

- **The code** (`saws/*.py`, `tests/`, `ledger/`) is licensed under the [GNU Affero General Public License v3.0 or later](LICENSE), copyright 2026 Xavier Grehant.
- **The knowledge base**, the database `saws.knowledge()` returns (documents.json and every value on its nodes), is licensed under [Creative Commons Attribution-NonCommercial-NoDerivatives 4.0](LICENSE-DATA), database rights included, with one added permission: designing, building and selling furniture with it is allowed. An improvement is published here, through [CONTRIBUTING.md](CONTRIBUTING.md).
- The makers' values are cited from their documents, not licensed.

## Tests

`uv run pytest --testmon`, then `uv run pytest`. Both stop at the first failure.

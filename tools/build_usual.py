"""Write saws/usual.json: the rows of each blade catalogue, read from its copy in the private repo (xag/furniture,
sources/saws/, beside this repo or at $FURNITURE_REPO) by tests/readings.py. Run once when a catalogue is
added; tests/test_usual.py reads the copies again and checks every row.

    uv run python tools/build_usual.py
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tests"))
from readings import READINGS  # noqa: E402

CAPTURES = Path(os.environ.get("FURNITURE_REPO", ROOT.parent / "furniture")) / "sources" / "saws"

CATALOGUES = [
    {"id": "freud-portable-finder", "publisher": "Freud S.p.A.",
     "title": "Circular saw blade range for portable machines: product finder (MKFRM 249)",
     "url": "https://www.freudtools.com/gb/media/downloads/fr_k_csb_freud_portable_product_finder_mkfrm_249_f03fa25223_eng_v0_psw.pdf",
     "fetched": "2026-11-14", "sha256": "d16e71aaa3e16f863ddd4205cff49c4de0216bf41f7968498cde3266a6d2dcbf",
     "file": "blades-freud-portable-finder.pdf", "text": "blades-freud-portable-finder.txt",
     "reading": "freud", "pages": [4, 5, 6, 7, 8, 9, 10], "machine": "circular saw",
     "locator": "pp. 4-10, wood: for hand-held and plunge circular saws, cordless hand-held, mitre and cordless "
                "mitre, small table and cordless small table saws; columns D, B (cutting width), b (body), d"},
    {"id": "leitz-lexicon-7-sawing", "publisher": "Leitz GmbH & Co. KG",
     "title": "Leitz Lexicon Edition 7, chapter 1: Sawing",
     "url": "https://www.leitz.org/fileadmin/Downloads/Lexicon/EN/Leitz_Lexicon_Edition_7_-_01_Sawing.pdf",
     "fetched": "2026-11-14", "sha256": "daf1ed1f3153284ca588b6658897e8c9bd1c28dc603109468aeca3d0c3de79f0",
     "file": "blades-leitz-lexicon7-sawing.pdf", "text": "blades-leitz-lexicon7-sawing.txt",
     "reading": "leitz", "pages": [80, 81, 83], "machine": "circular saw",
     "locator": "1.7.1 Circular sawblades WZ, the pages whose machines are accu-portable saws (p. 80), portable "
                "and table saws (p. 81), trimming and mitre saws (p. 83); columns D, SB (cutting width), TDI, BO"},
    {"id": "cmt-catalogue-2017", "publisher": "CMT Utensili",
     "title": "General catalogue 2017, English (03.60.3006): circular saw blades",
     "url": "https://cmt-shop.ru/upload/medialibrary/f73/143_1895_03.60.3006_cat_en_2017.pdf",
     "fetched": "2026-11-14", "sha256": "1d3bcf7ea5b171a0069f1b4a9d6843c225fb63e1a3c3e113a236ef04263bc597",
     "file": None, "text": "blades-cmt-catalogue-2017.txt",
     "reading": "cmt", "pages": [33, 34, 35, 36, 37, 38], "machine": "circular saw",
     "locator": "pp. 33-38, the wood blades whose machines are mitre, table, portable and cordless saws (ITK-Plus "
                "271-273, cordless 271-272, rip 290, crosscut 285-291, fine cut-off 281-285-292); columns D, B, Z, "
                "K (kerf), P (plate). A mirror of the maker's catalogue; its 70 MB PDF is identified by its sha256 "
                "and its text kept"},
    {"id": "leitz-lexicon-7-panel-sizing", "publisher": "Leitz GmbH & Co. KG",
     "title": "Leitz Lexicon Edition 7, chapter 1: Sawing",
     "url": "https://www.leitz.org/fileadmin/Downloads/Lexicon/EN/Leitz_Lexicon_Edition_7_-_01_Sawing.pdf",
     "fetched": "2026-11-14", "sha256": "daf1ed1f3153284ca588b6658897e8c9bd1c28dc603109468aeca3d0c3de79f0",
     "file": "blades-leitz-lexicon7-sawing.pdf", "text": "blades-leitz-lexicon7-sawing.txt",
     "reading": "leitz", "pages": [44, 45, 46, 47, 48, 49, 50, 51], "machine": "panel saw",
     "locator": "1.4 Panel sizing, the main sawblades of panel sizing saws with a pressure beam: 1.4.1 WZ (p. 44), "
                "1.4.2 FZ/TR (pp. 45-47), 1.4.3 TR/TR (pp. 48-51); not the scoring blades; columns D, SB (cutting "
                "width), TDI, BO"},
    {"id": "cmt-catalogue-2017-panel-sizing", "publisher": "CMT Utensili",
     "title": "General catalogue 2017, English (03.60.3006): circular saw blades",
     "url": "https://cmt-shop.ru/upload/medialibrary/f73/143_1895_03.60.3006_cat_en_2017.pdf",
     "fetched": "2026-11-14", "sha256": "1d3bcf7ea5b171a0069f1b4a9d6843c225fb63e1a3c3e113a236ef04263bc597",
     "file": None, "text": "blades-cmt-catalogue-2017.txt",
     "reading": "cmt", "pages": [28], "machine": "panel saw",
     "locator": "printed p. 25, Panel Sizing Saw Blades Industrial Line 281-282, for horizontal panel sizing "
                "machines; columns D, B, Z, K (kerf), P (plate). A mirror of the maker's catalogue; its 70 MB PDF is "
                "identified by its sha256 and its text kept"},
]


def main() -> None:
    out = []
    for c in CATALOGUES:
        text_path = CAPTURES / c["text"]
        text = text_path.read_text(encoding="utf-8", errors="replace")
        rows = READINGS[c["reading"]](text, c["pages"])
        out.append({**c, "text_sha256": hashlib.sha256(text_path.read_bytes()).hexdigest(), "rows": rows})
        print(c["id"], len(rows), "rows")
    (ROOT / "saws" / "usual.json").write_text(json.dumps({"catalogues": out}, ensure_ascii=False, indent=1) + "\n",
                                              encoding="utf-8")


if __name__ == "__main__":
    main()

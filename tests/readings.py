"""How a blade catalogue's rows are read from its text (pdftotext -layout, one page per form feed): each
row a blade, (page, D, kerf, body), its diameter, its cutting width and its body as printed. Used by
tools/build_usual.py to write saws/usual.json once, and by tests/test_usual.py to check every row
listed there against the copy again."""

from __future__ import annotations

import re

READINGS = {}


def reading(fn):
    READINGS[fn.__name__] = fn
    return fn


def _pages(text: str) -> list[str]:
    return text.split("\f")


def _mm(s: str) -> float:
    return float(s.replace(",", "."))


@reading
def freud(text: str, pages: list[int]) -> list[list]:
    """Columns D, B (cutting width), b (body), d (bore), each row at the start of its line."""
    out = []
    for i, page in enumerate(_pages(text), 1):
        if i in pages:
            for line in page.split("\n"):
                m = re.match(r"^\s*(\d{3})\s+(\d,\d)\s+(\d,\d)\s+(\d{2})\b", line)
                if m:
                    out.append([i, int(m[1]), _mm(m[2]), _mm(m[3])])
    return out


@reading
def leitz(text: str, pages: list[int]) -> list[list]:
    """Columns D, SB (cutting width), TDI (body), BO (bore); a margin label or a chart's text may stand
    before a row on its line."""
    out = []
    for i, page in enumerate(_pages(text), 1):
        if i in pages:
            for line in page.split("\n"):
                m = re.search(r"(?:^|\s)(\d{2,3})\s+(\d,\d)\s+(\d,\d)\s+(\d{2})\b", line)
                if m:
                    out.append([i, int(m[1]), _mm(m[2]), _mm(m[3])])
    return out


@reading
def cmt(text: str, pages: list[int]) -> list[list]:
    """Columns D, B (bore), pin hole, Z, K (kerf), P (plate): the first Z K P after the bore. Rows under a
    heading for diamond (DP) blades, metal or a garden trimmer are left out; a row whose numbers the text
    layer prints on its heading's line (p. 35, the 136 mm cordless blades) is not read."""
    out = []
    for i, page in enumerate(_pages(text), 1):
        if i in pages:
            head = ""
            for line in page.split("\n"):
                if "Saw Blades" in line and not re.match(r"^\s*\d", line):
                    head = line
                m = re.match(r"^\s*(\d{2,3})\s+(\d{2}(?:,\d+)?)\b.*?\s(\d{1,3})\s+(\d,\d)\s+(\d,\d)\s", line)
                if m and not re.search(r"DP |Garden|Metal|Compound", head):
                    out.append([i, int(m[1]), _mm(m[4]), _mm(m[5])])
    return out

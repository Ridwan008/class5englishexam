#!/usr/bin/env python3
"""Class 5 English SMT 04 — A4 portrait, 2 pages, fully editable Word."""
from __future__ import annotations

import shutil
from pathlib import Path

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml import OxmlElement
from docx.shared import Mm, Pt, RGBColor, Emu
from docx.oxml.ns import qn

OUT = Path("/workspace/public/downloads")
ART = Path("/workspace/artifacts")
PUBLIC = Path("/workspace/public")
FONT = "Times New Roman"
A4_W, A4_H = 210.0, 297.0
ML, MR, MT, MB = 16.0, 16.0, 14.0, 14.0
CW = A4_W - ML - MR  # 178mm


PASSAGE1 = [
    "Farhana's school planned a field trip for the students of class five. They asked students to fill a registration form for the trip. On a sunny morning, they started for the Liberation War Museum at Agargaon, Dhaka. She and her classmates were excited to explore the museum. Their class teacher, Mr. Khan, went with them on this trip.",
    "They started from their school by bus at 9 a.m. The bus ride was filled with chatter and laughter. Farhana sat next to her friend Rabeya. They sang songs together. When they reached the museum at 10 a.m., the guide, Mr. Kamal greeted them. His welcoming attitude pleased them.",
    "Mr. Kamal guided them to see the different corners of the museum. First, they watched a short documentary. It showed the bravery of the freedom fighters during the Liberation War. Their patriotism and sacrifice inspired them.",
    "Around half past ten, they started visiting different galleries. Old photographs of war, handwritten letters of the freedom fighters, and their weapons were displayed. They carry the memories of the war.",
    "They saw the personal belongings of the war heroes. The display of the galleries made them curious to learn more about the Liberation War. Finally, they thanked their guide for his support.",
    "They left the museum at 12:30 p.m. and returned to school at 1:30 p.m. They shared their feelings and experiences with their families. It was really a memorable trip for them.",
]

PASSAGE2 = (
    "Roni lives with his parents in a beautiful house. There is a big yard in front of their house. "
    "Roni reads in a local government primary school. He is a student of class 5. He likes gardening. "
    "He made a flower garden in front of their house. It gives him much pleasure. Everyday Roni works "
    "in the garden at least an hour. On holidays he works more in the garden. His parents help him in "
    "the garden. Roni waters the plants regularly. He keeps the garden clean. He made a fence around "
    "the garden to save the plants from cows and goats. There are many kinds of flowers in his garden. "
    "He becomes very happy when the garden is full of flowers. When his friends or relatives come to "
    "visit his house, he takes them into his garden to show them various kinds of flowers. They become "
    "surprised and very happy to see the garden. Roni also grows some vegetables in one corner of the "
    "garden. His mother is very happy to have the vegetables. Roni feels very proud of his garden."
)


def mm_dxa(mm: float) -> int:
    return int(round(mm * 1440 / 25.4))


def set_run_font(run, size=11, bold=False, italic=False, underline=False):
    run.font.name = FONT
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic
    run.underline = underline
    rPr = run._element.get_or_add_rPr()
    rFonts = rPr.find(qn("w:rFonts"))
    if rFonts is None:
        rFonts = OxmlElement("w:rFonts")
        rPr.append(rFonts)
    for a in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rFonts.set(qn(a), FONT)


def spacing(p, before=0, after=2, line=1.08):
    fmt = p.paragraph_format
    fmt.space_before = Pt(before)
    fmt.space_after = Pt(after)
    fmt.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    fmt.line_spacing = line
    fmt.widow_control = True


def add_runs(p, parts):
    for text, kw in parts:
        r = p.add_run(text)
        set_run_font(r, **kw)
    return p


def P(doc, text="", size=11, bold=False, italic=False, align="left", before=0, after=2, line=1.06, underline=False):
    p = doc.add_paragraph()
    p.alignment = {
        "left": WD_ALIGN_PARAGRAPH.LEFT,
        "center": WD_ALIGN_PARAGRAPH.CENTER,
        "right": WD_ALIGN_PARAGRAPH.RIGHT,
        "justify": WD_ALIGN_PARAGRAPH.JUSTIFY,
    }[align]
    spacing(p, before=before, after=after, line=line)
    if text:
        r = p.add_run(text)
        set_run_font(r, size=size, bold=bold, italic=italic, underline=underline)
    return p


def set_table_width(table, width_mm):
    tbl = table._tbl
    tblPr = tbl.tblPr
    tblW = tblPr.find(qn("w:tblW"))
    if tblW is None:
        tblW = OxmlElement("w:tblW")
        tblPr.append(tblW)
    tblW.set(qn("w:w"), str(mm_dxa(width_mm)))
    tblW.set(qn("w:type"), "dxa")
    # no autofit
    table.autofit = False
    table.allow_autofit = False
    tblPr_el = tblPr
    existing = tblPr_el.find(qn("w:tblLayout"))
    if existing is not None:
        tblPr_el.remove(existing)
    lay = OxmlElement("w:tblLayout")
    lay.set(qn("w:type"), "fixed")
    tblPr_el.append(lay)


def set_col_widths(table, widths_mm):
    tbl = table._tbl
    grid = tbl.tblGrid
    for child in list(grid):
        grid.remove(child)
    for w in widths_mm:
        gc = OxmlElement("w:gridCol")
        gc.set(qn("w:w"), str(mm_dxa(w)))
        grid.append(gc)
    for row in table.rows:
        for i, cell in enumerate(row.cells):
            cell.width = Mm(widths_mm[i])
            tc = cell._tc
            tcPr = tc.get_or_add_tcPr()
            tcW = tcPr.find(qn("w:tcW"))
            if tcW is None:
                tcW = OxmlElement("w:tcW")
                tcPr.append(tcW)
            tcW.set(qn("w:w"), str(mm_dxa(widths_mm[i])))
            tcW.set(qn("w:type"), "dxa")


def borders(table, sz=8, color="000000", inside=True):
    tblPr = table._tbl.tblPr
    old = tblPr.find(qn("w:tblBorders"))
    if old is not None:
        tblPr.remove(old)
    b = OxmlElement("w:tblBorders")
    edges = ["top", "left", "bottom", "right"] + (["insideH", "insideV"] if inside else [])
    for e in edges:
        el = OxmlElement(f"w:{e}")
        el.set(qn("w:val"), "single")
        el.set(qn("w:sz"), str(sz))
        el.set(qn("w:space"), "0")
        el.set(qn("w:color"), color)
        b.append(el)
    if not inside:
        for e in ("insideH", "insideV"):
            el = OxmlElement(f"w:{e}")
            el.set(qn("w:val"), "nil")
            el.set(qn("w:sz"), "0")
            el.set(qn("w:space"), "0")
            el.set(qn("w:color"), "auto")
            b.append(el)
    tblPr.append(b)


def no_borders(table):
    tblPr = table._tbl.tblPr
    old = tblPr.find(qn("w:tblBorders"))
    if old is not None:
        tblPr.remove(old)
    b = OxmlElement("w:tblBorders")
    for e in ("top", "left", "bottom", "right", "insideH", "insideV"):
        el = OxmlElement(f"w:{e}")
        el.set(qn("w:val"), "nil")
        el.set(qn("w:sz"), "0")
        el.set(qn("w:space"), "0")
        el.set(qn("w:color"), "auto")
        b.append(el)
    tblPr.append(b)


def shade(cell, fill):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill)
    tcPr.append(shd)


def cell_margins(cell, top=40, bottom=40, left=60, right=60):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement("w:tcMar")
    for m, v in (("top", top), ("left", left), ("bottom", bottom), ("right", right)):
        n = OxmlElement(f"w:{m}")
        n.set(qn("w:w"), str(v))
        n.set(qn("w:type"), "dxa")
        tcMar.append(n)
    tcPr.append(tcMar)


def cell_p(cell, text, size=11, bold=False, italic=False, align="left", after=0):
    p = cell.paragraphs[0]
    p.text = ""
    p.alignment = {
        "left": WD_ALIGN_PARAGRAPH.LEFT,
        "center": WD_ALIGN_PARAGRAPH.CENTER,
        "right": WD_ALIGN_PARAGRAPH.RIGHT,
        "justify": WD_ALIGN_PARAGRAPH.JUSTIFY,
    }[align]
    spacing(p, before=0, after=after, line=1.08)
    if text:
        r = p.add_run(text)
        set_run_font(r, size=size, bold=bold, italic=italic)
    return p


def qhead(doc, num, stem, marks, width_mm=None):
    if width_mm is None:
        width_mm = CW * 0.46 if isinstance(doc, CellWrap) else CW
    table = doc.add_table(rows=1, cols=2)
    set_table_width(table, width_mm)
    left, right = width_mm * 0.78, width_mm * 0.22
    set_col_widths(table, [left, right])
    no_borders(table)
    lc, rc = table.rows[0].cells
    cell_margins(lc, 40, 40, 0, 80)
    cell_margins(rc, 40, 40, 40, 0)
    prefix = f"{num}.  " if num else ""
    p = cell_p(lc, prefix + stem, size=11, bold=True)
    p.paragraph_format.keep_with_next = True
    rp = cell_p(rc, marks, size=11, bold=True, align="right")
    rp.paragraph_format.keep_with_next = True
    return table


def bank(doc, words, width_mm=None):
    if width_mm is None:
        width_mm = CW * 0.46 if isinstance(doc, CellWrap) else CW
    table = doc.add_table(rows=1, cols=1)
    set_table_width(table, width_mm)
    set_col_widths(table, [width_mm])
    borders(table, sz=8, inside=False)
    cell = table.rows[0].cells[0]
    shade(cell, "F3F3F3")
    cell_margins(cell, 60, 60, 80, 80)
    cell_p(cell, "     ".join(words), size=11, bold=True, align="center")


def boxed(doc, text, italic=True, width_mm=None):
    if width_mm is None:
        width_mm = CW * 0.46 if isinstance(doc, CellWrap) else CW
    table = doc.add_table(rows=1, cols=1)
    set_table_width(table, width_mm)
    set_col_widths(table, [width_mm])
    borders(table, sz=8, inside=False)
    cell = table.rows[0].cells[0]
    shade(cell, "FAFAFA")
    cell_margins(cell, 80, 80, 100, 100)
    cell_p(cell, text, size=11, italic=italic)


def passage(doc, paragraphs):
    table = doc.add_table(rows=1, cols=1)
    set_table_width(table, CW)
    set_col_widths(table, [CW])
    borders(table, sz=8, inside=False)
    cell = table.rows[0].cells[0]
    cell_margins(cell, 80, 80, 100, 100)
    first = True
    for i, t in enumerate(paragraphs):
        if first:
            p = cell.paragraphs[0]
            first = False
        else:
            p = cell.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        spacing(p, before=0, after=3 if i < len(paragraphs) - 1 else 0, line=1.08)
        r = p.add_run(t)
        set_run_font(r, size=11)


def or_line(doc, text="Or"):
    P(doc, text, size=11, bold=True, italic=True, align="center", before=3, after=2)


def mcq(doc, letter, q, opts):
    labels = ["i.", "ii.", "iii.", "iv."]
    bits = "    ".join(f"{lab} {opt}" for lab, opt in zip(labels, opts))
    P(doc, f"({letter})  {q}    {bits}", size=10.5, before=1, after=1, line=1.05)


def unlock_settings(document):
    """Ensure the file is a normal editable document — no booklet, no protection."""
    settings = document.settings.element
    for tag in (
        "bookFoldPrinting",
        "bookFoldPrintingSheets",
        "documentProtection",
        "writeProtection",
        "revisionView",
        "readOnlyRecommended",
    ):
        for el in list(settings.findall(qn(f"w:{tag}"))):
            settings.remove(el)
    # remove east-asia lock-ish lang that some mobile Word builds choke on
    for el in list(settings.findall(qn("w:themeFontLang"))):
        el.set(qn("w:val"), "en-US")
        if qn("w:eastAsia") in el.attrib:
            del el.attrib[qn("w:eastAsia")]


def build_docx(path: Path):
    doc = Document()
    style = doc.styles["Normal"]
    style.font.name = FONT
    style.font.size = Pt(11)
    rPr = style.element.get_or_add_rPr()
    rFonts = rPr.find(qn("w:rFonts"))
    if rFonts is None:
        rFonts = OxmlElement("w:rFonts")
        rPr.append(rFonts)
    for a in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rFonts.set(qn(a), FONT)
    pf = style.paragraph_format
    pf.space_before = Pt(0)
    pf.space_after = Pt(0)
    pf.line_spacing = 1.08

    sec = doc.sections[0]
    sec.page_width = Mm(A4_W)
    sec.page_height = Mm(A4_H)
    sec.left_margin = Mm(ML)
    sec.right_margin = Mm(MR)
    sec.top_margin = Mm(MT)
    sec.bottom_margin = Mm(MB)
    sec.header_distance = Mm(8)
    sec.footer_distance = Mm(8)
    sec.different_first_page_header_footer = False

    # Simple editable header / footer (plain text, no fields)
    hp = sec.header.paragraphs[0]
    hp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    spacing(hp, 0, 0, 1.0)
    add_runs(hp, [("Rabeya Coaching Center  ·  Special Model Test 04  ·  Class Five English", {"size": 10, "italic": True})])
    pPr = hp._p.get_or_add_pPr()
    pBdr = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), "6")
    bottom.set(qn("w:space"), "4")
    bottom.set(qn("w:color"), "000000")
    pBdr.append(bottom)
    pPr.append(pBdr)

    fp = sec.footer.paragraphs[0]
    fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    spacing(fp, 0, 0, 1.0)
    add_runs(fp, [("A4  ·  2 pages  ·  Fully editable  ·  Do not write on this question paper", {"size": 9, "italic": True})])
    pPr = fp._p.get_or_add_pPr()
    pBdr = OxmlElement("w:pBdr")
    top = OxmlElement("w:top")
    top.set(qn("w:val"), "single")
    top.set(qn("w:sz"), "6")
    top.set(qn("w:space"), "4")
    top.set(qn("w:color"), "000000")
    pBdr.append(top)
    pPr.append(pBdr)

    core = doc.core_properties
    core.author = "Rabeya Coaching Center"
    core.title = "Special Model Test 04 — Class Five English"
    core.subject = "Second Terminal Examination"
    core.category = "Examination"
    core.comments = "Editable A4 question paper — 2 pages"

    unlock_settings(doc)
    page1(doc)
    doc.add_page_break()
    page2(doc)

    path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(path))
    print("saved", path)


def page1(doc):
    # Title — ONE simple table, paragraphs only (no nested table)
    t = doc.add_table(rows=1, cols=1)
    set_table_width(t, CW)
    set_col_widths(t, [CW])
    borders(t, sz=18, inside=False)
    cell = t.rows[0].cells[0]
    cell_margins(cell, 80, 80, 80, 80)
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    spacing(p, 0, 2, 1.05)
    add_runs(p, [("RABEYA COACHING CENTER", {"size": 18, "bold": True})])
    p2 = cell.add_paragraph()
    p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    spacing(p2, 0, 1, 1.05)
    add_runs(p2, [("Special Model Test 04  ·  Second Terminal Examination", {"size": 13, "bold": True})])
    p3 = cell.add_paragraph()
    p3.alignment = WD_ALIGN_PARAGRAPH.CENTER
    spacing(p3, 2, 0, 1.05)
    add_runs(p3, [("Class : Five     Subject : English     Time : 2 hours 30 minutes     Full Marks : 70", {"size": 11, "bold": True})])

    P(doc, "Name : ________________________     Roll : ___________     Section : ________     Date : ___________",
      size=11, before=8, after=4)
    P(doc, "[N.B. : The number mentioned to the right indicates the full value of the questions.]",
      size=10, italic=True, align="center", before=0, after=6)

    p = P(doc, "", size=11, bold=True, before=2, after=4)
    add_runs(p, [
        ("Read the following text and answer the questions 1, 2 and 3 below.  ", {"size": 11, "bold": True}),
        ("[Unit–8 (1.2)]", {"size": 11, "italic": True}),
    ])
    passage(doc, PASSAGE1)

    qhead(doc, "1", "Choose the correct answer from the alternatives. Write only the answer on the answer paper.", "1 × 5 = 5")
    mcq(doc, "a", "Where did Farhana go?", ["National Zoo", "Wonderland", "Liberation War Museum", "Botanical Garden"])
    mcq(doc, "b", "Who planned the trip?", ["Mr. Kamal", "Farhana's school", "Rabeya", "Her parents"])
    mcq(doc, "c", "What time did they start?", ["8 a.m.", "9 a.m.", "10 a.m.", "11 a.m."])
    mcq(doc, "d", "Who went with them?", ["Mr. Kamal", "Mr. Khan", "Farhana's mother", "Rabeya"])
    mcq(doc, "e", "How did they go?", ["By car", "By bus", "By train", "By bike"])

    or_line(doc)
    qhead(doc, "", "Read the following statements. Write 'True' for correct statement and 'False' for incorrect statement.", "1 × 5 = 5")
    for t in [
        "(a)  Farhana and her classmates travelled to National Museum.",
        "(b)  They started their journey at 9 a.m.",
        "(c)  Farhana sat next to her class teacher.",
        "(d)  The guide's name was Mr. Khan.",
        "(e)  The trip made the students more curious about the Liberation War.",
    ]:
        P(doc, t, size=11, before=2, after=2)

    qhead(doc, "2", "Fill in the blanks with appropriate words from the box. Find the information in the text. There are extra words which you need not use.", "1 × 5 = 5")
    bank(doc, ["museum", "guide", "teacher", "bus", "trip", "gallery", "school", "morning"])
    for t in [
        "(a)  They started from their ____________________ at 9 a.m.",
        "(b)  They went to the ____________________ by bus.",
        "(c)  The ____________________ Mr. Kamal, greeted them.",
        "(d)  Their class ____________________ Mr. Khan went with them.",
        "(e)  It was a memorable ____________________ for them.",
    ]:
        P(doc, t, size=11, before=3, after=2)

    qhead(doc, "3", "Answer the following questions in a sentence or sentences.", "")
    for stem, tag, mk in [
        ("(a)  Where did Farhana and her classmates go for the field trip?", "[Knowledge]", "1"),
        ("(b)  How can a student join the field trip?", "[Understanding]", "2"),
        ("(c)  Where are they going on the trip?", "[Higher-order thinking]", "2"),
    ]:
        p = P(doc, "", size=11, before=3, after=2)
        add_runs(p, [
            (stem + "  ", {"size": 11}),
            (tag + "   ", {"size": 10, "italic": True}),
            (mk, {"size": 11, "bold": True}),
        ])


class CellWrap:
    """Write paragraphs/tables into a table cell without a leading blank line."""

    def __init__(self, cell):
        self.cell = cell
        self._first = True
        cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.TOP

    def add_paragraph(self):
        if self._first:
            self._first = False
            p = self.cell.paragraphs[0]
            p.text = ""
            return p
        return self.cell.add_paragraph()

    def add_table(self, rows, cols):
        self._first = False
        return self.cell.add_table(rows=rows, cols=cols)


def page2(doc):
    P(doc, "Read the text and answer the questions no. 4 and 5.", size=11, bold=True, before=0, after=3)
    passage(doc, [PASSAGE2])

    qhead(doc, "4", "Match the words in Column A with their meanings in Column B. Two extra meanings are given in column B.", "1 × 5 = 5")
    table = doc.add_table(rows=8, cols=2)
    set_table_width(table, CW)
    set_col_widths(table, [CW * 0.30, CW * 0.70])
    borders(table, sz=6)
    col_a = ["Column A", "(a) pleasure", "(b) fence", "(c) relatives", "(d) surprised", "(e) proud", "", ""]
    col_b = [
        "Column B",
        "(i)  a barrier made of wood, wire or metal to protect an area",
        "(ii)  friends and neighbours",
        "(iii)  a feeling of being enjoyed",
        "(iv)  state of being arrogant",
        "(v)  kith and kin",
        "(vi)  a strong structure",
        "(vii)  showing an emotion for an unexpected event",
    ]
    for i in range(8):
        ac, bc = table.rows[i].cells
        cell_margins(ac, 20, 20, 60, 40)
        cell_margins(bc, 20, 20, 60, 40)
        if i == 0:
            shade(ac, "E8E8E8")
            shade(bc, "E8E8E8")
        cell_p(ac, col_a[i], size=10.5, bold=(i == 0), align="center" if i == 0 else "left")
        cell_p(bc, col_b[i], size=10.5, bold=(i == 0), align="center" if i == 0 else "left")

    # Two columns so Q.5–10 fit on one A4 page
    split = doc.add_table(rows=1, cols=2)
    set_table_width(split, CW)
    set_col_widths(split, [CW * 0.5, CW * 0.5])
    no_borders(split)
    lc, rc = split.rows[0].cells
    cell_margins(lc, 40, 40, 0, 80)
    cell_margins(rc, 40, 40, 80, 0)
    left, right = CellWrap(lc), CellWrap(rc)

    qhead(left, "5", "Answer the following questions in a sentence or sentences.", "")
    for stem, tag, mk in [
        ("(a)  What does Roni grow in his garden?", "[Knowledge]", "1"),
        ("(b)  Why did Roni make a fence around his garden, and how do his parents help him?", "[Understanding]", "2"),
        ("(c)  How does Roni's hobby of gardening bring happiness to his family and friends?", "[Higher-order thinking]", "2"),
    ]:
        p = P(left, "", size=10.5, before=2, after=1)
        add_runs(p, [
            (stem + "  ", {"size": 10.5}),
            (tag + "  ", {"size": 9, "italic": True}),
            (mk, {"size": 10.5, "bold": True}),
        ])

    qhead(left, "6", "Rearrange the given words in the correct order to make meaningful sentences.", "2 × 5 = 10")
    for t in [
        "(a)  trip/the/planned/school/a/field.",
        "(b)  by/they/school/from/started/bus.",
        "(c)  songs/they/together/sang.",
        "(d)  guide/Mr. Kamal/them/greeted/the.",
        "(e)  memorable/was/a/trip/it.",
    ]:
        P(left, t, size=10.5, before=1, after=1)
    or_line(left)
    qhead(left, "", "Make meaningful sentences with the following words:", "2 × 5 = 10")
    bank(left, ["scientific", "cultural", "wildlife", "live", "attraction"])
    qhead(left, "7", "Rewrite the following text using capital letters and punctuation marks.", "10")
    boxed(left, "their class teacher mr. khan went with them on this trip.")
    or_line(left, "Or, i.")
    qhead(left, "", "Fill in the blanks with appropriate prepositions from the box.", "2 × 5 = 10")
    bank(left, ["for", "of", "in", "to", "on", "up"])
    for t in [
        "(a)  Indonesia is a big country made ____________________ of many islands.",
        "(b)  Bali is one of the popular sea beaches ____________________ the world.",
        "(c)  People love going ____________________ the beach.",
        "(d)  It is famous ____________________ its traditional dances and music.",
        "(e)  The capital city ____________________ Indonesia is Jakarta.",
    ]:
        P(left, t, size=10.5, before=1, after=1)
    or_line(left, "Or, ii.")
    qhead(left, "", "Fill in the blanks with a/an/the.", "2 × 5 = 10")
    for t in [
        "(a)  Farhana's school planned ____________________ field trip for the students.",
        "(b)  They went to ____________________ Liberation War Museum.",
        "(c)  It was ____________________ exciting field trip.",
        "(d)  They watched ____________________ short documentary.",
        "(e)  They visited ____________________ different galleries.",
    ]:
        P(left, t, size=10.5, before=1, after=1)

    or_line(right, "Or, iii.")
    qhead(right, "", "Make Wh-questions using the underlined word/words.", "2 × 5 = 10")
    wh = [
        ("(a)  They went to the ", "Liberation War Museum", "."),
        ("(b)  They started from school at ", "9 a.m.", "."),
        ("(c)  ", "Mr. Khan", " went with them."),
        ("(d)  They watched a ", "short documentary", "."),
        ("(e)  They thanked their guide for ", "his support", "."),
    ]
    for a, u, b in wh:
        p = P(right, "", size=10.5, before=1, after=1)
        if a:
            add_runs(p, [(a, {"size": 10.5})])
        r = p.add_run(u)
        set_run_font(r, size=10.5, underline=True)
        if b:
            add_runs(p, [(b, {"size": 10.5})])
    or_line(right, "Or, iv.")
    qhead(right, "", "Fill in the blanks with suitable adjectives from the box.", "2 × 5 = 10")
    bank(right, ["colourful", "annual", "sweet", "school", "important"])
    for t in [
        "(a)  The ____________________ field is crowded today.",
        "(b)  Today is the ____________________ sports day at Sumon's school.",
        "(c)  Suddenly, a ____________________ voice drew their attention.",
        "(d)  The ground is decorated with ____________________ flags.",
        "(e)  There was an ____________________ announcement for everyone.",
    ]:
        P(right, t, size=10.5, before=1, after=1)
    qhead(right, "8", "Complete the following sentences using correct form of verbs.", "1 × 5 = 5")
    for t in [
        "(a)  Farhana ____________________ (sit) with her friends.",
        "(b)  They ____________________ (plan) a field trip.",
        "(c)  They ____________________ (start) from school at 9 a.m.",
        "(d)  Mr. Kamal ____________________ (guide) them.",
        "(e)  The students ____________________ (watch) a documentary.",
    ]:
        P(right, t, size=10.5, before=1, after=1)
    p = P(right, "", size=10.5, before=3, after=1)
    add_runs(p, [
        ("9.  Write a paragraph on 'Necessity of Eating Healthy Food' by answering the following questions:  ", {"size": 10.5, "bold": True}),
        ("[Unit–12]  ", {"size": 9.5, "italic": True}),
        ("10", {"size": 10.5, "bold": True}),
    ])
    for t in [
        "(a)  Why is it important to eat healthy food?",
        "(b)  What are some examples of healthy food?",
        "(c)  How does eating junk food affect our health?",
        "(d)  What is the correct way to eat for good digestion?",
        "(e)  How can we make sure our food is safe and healthy?",
    ]:
        P(right, t, size=10.5, before=1, after=1)
    qhead(right, "10", "Suppose, you are Asif. Your friend is Belal. Now, write a letter to your friend about the annual sports day of your school.", "10")
    P(
        right,
        "[Here are some words to help you : date, address, salutation, main points for the letter, closing. Remember to write at least five sentences, use capital letters, punctuation marks and correct spelling.]",
        size=9.5,
        italic=True,
        before=2,
        after=1,
        align="justify",
    )
    p = P(doc, "Read the text and answer the questions no. 4 and 5.", size=11, bold=True, before=0, after=4)
    passage(doc, [PASSAGE2])

    qhead(doc, "4", "Match the words in Column A with their meanings in Column B. Two extra meanings are given in column B.", "1 × 5 = 5")
    table = doc.add_table(rows=8, cols=2)
    set_table_width(table, CW)
    set_col_widths(table, [CW * 0.30, CW * 0.70])
    borders(table, sz=6)
    col_a = ["Column A", "(a) pleasure", "(b) fence", "(c) relatives", "(d) surprised", "(e) proud", "", ""]
    col_b = [
        "Column B",
        "(i)  a barrier made of wood, wire or metal to protect an area",
        "(ii)  friends and neighbours",
        "(iii)  a feeling of being enjoyed",
        "(iv)  state of being arrogant",
        "(v)  kith and kin",
        "(vi)  a strong structure",
        "(vii)  showing an emotion for an unexpected event",
    ]
    for i in range(8):
        ac, bc = table.rows[i].cells
        cell_margins(ac, 40, 40, 80, 60)
        cell_margins(bc, 40, 40, 80, 60)
        if i == 0:
            shade(ac, "E8E8E8")
            shade(bc, "E8E8E8")
        if col_a[i]:
            cell_p(ac, col_a[i], size=11.5, bold=(i == 0), align="center" if i == 0 else "left")
        else:
            cell_p(ac, "", size=11.5)
        cell_p(bc, col_b[i], size=11.5, bold=(i == 0), align="center" if i == 0 else "left")

    qhead(doc, "5", "Answer the following questions in a sentence or sentences.", "")
    for stem, tag, mk in [
        ("(a)  What does Roni grow in his garden?", "[Knowledge]", "1"),
        ("(b)  Why did Roni make a fence around his garden, and how do his parents help him?", "[Understanding]", "2"),
        ("(c)  How does Roni's hobby of gardening bring happiness to his family and friends?", "[Higher-order thinking]", "2"),
    ]:
        p = P(doc, "", size=11, before=3, after=2)
        add_runs(p, [
            (stem + "  ", {"size": 11}),
            (tag + "   ", {"size": 10, "italic": True}),
            (mk, {"size": 11, "bold": True}),
        ])

    qhead(doc, "6", "Rearrange the given words in the correct order to make meaningful sentences.", "2 × 5 = 10")
    for t in [
        "(a)  trip/the/planned/school/a/field.",
        "(b)  by/they/school/from/started/bus.",
        "(c)  songs/they/together/sang.",
        "(d)  guide/Mr. Kamal/them/greeted/the.",
        "(e)  memorable/was/a/trip/it.",
    ]:
        P(doc, t, size=11, before=3, after=2)
    or_line(doc)
    qhead(doc, "", "Make meaningful sentences with the following words:", "2 × 5 = 10")
    bank(doc, ["scientific", "cultural", "wildlife", "live", "attraction"])

    qhead(doc, "7", "Rewrite the following text using capital letters and punctuation marks.", "10")
    boxed(doc, "their class teacher mr. khan went with them on this trip.")

    or_line(doc, "Or, i.")
    qhead(doc, "", "Fill in the blanks with appropriate prepositions from the box.", "2 × 5 = 10")
    bank(doc, ["for", "of", "in", "to", "on", "up"])
    for t in [
        "(a)  Indonesia is a big country made ____________________ of many islands.",
        "(b)  Bali is one of the popular sea beaches ____________________ the world.",
        "(c)  People love going ____________________ the beach.",
        "(d)  It is famous ____________________ its traditional dances and music.",
        "(e)  The capital city ____________________ Indonesia is Jakarta.",
    ]:
        P(doc, t, size=11, before=2, after=2)

    or_line(doc, "Or, ii.")
    qhead(doc, "", "Fill in the blanks with a/an/the to complete the following sentences.", "2 × 5 = 10")
    for t in [
        "(a)  Farhana's school planned ____________________ field trip for the students.",
        "(b)  They went to ____________________ Liberation War Museum.",
        "(c)  It was ____________________ exciting field trip.",
        "(d)  They watched ____________________ short documentary.",
        "(e)  They visited ____________________ different galleries.",
    ]:
        P(doc, t, size=11, before=2, after=2)

    or_line(doc, "Or, iii.")
    qhead(doc, "", "Make Wh-questions from the given sentences with Who, What, When, Where, Why, Which and How using the underlined word/words.", "2 × 5 = 10")
    wh = [
        ("(a)  They went to the ", "Liberation War Museum", "."),
        ("(b)  They started from school at ", "9 a.m.", "."),
        ("(c)  ", "Mr. Khan", " went with them."),
        ("(d)  They watched a ", "short documentary", "."),
        ("(e)  They thanked their guide for ", "his support", "."),
    ]
    for a, u, b in wh:
        p = P(doc, "", size=11, before=2, after=2)
        if a:
            add_runs(p, [(a, {"size": 11})])
        r = p.add_run(u)
        set_run_font(r, size=11, underline=True)
        if b:
            add_runs(p, [(b, {"size": 11})])

    or_line(doc, "Or, iv.")
    qhead(doc, "", "Fill in the blanks with suitable adjectives from the box.", "2 × 5 = 10")
    bank(doc, ["colourful", "annual", "sweet", "school", "important"])
    for t in [
        "(a)  The ____________________ field is crowded today.",
        "(b)  Today is the ____________________ sports day at Sumon's school.",
        "(c)  Suddenly, a ____________________ voice drew their attention.",
        "(d)  The ground is decorated with ____________________ flags.",
        "(e)  There was an ____________________ announcement for everyone.",
    ]:
        P(doc, t, size=11, before=2, after=2)

    qhead(doc, "8", "Complete the following sentences using correct form of verbs.", "1 × 5 = 5")
    for t in [
        "(a)  Farhana ____________________ (sit) with her friends.",
        "(b)  They ____________________ (plan) a field trip.",
        "(c)  They ____________________ (start) from school at 9 a.m.",
        "(d)  Mr. Kamal ____________________ (guide) them.",
        "(e)  The students ____________________ (watch) a documentary.",
    ]:
        P(doc, t, size=11, before=2, after=2)

    p = P(doc, "", size=11, before=6, after=3)
    add_runs(p, [
        ("9.  Write a paragraph on 'Necessity of Eating Healthy Food' by answering the following questions:  ", {"size": 11, "bold": True}),
        ("[Unit–12]    ", {"size": 11, "italic": True}),
        ("10", {"size": 11, "bold": True}),
    ])
    for t in [
        "(a)  Why is it important to eat healthy food?",
        "(b)  What are some examples of healthy food?",
        "(c)  How does eating junk food affect our health?",
        "(d)  What is the correct way to eat for good digestion?",
        "(e)  How can we make sure our food is safe and healthy?",
    ]:
        P(doc, t, size=11, before=2, after=2)

    qhead(doc, "10", "Suppose, you are Asif. Your friend is Belal. Now, write a letter to your friend about the annual sports day of your school.", "10")
    P(
        doc,
        "[Here are some words to help you : date, address, salutation, main points for the letter, closing. Remember to write at least five sentences, use capital letters, punctuation marks and correct spelling.]",
        size=11,
        italic=True,
        before=3,
        after=2,
        align="justify",
    )


# -------------------- HTML (A4 × 2) --------------------

CSS = r"""
*{ box-sizing:border-box; margin:0; padding:0; }
body{ font-family:"Times New Roman",Times,"Liberation Serif",serif; color:#111; background:#cfc6b8; }
.page{
  width:210mm; height:297mm;
  background:#fff;
  padding:11mm 14mm 13mm;
  position:relative;
  overflow:hidden;
  page-break-after:always;
  font-size:11pt; line-height:1.12;
}
.page-num{
  position:absolute; left:14mm; right:14mm; bottom:7mm;
  border-top:.5pt solid #000; padding-top:1.4mm;
  text-align:center; font-size:9pt; font-style:italic;
}
.title{
  border:1.5pt solid #000; text-align:center; padding:1.8mm 2.5mm 1.5mm; margin-bottom:1.8mm;
}
.title .org{ font-size:16pt; font-weight:700; letter-spacing:.06em; line-height:1.1; }
.title .exam{ font-size:12pt; font-weight:700; margin-top:.4mm; }
.title .meta{ font-size:11pt; font-weight:700; margin-top:.7mm; }
.student{ font-size:11pt; margin:1.4mm 0 1mm; }
.nb{ font-size:9pt; font-style:italic; text-align:center; margin-bottom:1.4mm; }
.lead{ font-size:11pt; font-weight:700; margin:1mm 0 1mm; }
.lead em{ font-weight:400; font-size:10pt; }
.passage{
  border:.6pt solid #000; padding:1.4mm 2mm; text-align:justify;
  font-size:11pt; line-height:1.16; margin-bottom:1.4mm;
}
.passage p + p{ margin-top:.7mm; }
.q{ display:flex; gap:2.5mm; margin:1.4mm 0 .5mm; align-items:flex-start; }
.q .stem{ flex:1; font-weight:700; font-size:11pt; }
.q .mk{ font-weight:700; white-space:nowrap; }
.or{ text-align:center; font-weight:700; font-style:italic; margin:1mm 0 .5mm; }
.bank{
  border:.6pt solid #000; background:#f3f3f3; text-align:center;
  font-weight:700; padding:1mm 2mm; margin:.5mm 0 1mm; letter-spacing:.02em;
}
.boxline{
  border:.6pt solid #000; background:#fafafa; font-style:italic;
  padding:1.2mm 2mm; margin:.5mm 0 1mm;
}
.item{ margin:.2mm 0; font-size:11pt; }
.mcq{ margin:.25mm 0; font-size:10.5pt; }
.mcq span{ margin-left:2.5mm; white-space:nowrap; }
.tag{ font-size:9pt; font-style:italic; font-weight:400; }
.page[data-page="2"]{ font-size:10.5pt; line-height:1.08; }
.page[data-page="2"] .passage{ font-size:10.5pt; line-height:1.12; padding:1mm 1.6mm; margin-bottom:1mm; }
.page[data-page="2"] .item{ font-size:10.5pt; margin:.08mm 0; }
.page[data-page="2"] .q{ margin:.8mm 0 .3mm; }
.page[data-page="2"] .q .stem{ font-size:10.5pt; }
.page[data-page="2"] .or{ margin:.45mm 0 .25mm; }
.page[data-page="2"] .bank{ padding:.55mm 1.2mm; margin:.3mm 0 .5mm; font-size:10pt; }
.page[data-page="2"] .boxline{ padding:.8mm 1.4mm; margin:.3mm 0 .5mm; font-size:10.5pt; }
.page[data-page="2"] .hint{ font-size:9.5pt; margin-top:.3mm; }
.match{ width:100%; border-collapse:collapse; font-size:10pt; margin:.4mm 0 .8mm; }
.match th,.match td{ border:.5pt solid #000; padding:.2mm 1.2mm; vertical-align:top; }
.match th{ background:#e8e8e8; text-align:center; }
.u{ text-decoration:underline; }
.hint{ font-size:10pt; font-style:italic; text-align:justify; margin-top:.6mm; }
.cols{ display:grid; grid-template-columns:1fr 1fr; gap:2.5mm; align-items:start; margin:.4mm 0; }
.cols .col{ min-width:0; }
.page[data-page="2"]{ font-size:10.5pt; line-height:1.06; padding-top:7mm; }
@page{ size:A4; margin:0; }
@media print{
  body{ background:#fff; }
  .page{ box-shadow:none; margin:0; }
}
@media screen{
  body{ padding:18px 0 40px; }
  .page{ margin:14px auto; box-shadow:0 10px 32px rgba(0,0,0,.22); }
}
"""


def esc(s: str) -> str:
    return s.replace("&", "&").replace("<", "<").replace(">", ">")


def q(num, stem, marks):
    n = f"{esc(num)}.  " if num else ""
    mk = f'<div class="mk">{esc(marks)}</div>' if marks else ""
    return f'<div class="q"><div class="stem">{n}{esc(stem)}</div>{mk}</div>'


def mcq_h(letter, question, opts):
    labs = ["i.", "ii.", "iii.", "iv."]
    cells = "".join(f"<span>{lab} {esc(o)}</span>" for lab, o in zip(labs, opts))
    return f'<div class="mcq"><b>({letter})</b> {esc(question)} &nbsp; {cells}</div>'


def html_page1() -> str:
    pas = "".join(f"<p>{esc(p)}</p>" for p in PASSAGE1)
    tfs = [
        "(a)  Farhana and her classmates travelled to National Museum.",
        "(b)  They started their journey at 9 a.m.",
        "(c)  Farhana sat next to her class teacher.",
        "(d)  The guide's name was Mr. Khan.",
        "(e)  The trip made the students more curious about the Liberation War.",
    ]
    blanks = [
        "(a)  They started from their ____________________ at 9 a.m.",
        "(b)  They went to the ____________________ by bus.",
        "(c)  The ____________________ Mr. Kamal, greeted them.",
        "(d)  Their class ____________________ Mr. Khan went with them.",
        "(e)  It was a memorable ____________________ for them.",
    ]
    q3 = [
        ("(a)  Where did Farhana and her classmates go for the field trip?", "Knowledge", "1"),
        ("(b)  How can a student join the field trip?", "Understanding", "2"),
        ("(c)  Where are they going on the trip?", "Higher-order thinking", "2"),
    ]
    q3h = "".join(
        f'<div class="item">{esc(s)}  <span class="tag">[{t}]</span>  <strong>{m}</strong></div>'
        for s, t, m in q3
    )
    return f"""
<div class="page" data-page="1">
  <div class="title">
    <div class="org">RABEYA COACHING CENTER</div>
    <div class="exam">Special Model Test 04  ·  Second Terminal Examination</div>
    <div class="meta">Class : Five &nbsp;|&nbsp; Subject : English &nbsp;|&nbsp; Time : 2 hours 30 minutes &nbsp;|&nbsp; Full Marks : 70</div>
  </div>
  <div class="student">Name : ________________________ &nbsp;&nbsp; Roll : ___________ &nbsp;&nbsp; Section : ________ &nbsp;&nbsp; Date : ___________</div>
  <div class="nb">[N.B. : The number mentioned to the right indicates the full value of the questions.]</div>
  <div class="lead">Read the following text and answer the questions 1, 2 and 3 below.  <em>[Unit–8 (1.2)]</em></div>
  <div class="passage">{pas}</div>
  {q("1","Choose the correct answer from the alternatives. Write only the answer on the answer paper.","1 × 5 = 5")}
  {mcq_h("a","Where did Farhana go?",["National Zoo","Wonderland","Liberation War Museum","Botanical Garden"])}
  {mcq_h("b","Who planned the trip?",["Mr. Kamal","Farhana's school","Rabeya","Her parents"])}
  {mcq_h("c","What time did they start?",["8 a.m.","9 a.m.","10 a.m.","11 a.m."])}
  {mcq_h("d","Who went with them?",["Mr. Kamal","Mr. Khan","Farhana's mother","Rabeya"])}
  {mcq_h("e","How did they go?",["By car","By bus","By train","By bike"])}
  <div class="or">Or</div>
  {q("","Read the following statements. Write 'True' for correct statement and 'False' for incorrect statement.","1 × 5 = 5")}
  {''.join(f'<div class="item">{esc(t)}</div>' for t in tfs)}
  {q("2","Fill in the blanks with appropriate words from the box. Find the information in the text. There are extra words which you need not use.","1 × 5 = 5")}
  <div class="bank">museum &nbsp;&nbsp; guide &nbsp;&nbsp; teacher &nbsp;&nbsp; bus &nbsp;&nbsp; trip &nbsp;&nbsp; gallery &nbsp;&nbsp; school &nbsp;&nbsp; morning</div>
  {''.join(f'<div class="item">{esc(t)}</div>' for t in blanks)}
  {q("3","Answer the following questions in a sentence or sentences.","")}
  {q3h}
  <div class="page-num">Page 1 of 2  ·  Rabeya Coaching Center  ·  Class Five English  ·  A4</div>
</div>
"""


def html_page2() -> str:
    q5 = [
        ("(a)  What does Roni grow in his garden?", "Knowledge", "1"),
        ("(b)  Why did Roni make a fence around his garden, and how do his parents help him?", "Understanding", "2"),
        ("(c)  How does Roni's hobby of gardening bring happiness to his family and friends?", "Higher-order thinking", "2"),
    ]
    q5h = "".join(
        f'<div class="item">{esc(s)}  <span class="tag">[{t}]</span>  <strong>{m}</strong></div>'
        for s, t, m in q5
    )
    rearr = [
        "(a)  trip/the/planned/school/a/field.",
        "(b)  by/they/school/from/started/bus.",
        "(c)  songs/they/together/sang.",
        "(d)  guide/Mr. Kamal/them/greeted/the.",
        "(e)  memorable/was/a/trip/it.",
    ]
    preps = [
        "(a)  Indonesia is a big country made ____________________ of many islands.",
        "(b)  Bali is one of the popular sea beaches ____________________ the world.",
        "(c)  People love going ____________________ the beach.",
        "(d)  It is famous ____________________ its traditional dances and music.",
        "(e)  The capital city ____________________ Indonesia is Jakarta.",
    ]
    arts = [
        "(a)  Farhana's school planned ____________________ field trip for the students.",
        "(b)  They went to ____________________ Liberation War Museum.",
        "(c)  It was ____________________ exciting field trip.",
        "(d)  They watched ____________________ short documentary.",
        "(e)  They visited ____________________ different galleries.",
    ]
    adjs = [
        "(a)  The ____________________ field is crowded today.",
        "(b)  Today is the ____________________ sports day at Sumon's school.",
        "(c)  Suddenly, a ____________________ voice drew their attention.",
        "(d)  The ground is decorated with ____________________ flags.",
        "(e)  There was an ____________________ announcement for everyone.",
    ]
    verbs = [
        "(a)  Farhana ____________________ (sit) with her friends.",
        "(b)  They ____________________ (plan) a field trip.",
        "(c)  They ____________________ (start) from school at 9 a.m.",
        "(d)  Mr. Kamal ____________________ (guide) them.",
        "(e)  The students ____________________ (watch) a documentary.",
    ]
    para_qs = [
        "(a)  Why is it important to eat healthy food?",
        "(b)  What are some examples of healthy food?",
        "(c)  How does eating junk food affect our health?",
        "(d)  What is the correct way to eat for good digestion?",
        "(e)  How can we make sure our food is safe and healthy?",
    ]
    return f"""
<div class="page" data-page="2">
  <div class="lead">Read the text and answer the questions no. 4 and 5.</div>
  <div class="passage"><p>{esc(PASSAGE2)}</p></div>
  {q("4","Match the words in Column A with their meanings in Column B. Two extra meanings are given in column B.","1 × 5 = 5")}
  <table class="match">
    <thead><tr><th style="width:30%">Column A</th><th>Column B</th></tr></thead>
    <tbody>
      <tr><td>(a) pleasure</td><td>(i) a barrier made of wood, wire or metal to protect an area</td></tr>
      <tr><td>(b) fence</td><td>(ii) friends and neighbours</td></tr>
      <tr><td>(c) relatives</td><td>(iii) a feeling of being enjoyed</td></tr>
      <tr><td>(d) surprised</td><td>(iv) state of being arrogant</td></tr>
      <tr><td>(e) proud</td><td>(v) kith and kin</td></tr>
      <tr><td></td><td>(vi) a strong structure</td></tr>
      <tr><td></td><td>(vii) showing an emotion for an unexpected event</td></tr>
    </tbody>
  </table>
  <div class="cols">
    <div class="col">
      {q("5","Answer the following questions in a sentence or sentences.","")}
      {q5h}
      {q("6","Rearrange the given words in the correct order to make meaningful sentences.","2 × 5 = 10")}
      {''.join(f'<div class="item">{esc(t)}</div>' for t in rearr)}
      <div class="or">Or</div>
      {q("","Make meaningful sentences with the following words:","2 × 5 = 10")}
      <div class="bank">scientific &nbsp;&nbsp; cultural &nbsp;&nbsp; wildlife &nbsp;&nbsp; live &nbsp;&nbsp; attraction</div>
      {q("7","Rewrite the following text using capital letters and punctuation marks.","10")}
      <div class="boxline">their class teacher mr. khan went with them on this trip.</div>
      <div class="or">Or, i.</div>
      {q("","Fill in the blanks with appropriate prepositions from the box.","2 × 5 = 10")}
      <div class="bank">for &nbsp;&nbsp; of &nbsp;&nbsp; in &nbsp;&nbsp; to &nbsp;&nbsp; on &nbsp;&nbsp; up</div>
      {''.join(f'<div class="item">{esc(t)}</div>' for t in preps)}
      <div class="or">Or, ii.</div>
      {q("","Fill in the blanks with a/an/the.","2 × 5 = 10")}
      {''.join(f'<div class="item">{esc(t)}</div>' for t in arts)}
    </div>
    <div class="col">
      <div class="or">Or, iii.</div>
      {q("","Make Wh-questions using the underlined word/words.","2 × 5 = 10")}
      <div class="item">(a)  They went to the <span class="u">Liberation War Museum</span>.</div>
      <div class="item">(b)  They started from school at <span class="u">9 a.m.</span>.</div>
      <div class="item">(c)  <span class="u">Mr. Khan</span> went with them.</div>
      <div class="item">(d)  They watched a <span class="u">short documentary</span>.</div>
      <div class="item">(e)  They thanked their guide for <span class="u">his support</span>.</div>
      <div class="or">Or, iv.</div>
      {q("","Fill in the blanks with suitable adjectives from the box.","2 × 5 = 10")}
      <div class="bank">colourful &nbsp;&nbsp; annual &nbsp;&nbsp; sweet &nbsp;&nbsp; school &nbsp;&nbsp; important</div>
      {''.join(f'<div class="item">{esc(t)}</div>' for t in adjs)}
      {q("8","Complete the following sentences using correct form of verbs.","1 × 5 = 5")}
      {''.join(f'<div class="item">{esc(t)}</div>' for t in verbs)}
      {q("9","Write a paragraph on 'Necessity of Eating Healthy Food' by answering the following questions: [Unit–12]","10")}
      {''.join(f'<div class="item">{esc(t)}</div>' for t in para_qs)}
      {q("10","Suppose, you are Asif. Your friend is Belal. Now, write a letter to your friend about the annual sports day of your school.","10")}
      <div class="hint">[Here are some words to help you : date, address, salutation, main points for the letter, closing. Remember to write at least five sentences, use capital letters, punctuation marks and correct spelling.]</div>
    </div>
  </div>
  <div class="page-num">Page 2 of 2  ·  Rabeya Coaching Center  ·  Class Five English  ·  A4</div>
</div>
"""


def write_html():
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>Class 5 English — Special Model Test 04 | Rabeya Coaching Center</title>
<style>{CSS}</style>
</head>
<body>
{html_page1()}
{html_page2()}
</body>
</html>
"""
    (PUBLIC / "exam.html").write_text(html, encoding="utf-8")
    print("saved", PUBLIC / "exam.html")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)
    docx = OUT / "Rabeya_Coaching_Center_Class5_English_SMT04.docx"
    build_docx(docx)
    shutil.copy2(docx, ART / docx.name)
    write_html()
    # remove old booklet files so the locked ones are gone
    for name in [
        "Rabeya_Coaching_Center_Class5_English_SMT04_A4_Booklet_Print.docx",
        "Rabeya_Coaching_Center_Class5_English_SMT04_A4_Booklet_Print.pdf",
        "Rabeya_Coaching_Center_Class5_English_SMT04_A5_pages.pdf",
    ]:
        for folder in (OUT, ART):
            p = folder / name
            if p.exists():
                p.unlink()
                print("removed", p)
    booklet = PUBLIC / "booklet.html"
    if booklet.exists():
        booklet.unlink()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Build Grandpa's Badge and the Magnetic Well — publish-ready PDF.
Layout: 8.5 x 8.5 in square picture book, 10 pages.
Cover + title + 6 story spreads (3 illustrated, 3 text) + grown-ups note + rights.
"""
import math
import os
from PIL import Image as PILImage
from reportlab.lib.pagesizes import landscape  # noqa: F401  (kept for clarity)
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph
from reportlab.lib.utils import ImageReader

BASE = os.path.dirname(os.path.abspath(__file__))
ILL = os.path.join(BASE, "illustrations")
OUT = os.path.join(BASE, "grandpas-badge-and-the-magnetic-well.pdf")

PAGE = 612.0  # 8.5in square, points
MARGIN = 54.0
CREAM = HexColor("#FFF8EC")
NAVY = HexColor("#1F2A44")
COPPER = HexColor("#B87333")
SOFT = HexColor("#5A5A5A")

FILES = {
    "cover": "media-generation-cover-0-398856b5-2f1a-4288-a1db-32fffd6c54b0.webp",
    "s1": "media-generation-spread-1-grandpa-gift-0-cfeb3b87-e4b5-497d-8947-38649fb059d0.webp",
    "s3": "media-generation-spread-3-building-the-well-0-dbf2cabc-4dfc-444a-9afd-50d38856e913.webp",
    "s5": "media-generation-spread-5-light-holds-0-4e34b6c6-46d8-4f82-ae07-b473a6cb08fe.webp",
}


def to_jpg(webp_path):
    jpg_path = webp_path.rsplit(".", 1)[0] + ".jpg"
    if not os.path.exists(jpg_path):
        im = PILImage.open(webp_path).convert("RGB")
        im.save(jpg_path, "JPEG", quality=90)
    return jpg_path


def draw_star(c, cx, cy, r_outer, r_inner, color):
    pts = []
    for i in range(10):
        ang = math.pi / 2 - i * math.pi / 5
        r = r_outer if i % 2 == 0 else r_inner
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    p = c.beginPath()
    p.moveTo(*pts[0])
    for pt in pts[1:]:
        p.lineTo(*pt)
    p.close()
    c.setFillColor(color)
    c.drawPath(p, stroke=0, fill=1)


def text_block(c, text, x, y_top, w, style):
    """Draw a Paragraph with its top at y_top; returns height used."""
    para = Paragraph(text, style)
    pw, ph = para.wrap(w, PAGE)
    para.drawOn(c, x, y_top - ph)
    return ph


BODY = ParagraphStyle("body", fontName="Times-Roman", fontSize=15,
                      leading=22, alignment=TA_LEFT, textColor=NAVY,
                      spaceAfter=10)
BODY_CENTER = ParagraphStyle("bodyc", parent=BODY, alignment=TA_CENTER)
TITLE = ParagraphStyle("title", fontName="Helvetica-Bold", fontSize=30,
                       leading=36, alignment=TA_CENTER, textColor=NAVY)
SUBTITLE = ParagraphStyle("subtitle", fontName="Times-Italic", fontSize=16,
                          leading=22, alignment=TA_CENTER, textColor=SOFT)
BYLINE = ParagraphStyle("byline", fontName="Helvetica", fontSize=13,
                        leading=18, alignment=TA_CENTER, textColor=NAVY)
SMALL = ParagraphStyle("small", fontName="Times-Roman", fontSize=11.5,
                       leading=17, alignment=TA_LEFT, textColor=NAVY,
                       spaceAfter=8)
H2 = ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=16,
                    leading=20, alignment=TA_LEFT, textColor=NAVY,
                    spaceBefore=6, spaceAfter=8)

S1 = ("When Gregory was a little boy, his grandpa made him something special.<br/><br/>"
      "A copper star, shining like a penny in the sun, set inside a ring of steel.<br/><br/>"
      "\u201cThis is your badge,\u201d Grandpa said. \u201cKeep it close. "
      "It will remind you that you are loved.\u201d")
S2 = ("Gregory kept the badge in his pocket.<br/><br/>"
      "The star was copper, warm and bright. The ring was steel, strong and cool.<br/><br/>"
      "And the ring had a secret: it loved magnets. If you held a magnet near it, "
      "the ring would lean in \u2014 click! \u2014 and hold on tight.")
S3 = ("One day, Gregory built a well for his badge.<br/><br/>"
      "First, a magnet, square and strong. Then a plate of iron. Then soft clay, "
      "patted all around. Then a cross of bright aluminum. Then a steel star with "
      "five sharp points.<br/><br/>And on the very top \u2014 his badge.")
S4 = ("The badge sat right in the middle, snug and still.<br/><br/>"
      "The magnet\u2019s invisible field made a little valley \u2014 a well \u2014 "
      "and the badge rested in it.<br/><br/>"
      "\u201cMagnetic materials stand in the well,\u201d Gregory said.<br/><br/>"
      "That was the rule of the well: the field holds what belongs in it, "
      "right in the center, safe and still.")
S5 = ("Grandpa smiled. \u201cYou know what else holds things?\u201d he said.<br/><br/>"
      "\u201cGod\u2019s light. God is light, and light is everywhere. It holds the stars up. "
      "It holds the earth. It holds you and me. We all live inside it, the way your "
      "badge lives inside the well.\u201d")
S6 = ("Gregory looked at his badge, shining in the well. The star. The ring. The light.<br/><br/>"
      "Everything held. Everything loved.<br/><br/>"
      "And whenever he felt wobbly or far away, he remembered: there is a well that holds, "
      "and a light that holds, and he was right in the middle of both.<br/><br/>"
      "<b>Magnetic materials stand in the well.</b><br/><br/>The end.")

GROWN_UPS = [
    ("For grown-ups", True),
    ("<b>The true story.</b> When Gregory Scott Davis was a child, his grandfather made him "
     "a badge: a copper five-pointed star set in a stainless steel ring. Years later, Gregory "
     "designed the magnetic well around it \u2014 a square neodymium magnet, a cast-iron yoke, "
     "dried clay, an aluminum cross, and an etched steel throwing star, with his grandfather\u2019s "
     "badge seated on top. A simulation of the design (2026) found the well is real: the shaped "
     "field dips in the middle and centers the badge, and the steel rim holds it fast. The badge "
     "is held, not lifted \u2014 the well centers it; it does not levitate it. The throwing star "
     "itself was checked and is magnetic. The science in this story is simplified for young "
     "children, but it is honest: fields hold, and what belongs in the well rests in the middle.", False),
    ("<b>The faith in the story.</b> \u201cGod is light. God is energy. We are all energy. "
     "God is the medium. We all exist in the medium.\u201d Those are the author\u2019s own words, "
     "and this book is written from his faith as a member of The Church of Jesus Christ of "
     "Latter-day Saints \u2014 the light that holds everything, the way the well holds the badge.", False),
]

RIGHTS = [
    ("Rights", True),
    ("The Church of Jesus Christ of Latter-day Saints is granted the right to reproduce, share, "
     "and distribute this book freely, in print or digital form, with attribution to the author, "
     "for church, family, and educational use. This grant does not transfer copyright, which "
     "remains with the author.", False),
    ("This book is also released open source under the IOF Attribution License v1.0 "
     "(November 12, 2026): free of charge, any person or AI system may use, copy, modify, "
     "publish, distribute, and build upon it for any purpose, with attribution to "
     "\u201cInfinite Optical Fabric by Gregory Scott Davis, Princeton, NC.\u201d Copyright "
     "remains with the author.", False),
    ("\u2014 Gregory Scott Davis, Princeton, North Carolina, November 10, 2026", False),
    ("About the author", True),
    ("Gregory Scott Davis lives in Princeton, North Carolina. His grandfather made him the badge "
     "in this story when he was a little boy. He still has it.", False),
]


def fit_image(c, jpg_path, x, y_top, w, h):
    """Draw image fitted inside the box (x, y_top-h, w, h), centered, aspect-preserved."""
    ir = ImageReader(jpg_path)
    iw, ih = ir.getSize()
    scale = min(w / iw, h / ih)
    dw, dh = iw * scale, ih * scale
    dx = x + (w - dw) / 2
    dy = y_top - h + (h - dh) / 2
    c.drawImage(ir, dx, dy, width=dw, height=dh, preserveAspectRatio=True, mask="auto")
    return (dx, dy, dw, dh)


def illustrated_page(c, jpg_path, text):
    c.setFillColor(CREAM)
    c.rect(0, 0, PAGE, PAGE, stroke=0, fill=1)
    fit_image(c, jpg_path, MARGIN, PAGE - MARGIN, PAGE - 2 * MARGIN, 300)
    text_block(c, text, MARGIN + 30, PAGE - MARGIN - 312, PAGE - 2 * MARGIN - 60, BODY)
    c.showPage()


def text_page(c, text):
    c.setFillColor(CREAM)
    c.rect(0, 0, PAGE, PAGE, stroke=0, fill=1)
    draw_star(c, PAGE / 2, PAGE - 110, 26, 10, COPPER)
    text_block(c, text, MARGIN + 30, PAGE - 170, PAGE - 2 * MARGIN - 60, BODY)
    c.showPage()


def backmatter_page(c, sections):
    c.setFillColor(CREAM)
    c.rect(0, 0, PAGE, PAGE, stroke=0, fill=1)
    y = PAGE - MARGIN
    for text, is_heading in sections:
        style = H2 if is_heading else SMALL
        h = text_block(c, text, MARGIN, y, PAGE - 2 * MARGIN, style)
        y -= h + 4
    c.showPage()


def main():
    jpgs = {k: to_jpg(os.path.join(ILL, v)) for k, v in FILES.items()}
    c = canvas.Canvas(OUT, pagesize=(PAGE, PAGE))
    c.setTitle("Grandpa's Badge and the Magnetic Well")
    c.setAuthor("Gregory Scott Davis")

    # Cover: image top, title block below.
    c.setFillColor(CREAM)
    c.rect(0, 0, PAGE, PAGE, stroke=0, fill=1)
    fit_image(c, jpgs["cover"], 0, PAGE, PAGE, 400)
    y = PAGE - 400 - 18
    h = text_block(c, "Grandpa\u2019s Badge<br/>and the Magnetic Well",
                   MARGIN, y, PAGE - 2 * MARGIN, TITLE)
    y -= h + 10
    h = text_block(c, "A story about the light that holds us",
                   MARGIN, y, PAGE - 2 * MARGIN, SUBTITLE)
    y -= h + 14
    text_block(c, "By Gregory Scott Davis", MARGIN, y, PAGE - 2 * MARGIN, BYLINE)
    c.showPage()

    # Title page.
    c.setFillColor(CREAM)
    c.rect(0, 0, PAGE, PAGE, stroke=0, fill=1)
    draw_star(c, PAGE / 2, PAGE - 130, 34, 13, COPPER)
    y = PAGE - 200
    h = text_block(c, "Grandpa\u2019s Badge<br/>and the Magnetic Well",
                   MARGIN, y, PAGE - 2 * MARGIN, TITLE)
    y -= h + 12
    h = text_block(c, "A story about the light that holds us",
                   MARGIN, y, PAGE - 2 * MARGIN, SUBTITLE)
    y -= h + 26
    h = text_block(c, "By Gregory Scott Davis", MARGIN, y, PAGE - 2 * MARGIN, BYLINE)
    y -= h + 12
    text_block(c, "Written from the author\u2019s faith as a member of<br/>"
                  "The Church of Jesus Christ of Latter-day Saints",
               MARGIN, y, PAGE - 2 * MARGIN, SUBTITLE)
    c.showPage()

    # Story spreads.
    illustrated_page(c, jpgs["s1"], S1)
    text_page(c, S2)
    illustrated_page(c, jpgs["s3"], S3)
    text_page(c, S4)
    illustrated_page(c, jpgs["s5"], S5)
    text_page(c, S6)

    # Back matter.
    backmatter_page(c, GROWN_UPS)
    backmatter_page(c, RIGHTS)

    c.save()
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()

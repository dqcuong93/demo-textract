from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas

overlay_pdf_file_name = "overlay_PDF.pdf"
pdf_template_file_name = "base_PDF_template.pdf"
# pdf_template_file_name = "base_PDF_template_rotated.pdf"
result_pdf_file_name = "final_PDF.pdf"
FONT_NAME = "Courier"
FONT_SIZE = 17
TEXT = "Dan"
BOUNDING_BOX_WIDTH = 137.63074378967283
BOUNDING_BOX_HEIGHT = 39.03012784838676
START_X = 49.51413624286651
START_Y = 29.64576608777046
END_Y = 717.9942339122296


def calculate_fontsize(text, bb_width):
    """
    Input:
        text: content of a line
        bb_width: the width of BoundingBox
    Return a suitable fontsize."""
    fontsize = FONT_SIZE
    text_width = pdfmetrics.stringWidth(text, FONT_NAME, fontsize)
    if text_width > bb_width:
        while text_width > bb_width:
            fontsize -= 0.5
            text_width = pdfmetrics.stringWidth(text, FONT_NAME, fontsize)
    elif text_width < bb_width:
        while text_width < bb_width:
            fontsize += 0.5
            text_width = pdfmetrics.stringWidth(text, FONT_NAME, fontsize)
    return fontsize


font_size = calculate_fontsize(text=TEXT, bb_width=BOUNDING_BOX_WIDTH)

# create a new PDF with Reportlab
can = canvas.Canvas(filename=overlay_pdf_file_name, pagesize=(578.4, 824.64))

textobject = can.beginText(START_X, END_Y)
textobject.setFont(FONT_NAME, font_size)
textobject.textOut(TEXT)
can.drawText(textobject)
can.save()

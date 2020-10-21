from PyPDF2 import PdfFileReader, PdfFileWriter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas

overlay_pdf_file_name = "overlay_PDF.pdf"
pdf_template_file_name = "base_PDF_template.pdf"
# pdf_template_file_name = "base_PDF_template_rotated.pdf"
result_pdf_file_name = "final_PDF.pdf"
FONT_NAME = "Courier"
FONT_SIZE = 17
TEXT = "Tuesday, August 11, 2020"
BOUNDING_BOX_WIDTH = 120.61135243177414
BOUNDING_BOX_HEIGHT = 11.081987231075763
START_X = 433.0115837574005
START_Y = 174.90205139636993
END_Y = 641.73794860363


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

# Take the PDF you created above and overlay it on your template PDF
# Open your template PDF
pdf_template = PdfFileReader(open(pdf_template_file_name, "rb"))

# Get the first page from the template
template_page = pdf_template.getPage(0)

# Open your overlay PDF that was created earlier
overlay_pdf = PdfFileReader(open(overlay_pdf_file_name, "rb"))

# Merge the overlay page onto the template page
template_page.mergePage(overlay_pdf.getPage(0))

# Write the result to a new PDF file
output_pdf = PdfFileWriter()
output_pdf.addPage(template_page)
output_pdf.write(open(result_pdf_file_name, "wb"))

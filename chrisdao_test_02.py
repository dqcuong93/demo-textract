from pprint import pprint

import PyPDF2
from PyPDF2 import PdfFileReader


def walk(my_object, font, embedded_font):
    """
    If there is a key called 'BaseFont', that is a font that is used in the document.
    If there is a key called 'FontName' and another key in the same dictionary my_object
    that is called 'FontFilex' (where x is null, 2, or 3), then that font name is
    embedded.

    We create and add to two sets, fnt = fonts used and emb = fonts embedded_font.
    """
    if not hasattr(my_object, "keys"):
        return None, None

    font_keys = set(["/FontFile", "/FontFile2", "/FontFile3"])

    if "/BaseFont" in my_object:
        font.add(my_object["/BaseFont"])
    if "/FontName" in my_object:
        if [x for x in font_keys if x in my_object]:  # test to see if there is FontFile
            embedded_font.add(my_object["/FontName"])

    for k in my_object.keys():
        walk(my_object[k], font, embedded_font)

    return font, embedded_font  # return the sets for each page


if __name__ == "__main__":
    fname = "2020 Payment - Mazda Temporary Vehicle Registration.pdf"  # Change this to the file name you want
    pdf = PdfFileReader(fname)
    fonts = set()
    embedded = set()
    for page in pdf.pages:
        obj = page.getObject()

        if type(obj) == PyPDF2.generic.ArrayObject:
            for i in obj:
                if hasattr(i, "keys"):
                    f, e = walk(i, fonts, embedded)
                    fonts = fonts.union(f)
                    embedded = embedded.union(e)
        else:
            f, e = walk(obj["/Resources"], fonts, embedded)
            fonts = fonts.union(f)
            embedded = embedded.union(e)

    unembedded = fonts - embedded

    print("Font List")
    pprint(sorted(list(fonts)))
    if unembedded:
        print("\nUnembedded Fonts")
        pprint(unembedded)

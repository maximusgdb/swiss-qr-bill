import datetime
import tempfile
from qrbill import QRBill
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF

my_bill = QRBill(
    account='CH5800791123000889012',
    creditor={
        'name': 'Jane',
        'pcode': '1000',
        'city': 'Lausanne',
        'country': 'CH',
    },
    amount='22.45',
)

with tempfile.TemporaryFile(encoding='utf-8', mode='r+') as temp:
    my_bill.as_svg(temp)
    temp.seek(0)
    drawing = svg2rlg(temp)

# Generate a clean timestamp and update the PDF file name
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
pdf_filename = f"invoice_{timestamp}.pdf"
renderPDF.drawToFile(drawing, pdf_filename)

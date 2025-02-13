import datetime
from qrbill import QRBill

my_bill = QRBill(
    account='CH5800791123000889012',
    creditor={
        'name': 'Jane',
        'pcode': '1000',
        'city': 'Lausanne',
        'country': 'CH',
    },
    additional_information='test swiss code',
    amount='22.1'
)

# Generate a clean timestamp in the format YYYYMMDD_HHMMSS
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
svg_filename = f"my_bill_{timestamp}.svg"

# Save the SVG file with the timestamp in its name
my_bill.as_svg(svg_filename)

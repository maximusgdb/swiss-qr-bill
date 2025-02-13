import datetime
from qrbill import QRBill
import cairosvg  # Import the cairosvg library for SVG to PNG conversion

# Generate the QR bill object
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

# Define filenames for SVG and PNG
svg_filename = f"my_bill_{timestamp}.svg"
png_filename = f"my_bill_{timestamp}.png"

# Save the SVG file with the timestamp in its name
my_bill.as_svg(svg_filename)

# Convert the SVG file to PNG using cairosvg
cairosvg.svg2png(url=svg_filename, write_to=png_filename)

print(f"SVG file saved as: {svg_filename}")
print(f"PNG file saved as: {png_filename}")
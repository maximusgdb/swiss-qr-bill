from flask import Flask, request, send_file, jsonify
import datetime
from qrbill.bill import QRBill
import cairosvg
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Secure API Token
API_TOKEN = os.getenv("API_TOKEN")

def check_auth():
    """Check if the request contains a valid API token in the Authorization header."""
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return False
    token = auth_header.split(" ")[1]  # Extract token after "Bearer "
    return token == API_TOKEN


@app.route('/generate_bill', methods=['POST'])
def generate_bill():
    try:
        # Validate API token
        if not check_auth():
            return jsonify({"error": "Unauthorized: Invalid or missing API token"}), 401

        # Parse incoming JSON data
        data = request.json

        # Extract required fields from the JSON payload
        account = data.get('account')
        creditor = data.get('creditor')
        amount = data.get('amount')
        currency = data.get('currency', 'CHF')
        debtor = data.get('debtor')
        additional_information = data.get('additional_information', '')
        language = data.get('language', 'en')

        # Validate required fields
        if not all([account, creditor, amount]):
            return jsonify({"error": "Missing required fields: account, creditor, or amount"}), 400

        # Generate the QR bill object
        my_bill = QRBill(
            account=account,
            creditor=creditor,
            final_creditor=data.get('final_creditor'),
            amount=amount,
            currency=currency,
            debtor=debtor,
            ref_number=data.get('ref_number') or data.get('reference_number'),
            extra_infos=data.get('extra_infos', ''),
            additional_information=additional_information,
            alt_procs=data.get('alt_procs', ()),
            language=language,
            top_line=data.get('top_line', True),
            payment_line=data.get('payment_line', True),
            font_factor=data.get('font_factor', 1)
        )

        # Generate a clean timestamp in the format YYYYMMDD_HHMMSS
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

        # Define filenames for SVG and PNG with full path
        output_dir = "/tmp"
        svg_filename = os.path.join(output_dir, f"my_bill_{timestamp}.svg")
        png_filename = os.path.join(output_dir, f"my_bill_{timestamp}.png")

        # Save the SVG file with the timestamp in its name
        my_bill.as_svg(svg_filename)

        # Convert the SVG file to PNG using cairosvg
        cairosvg.svg2png(url=svg_filename, write_to=png_filename)

        # Clean up temporary files
        os.remove(svg_filename)

        # Return the generated PNG file as a response
        return send_file(png_filename, mimetype='image/png', as_attachment=True, download_name=f"qr_bill_{timestamp}.png")

    except Exception as e:
        # Handle errors and return an error response
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

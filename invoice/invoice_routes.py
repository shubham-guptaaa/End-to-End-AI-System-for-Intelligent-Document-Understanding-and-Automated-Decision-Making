import os
import uuid
from flask import request, jsonify
from werkzeug.utils import secure_filename

from invoice.invoice_utils import allowed_file, convert_pdf
from invoice.invoice_model import (
    extract_text, extract_invoice_number, extract_date,
    extract_amount, extract_vendor, extract_items, extract_tax
)
from resume.visualization_utils import generate_confidence_heatmap  # Reuse visualization code


def register_invoice_routes(app):

    @app.route('/invoice', methods=['POST'])
    def invoice_route():
        try:
            
            # Get uploaded file
        
            file = request.files.get("file")

            # Check file validity
            if not file or not allowed_file(file.filename):
                return jsonify({"success": False, "error": "Invalid file type"}), 400

            # Generate unique ID for file
            fileid = str(uuid.uuid4())
            ext = file.filename.rsplit('.', 1)[1].lower()

            upload_folder = "uploads/invoices"
            os.makedirs(upload_folder, exist_ok=True)

            # Handle PDF
            if ext == "pdf":
                pdf_path = os.path.join(upload_folder, f"{fileid}.pdf")
                img_path = os.path.join(upload_folder, f"{fileid}.png")

                file.save(pdf_path)
                convert_pdf(pdf_path, img_path)
                os.remove(pdf_path)

                final_path = img_path
            else:
                final_path = os.path.join(upload_folder, f"{fileid}.{ext}")
                file.save(final_path)

            # Extract text using OCR
            text = extract_text(final_path)

            # Extract fields with confidence scores
            extracted = {
                "invoice_number": extract_invoice_number(text),
                "date": extract_date(text),
                "amount": extract_amount(text),
                "vendor": extract_vendor(text),
                "items": extract_items(text),
                "tax": extract_tax(text)
            }
            
            # Format results with text as answer
            results = {
                field: {
                    "answer": data["text"],
                    "confidence": data["confidence"]
                }
                for field, data in extracted.items()
            }

            # Debug
            print("Extracted results:", results)

            # Generate confidence heatmap
            try:
                heatmap = generate_confidence_heatmap(results)
                if not heatmap or not heatmap.startswith('data:image/png;base64,'):
                    print("Warning: Invalid heatmap data generated")
                    heatmap = None
            except Exception as viz_error:
                print(f"Heatmap generation error: {str(viz_error)}")
                heatmap = None

            # Delete uploaded temporary file
            if os.path.exists(final_path):
                os.remove(final_path)

            # Return successful response
            return jsonify({
                "success": True,
                "results": results,
                "heatmap": heatmap
            })

        except Exception as e:
            
            if 'final_path' in locals() and os.path.exists(final_path):
                os.remove(final_path)
              
            # Return error message  
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500

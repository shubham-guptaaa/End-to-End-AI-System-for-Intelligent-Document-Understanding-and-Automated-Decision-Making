import os
import uuid
from flask import request, jsonify

from resume.resume_utils import allowed_file, convert_pdf_to_image
from resume.resume_model import (
    extract_text, extract_name, extract_email,
    extract_phone, extract_skills, extract_education,
    extract_experience
)
from resume.visualization_utils import generate_confidence_heatmap


def register_resume_routes(app):

    @app.route('/resume', methods=['POST'])
    def resume_route():

        file = request.files.get("file")

        if not file or not allowed_file(file.filename):
            return jsonify({"error": "Invalid file type"}), 400

        fileid = str(uuid.uuid4())
        ext = file.filename.rsplit('.', 1)[1].lower()

        upload_folder = "uploads/resumes"
        os.makedirs(upload_folder, exist_ok=True)

        saved_path = os.path.join(upload_folder, f"{fileid}.{ext}")

        # Save file
        
        file.save(saved_path)

        # Convert PDF to image
        
        if ext == "pdf":
            img_path = os.path.join(upload_folder, f"{fileid}.png")
            convert_pdf_to_image(saved_path, img_path)
            os.remove(saved_path)
        else:
            img_path = saved_path

        try:
            # Extract text using OCR
            
            text = extract_text(img_path)

            # Extract fields with dynamic confidence scores
            
            extracted = {
                "name": extract_name(text),
                "email": extract_email(text),
                "phone": extract_phone(text),
                "skills": extract_skills(text),
                "education": extract_education(text),
                "experience": extract_experience(text)
            }
            
            # Format results
            
            results = {
                field: {
                    "answer": data["text"],
                    "confidence": data["confidence"]
                }
                for field, data in extracted.items()
            }

            # Generate confidence heatmap
            
            try:
                heatmap = generate_confidence_heatmap(results)
                if not heatmap or not heatmap.startswith('data:image/png;base64,'):
                    print("Warning: Invalid heatmap data generated")
                    heatmap = None
            except Exception as viz_error:
                print(f"Heatmap generation error: {str(viz_error)}")
                heatmap = None

            # remove
            if os.path.exists(img_path):
                os.remove(img_path)

            return jsonify({
                "success": True,
                "results": results,
                "heatmap": heatmap
            })

        except Exception as e:

            if os.path.exists(img_path):
                os.remove(img_path)
                
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500

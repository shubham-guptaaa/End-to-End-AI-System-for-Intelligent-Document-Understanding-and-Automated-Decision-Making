import os
import tempfile
from pdf2image import convert_from_path
from PIL import Image

ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def convert_pdf_to_image(file_path, output_path):
    
    #poppler_path
    
    poppler_path = r"C:\poppler-25.07.0\Library\bin"

    with tempfile.TemporaryDirectory() as tmp:
        pages = convert_from_path(file_path, output_folder=tmp, poppler_path=poppler_path)

        # Save first page only (better for resumes)
        
        pages[0].save(output_path, "PNG")

    return output_path

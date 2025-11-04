import os
import tempfile
from pdf2image import convert_from_path
from PIL import Image

# Allowed file extensions for uploads
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif', 'tiff'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def convert_pdf(file_path, output_path):
    
    # Path Poppler required by pdf2image
    
    poppler_path = r"C:\poppler-25.07.0\Library\bin"

    # Temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        
        # Convert PDF pages to images
        
        images = convert_from_path(file_path, output_folder=temp_dir, poppler_path=poppler_path)

        # Save each page as a JPEG
        paths = []
        for i, img in enumerate(images):
            img_path = os.path.join(temp_dir, f"{i}.jpg")
            img.save(img_path, "JPEG")
            paths.append(img_path)

        imgs = [Image.open(p).copy() for p in paths]

    min_width = min(i.width for i in imgs)
    total_height = sum(i.height for i in imgs)

    merged = Image.new(imgs[0].mode, (min_width, total_height))

    y = 0
    for img in imgs:
        merged.paste(img, (0, y))
        y += img.height

    # Save the merged output image
    merged.save(output_path)
    return output_path

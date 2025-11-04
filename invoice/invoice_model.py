from transformers import pipeline
import pytesseract
import re
from PIL import Image

# Path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r"C:\Tesseract\tesseract.exe"

def extract_text(image_path):
    """Extract all text from the invoice image."""
    return pytesseract.image_to_string(Image.open(image_path))

def extract_invoice_number(text):
    """Extract invoice number with confidence score."""
    patterns = [
        r"Invoice\s*#?\s*(\w+[-/]?\w+)",
        r"Invoice\s*Number\s*:?\s*(\w+[-/]?\w+)",
        r"Bill\s*No\s*:?\s*(\w+[-/]?\w+)"
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            # Higher confidence if found with explicit "Invoice" label
            confidence = 95 if "invoice" in pattern.lower() else 85
            return {"text": match.group(1), "confidence": confidence}
    
    return {"text": "Not found", "confidence": 0}

def extract_date(text):
    """Extract invoice date with confidence score."""
    # Various date formats
    patterns = [
        r"Date\s*:?\s*(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})",
        r"Invoice\s*Date\s*:?\s*(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})",
        r"(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})"
    ]
    
    # Check only the top part of the document
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            
            confidence = 95 if "date" in pattern.lower() else 80
            return {"text": match.group(1), "confidence": confidence}
    
    return {"text": "Not found", "confidence": 0}

def extract_amount(text):
    """Extract total amount with confidence score."""
    patterns = [
        r"Total\s*:?\s*[\$₹]?\s*(\d+[,\.]?\d*)",
        r"Amount\s*:?\s*[\$₹]?\s*(\d+[,\.]?\d*)",
        r"Total\s*Amount\s*:?\s*[\$₹]?\s*(\d+[,\.]?\d*)"
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            amount = match.group(1)
            # Higher confidence 
            
            confidence = 95 if "total amount" in pattern.lower() else 85
            return {"text": amount, "confidence": confidence}
    
    return {"text": "Not found", "confidence": 0}

def extract_vendor(text):
    """Extract vendor details with confidence score."""
    patterns = [
        r"(?:From|Vendor|Supplier|Company)\s*:?\s*([A-Za-z\s\.]+(?:Inc|LLC|Ltd|Limited|Corporation)?)",
        r"([A-Za-z\s\.]+(?:Inc|LLC|Ltd|Limited|Corporation))"
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text[:200], re.IGNORECASE) 
        if match:
            vendor = match.group(1).strip()
            
            confidence = 90 if any(label in pattern.lower() for label in ["from", "vendor", "supplier"]) else 75
            return {"text": vendor, "confidence": confidence}
    
    return {"text": "Not found", "confidence": 0}

def extract_items(text):
    """Extract item details with confidence score."""
    
    lines = text.split('\n')
    items = []
    
    price_pattern = r".*[\$₹]?\s*(\d+[,\.]?\d*)\s*$"
    
    for line in lines:
        if re.match(price_pattern, line.strip()):
            items.append(line.strip())
    
    if items:
        confidence = min(95, 60 + len(items) * 5)  # More items = higher confidence
        return {"text": "\n".join(items), "confidence": confidence}
    
    return {"text": "Not found", "confidence": 0}

def extract_tax(text):
    """Extract tax amount with confidence score."""
    patterns = [
        r"(?:Tax|GST|VAT)\s*:?\s*[\$₹]?\s*(\d+[,\.]?\d*)",
        r"(?:Tax|GST|VAT)\s*Amount\s*:?\s*[\$₹]?\s*(\d+[,\.]?\d*)"
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            # Higher confidence for explicit tax labels
            confidence = 95 if any(tax in pattern.lower() for tax in ["gst", "vat"]) else 85
            return {"text": match.group(1), "confidence": confidence}
    
    return {"text": "Not found", "confidence": 0}

# Load the Document QA model
nlp = pipeline("document-question-answering", model="impira/layoutlm-document-qa")

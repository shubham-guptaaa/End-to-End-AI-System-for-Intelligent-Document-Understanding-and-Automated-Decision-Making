import pytesseract
from PIL import Image
import re

# Path to the Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r"C:\Tesseract\tesseract.exe"


def extract_text(image_path):
    """Extracts all raw text from the resume image."""
    return pytesseract.image_to_string(Image.open(image_path))


def extract_name(text):
    """Extract name from the resume with confidence score."""
    lines = text.split("\n")
    for idx, line in enumerate(lines[:5]):
        words = line.split()
        if len(words) >= 2 and len(words) <= 5:  
            confidence = 95 - (idx * 5)  
            return {"text": line.strip(), "confidence": confidence}
    return {"text": "Not found", "confidence": 0}


def extract_email(text):
    """Extract email with confidence based on format validity."""
    match = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
    if match:
        email = match.group(0)
        
        # Higher confidence for professional email domains
        
        confidence = 98 if any(domain in email.lower() for domain in [
            'gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com'
        ]) else 90
        return {"text": email, "confidence": confidence}
    return {"text": "Not found", "confidence": 0}


def extract_phone(text):
    """Extract phone number with confidence based on format."""
    match = re.search(r"(\+91[- ]?)?[0-9]{10}", text)
    if match:
        number = match.group(0)
        
        # Higher confidence for properly formatted numbers
        
        confidence = 98 if len(number.replace('+', '').replace('-', '')) >= 10 else 85
        return {"text": number, "confidence": confidence}
    return {"text": "Not found", "confidence": 0}


def extract_skills(text):
    """Extract skills with confidence based on number of matches."""
    keywords = {
        "Languages": ["Python", "Java", "C++", "JavaScript", "TypeScript", "Go"],
        "Web": ["HTML", "CSS", "React", "Angular", "Vue", "Node.js", "Django", "Flask"],
        "Data": ["SQL", "MongoDB", "PostgreSQL", "MySQL", "Redis"],
        "ML/AI": ["Machine Learning", "AI", "Deep Learning", "TensorFlow", "PyTorch"],
        "Tools": ["Git", "Docker", "Kubernetes", "AWS", "Azure", "GCP"]
    }
    
    found = []
    total_keywords = sum(len(v) for v in keywords.values())
    matches = 0
    
    for category, terms in keywords.items():
        category_matches = [k for k in terms if k.lower() in text.lower()]
        if category_matches:
            found.extend(category_matches)
            matches += len(category_matches)
    
    if found:
        
        confidence = max(60, min(95, (matches / total_keywords) * 100))
        return {"text": ", ".join(found), "confidence": confidence}
    return {"text": "Not found", "confidence": 0}


def extract_education(text):
    """Extract education with confidence based on keyword matches."""
    edu_keywords = {
        "high": ["B.Tech", "M.Tech", "PhD", "Bachelor", "Master", "Computer Science"],
        "medium": ["Engineering", "Technology", "Science", "University", "College"],
        "low": ["School", "Institute", "Academy"]
    }
    
    lines = text.split("\n")
    best_match = {"line": "", "confidence": 0}
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Calculate confidence based on keyword matches
        
        confidence = 0
        if any(k.lower() in line.lower() for k in edu_keywords["high"]):
            confidence = 90
        elif any(k.lower() in line.lower() for k in edu_keywords["medium"]):
            confidence = 75
        elif any(k.lower() in line.lower() for k in edu_keywords["low"]):
            confidence = 60
            
        if confidence > best_match["confidence"]:
            best_match = {"line": line, "confidence": confidence}
    
    if best_match["line"]:
        return {"text": best_match["line"], "confidence": best_match["confidence"]}
    return {"text": "Not found", "confidence": 0}


def extract_experience(text):
    """Extract experience with confidence based on context and keywords."""
    exp_keywords = {
        "roles": ["Developer", "Engineer", "Architect", "Lead", "Manager", "Intern"],
        "companies": ["Technologies", "Software", "Solutions", "Systems", "Inc", "Ltd"],
        "context": ["Experience", "Work", "Employment", "Career", "Professional"]
    }
    
    lines = text.split("\n")
    best_match = {"line": "", "confidence": 0}
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Calculate confidence based on keyword matches
        
        confidence = 0
        
        # Role match
        if any(k.lower() in line.lower() for k in exp_keywords["roles"]):
            confidence += 40
        
        # Company indicator match
        if any(k.lower() in line.lower() for k in exp_keywords["companies"]):
            confidence += 30
            
        # Context match
        if any(k.lower() in line.lower() for k in exp_keywords["context"]):
            confidence += 20
            
        # Cap confidence at 95%
        confidence = min(95, confidence)
        
        if confidence > best_match["confidence"]:
            best_match = {"line": line, "confidence": confidence}
    
    if best_match["line"]:
        return {"text": best_match["line"], "confidence": best_match["confidence"]}
    return {"text": "Not found", "confidence": 0}

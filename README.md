# Document AI System

An intelligent document processing system that can analyze invoices and resumes using OCR and machine learning. The system provides confidence scores and visual heatmaps for extracted information.

## 🌟 Features

### Invoice Analysis
- Extract key information from invoices:
  - Invoice numbers
  - Dates
  - Amount details
  - Vendor information
  - Tax information
  - Line items
- Confidence scoring for each extracted field
- Visual heatmap showing extraction confidence levels

### Resume Analysis
- Extract and analyze resume components:
  - Skills
  - Experience
  - Education
  - Important sections
- Confidence-based highlighting
- Visual heatmap representation

## 🛠️ Technology Stack

- **Backend**: Python Flask
- **Frontend**: HTML, CSS, JavaScript
- **ML/AI Components**:
  - OCR: Tesseract
  - Document Understanding: LayoutLM (Transformers)
  - Visualization: Matplotlib, Seaborn
- **Server**: Waitress (Production WSGI)

## 📋 Prerequisites

- Python 3.8+
- Tesseract OCR Engine
- Required Python packages (see `requirements.txt`)

## 🚀 Setup and Installation

1. Clone the repository:
```bash
git clone https://github.com/shubham-guptaaa/End-to-End-AI-System-for-Intelligent-Document-Understanding-and-Automated-Decision-Making.git

```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Linux/Mac
# OR
venv\Scripts\activate     # On Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install Tesseract OCR:
- **Windows**: Download installer from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)
- **Linux**: `sudo apt-get install tesseract-ocr`
- **Mac**: `brew install tesseract`

5. Update Tesseract path in `invoice_model.py`:
```python
pytesseract.pytesseract.tesseract_cmd = r"C:\Tesseract\tesseract.exe"  # Adjust path as needed
```

## 🏃‍♂️ Running the Application

1. Start the server:
```bash
python main.py
```

2. Open in browser:
```
http://localhost:2001
```

## 📁 Project Structure

```
├── invoice/                 # Invoice processing module
│   ├── invoice_model.py    # Invoice extraction logic
│   ├── invoice_routes.py   # API routes for invoice
│   └── invoice_utils.py    # Utility functions
├── resume/                  # Resume processing module
│   ├── resume_model.py     # Resume extraction logic
│   ├── resume_routes.py    # API routes for resume
│   └── visualization_utils.py # Heatmap generation
├── static/                  # Static assets
│   ├── css/               
│   │   ├── index.css      # Landing page styles
│   │   ├── invoice.css    # Invoice page styles
│   │   └── resume.css     # Resume page styles
│   └── js/
│       ├── invoice.js     # Invoice frontend logic
│       └── resume.js      # Resume frontend logic
├── templates/              # HTML templates
│   ├── index.html         # Landing page
│   ├── invoice.html       # Invoice analysis page
│   └── resume.html        # Resume analysis page
├── uploads/               # Temporary file storage
│   ├── invoices/         # Uploaded invoices
│   └── resumes/          # Uploaded resumes
├── main.py               # Application entry point
└── requirements.txt      # Python dependencies
```

## 🔍 API Endpoints

### Invoice Analysis
- `POST /invoice`
  - Upload and analyze invoice documents
  - Returns extracted fields with confidence scores and heatmap

### Resume Analysis
- `POST /resume`
  - Upload and analyze resume documents
  - Returns parsed sections with confidence scores and heatmap


### Document Processing
- OCR using Tesseract for text extraction
- LayoutLM for understanding document structure
- Regular expressions for field extraction
- Confidence scoring for each extracted field

### Visualization
- Interactive heatmaps showing confidence levels
- Color-coded confidence indicators
- Visual feedback for extraction quality

### User Interface
- Clean, responsive design
- Real-time processing feedback
- Visual representation of results
- Mobile-friendly layout

## 🔐 Security Notes

- Uploaded files are temporarily stored and automatically cleaned up
- No sensitive information is permanently stored
- Local processing - no external API dependencies

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Tesseract OCR engine
- Hugging Face Transformers
- Flask framework

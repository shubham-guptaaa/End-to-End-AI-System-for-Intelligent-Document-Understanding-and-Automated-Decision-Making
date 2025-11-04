print("Importing modules...")
from flask import Flask, render_template
from waitress import serve

from invoice.invoice_routes import register_invoice_routes
from resume.resume_routes import register_resume_routes

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Route for Home Page
@app.route('/')
def home():
    return render_template("index.html")

#  Route for invoice UI page
@app.route('/invoice-page')
def invoice_page():
    return render_template("invoice.html")

# Route for resume UI page 
@app.route('/resume-page')
def resume_page():
    return render_template("resume.html")

# Register invoice backend logic
register_invoice_routes(app)

# Register resume backend logic
register_resume_routes(app)

print("Server started!")
serve(app, host="0.0.0.0", port=2001)

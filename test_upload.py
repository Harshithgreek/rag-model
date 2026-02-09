import requests
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

# Create a simple test PDF
pdf_buffer = io.BytesIO()
c = canvas.Canvas(pdf_buffer, pagesize=letter)
c.drawString(100, 750, "This is a test PDF document.")
c.drawString(100, 730, "It contains some sample text for testing the RAG system.")
c.drawString(100, 710, "The quick brown fox jumps over the lazy dog.")
c.save()
pdf_buffer.seek(0)

# Test the upload endpoint
url = "http://localhost:8000/upload"
files = {'file': ('test.pdf', pdf_buffer, 'application/pdf')}

try:
    response = requests.post(url, files=files)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {e}")

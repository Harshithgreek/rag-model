from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def create_sample_pdf(path="backend/data/knowledge.pdf"):
    c= canvas.Canvas(path, pagesize=letter)
    text = c.beginText(40, 750)

    lines= [
        "This is a sample PDF document for testing the RAG system.",    
        "",
        "Q: How do I file a claim?",
        "A: To file a claim, you can visit our website and click on the 'File a Claim' button. Follow the instructions to submit your claim online.",
        "",         
        "Q: What documents do I need to provide?",
        "A: You will need to provide a copy of your ID, proof of purchase,  and any relevant photos or documentation related to your claim.",
        "",         
        "Q: How long does the claims process take?",
        "A: The claims process typically takes 5-7 business days, but it may vary depending on the complexity of the claim and the volume of claims we are processing.",
        "",     
    ]

    for line in lines:
        text.textLine(line)

    c.drawText(text)
    c.showPage()
    c.save()


if __name__ == "__main__":
    create_sample_pdf()
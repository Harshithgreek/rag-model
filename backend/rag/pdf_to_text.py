from pypdf import PdfReader

def pdf_to_text(pdf_path : str) -> str:
    reader = PdfReader(pdf_path)
    pages = []
    for page in reader.pages:
        pages.append(page.extract_text() or "")

        text="\n".join(pages)
        text=text.replace("\r", "\n")
        text="\n".join([line.strip() for line in text.splitlines() if line.strip()])
    return text 

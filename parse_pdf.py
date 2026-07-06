import pypdf
import re

pdf = pypdf.PdfReader("Fit & Fine Forever Catalogue - new.pdf")
for i, page in enumerate(pdf.pages):
    text = page.extract_text()
    # Remove excessive spaces between letters
    text = re.sub(r'([A-Za-z0-9])\s([A-Za-z0-9])', r'\1\2', text)
    # run again for chained ones
    text = re.sub(r'([A-Za-z0-9])\s([A-Za-z0-9])', r'\1\2', text)
    text = re.sub(r'([A-Za-z0-9])\s([A-Za-z0-9])', r'\1\2', text)
    text = re.sub(r'([A-Za-z0-9])\s([A-Za-z0-9])', r'\1\2', text)
    print(f"--- PAGE {i+1} ---")
    print(text)

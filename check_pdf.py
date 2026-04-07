import PyPDF2
import os

pdf_path = r'd:\App\Quiz-extraction\scan\ElectricExam2019.pdf'
if os.path.exists(pdf_path):
    with open(pdf_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        num_pages = len(reader.pages)
        print(f"Total pages: {num_pages}")
        
        # Check first page text content
        page = reader.pages[0]
        text = page.extract_text()
        print(f"Page 1 text length: {len(text)}")
        print("Page 1 snippet:")
        print(text[:500])
else:
    print(f"File not found: {pdf_path}")

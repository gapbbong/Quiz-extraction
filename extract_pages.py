import fitz
import os

pdf_path = r'd:\App\Quiz-extraction\scan\ElectricExam2019.pdf'
output_dir = r'd:\App\Quiz-extraction\preview'
os.makedirs(output_dir, exist_ok=True)

doc = fitz.open(pdf_path)
for i in range(min(5, len(doc))):
    page = doc.load_page(i)
    pix = page.get_pixmap(dpi=150) # Lower DPI to see more at once
    output_path = os.path.join(output_dir, f'page_{i+1}.png')
    pix.save(output_path)
    print(f"Saved page {i+1} to {output_path}")
doc.close()

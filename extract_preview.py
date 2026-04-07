import fitz
import os

pdf_path = r'd:\App\Quiz-extraction\scan\ElectricExam2019.pdf'
output_dir = r'd:\App\Quiz-extraction\preview'
os.makedirs(output_dir, exist_ok=True)

doc = fitz.open(pdf_path)
page = doc.load_page(0)
pix = page.get_pixmap(dpi=300)
output_path = os.path.join(output_dir, 'page_1.png')
pix.save(output_path)
print(f"Saved page 1 to {output_path}")
doc.close()

import fitz
import os

pdf_path = r'd:\App\Quiz-extraction\scan\ElectricExam2019.pdf'
output_dir = r'd:\App\Quiz-extraction\session_images\s2'
os.makedirs(output_dir, exist_ok=True)

doc = fitz.open(pdf_path)
# Session 2: Pages 11-20 (10 to 19 in 0-indexed)
for i in range(10, 20):
    page = doc.load_page(i)
    pix = page.get_pixmap(dpi=300)
    output_path = os.path.join(output_dir, f'page_{i+1}.png')
    pix.save(output_path)
    print(f"Saved Session 2 Page {i+1} to {output_path}")

doc.close()

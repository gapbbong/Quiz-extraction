import fitz
import os

pdf_path = r'd:\App\Quiz-extraction\scan\ElectricExam2019.pdf'
output_dir = r'd:\App\Quiz-extraction\session_images\s1'
os.makedirs(output_dir, exist_ok=True)

doc = fitz.open(pdf_path)
# Session 1: Pages 1-10 (0 to 9 in 0-indexed)
for i in range(10):
    page = doc.load_page(i)
    pix = page.get_pixmap(dpi=300)
    output_path = os.path.join(output_dir, f'page_{i+1}.png')
    pix.save(output_path)
    print(f"Saved Session 1 Page {i+1} to {output_path}")

doc.close()

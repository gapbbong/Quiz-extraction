import fitz
import os

pdf_path = r'd:\App\Quiz-extraction\scan\ElectricExam2019.pdf'
output_dir = r'd:\App\Quiz-extraction\preview'
os.makedirs(output_dir, exist_ok=True)

doc = fitz.open(pdf_path)
total_pages = len(doc)
print(f"Total pages: {total_pages}")

# Extract headers (top portion of the first 40 pages) to identify sessions
for i in range(min(40, total_pages)):
    page = doc.load_page(i)
    # Get the top 20% of the page to find the session title
    rect = page.rect
    clip_rect = fitz.Rect(0, 0, rect.width, rect.height * 0.2)
    pix = page.get_pixmap(clip=clip_rect, dpi=150)
    output_path = os.path.join(output_dir, f'header_{i+1}.png')
    pix.save(output_path)

doc.close()
print("Extracted headers for first 40 pages.")

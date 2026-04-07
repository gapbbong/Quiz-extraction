import cv2
import numpy as np
import os

image_path = r'd:\App\Quiz-extraction\preview\page_1.png'
img = cv2.imread(image_path)
if img is None:
    print("Could not load image.")
    exit()

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# 1. Preprocessing: background (brightness 220+) removal
_, binary = cv2.threshold(gray, 220, 255, cv2.THRESH_BINARY_INV)

# 2. Filtering: Identify 'Images'
# Logic: [150 < W < 45%] and [100 < H < 45%]
page_h, page_w = gray.shape
min_w, max_w = 150, int(page_w * 0.45)
min_h, max_h = 100, int(page_h * 0.45)

contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

img_regions = []
for cnt in contours:
    x, y, w, h = cv2.boundingRect(cnt)
    if min_w < w < max_w and min_h < h < max_h:
        img_regions.append((x, y, w, h))
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

print(f"Found {len(img_regions)} potential image regions on page 1.")

# Save debug image
cv2.imwrite(r'd:\App\Quiz-extraction\preview\page_1_debug.png', img)

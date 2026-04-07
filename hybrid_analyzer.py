import cv2
import numpy as np
import os

class HybridVisionAnalyzer:
    def __init__(self, brightness_threshold=220):
        self.brightness_threshold = brightness_threshold

    def analyze_page(self, image_path):
        img = cv2.imread(image_path)
        if img is None:
            return None, []

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Background removal (brightness 220+)
        _, binary = cv2.threshold(gray, self.brightness_threshold, 255, cv2.THRESH_BINARY_INV)

        page_h, page_w = gray.shape
        mid_x = page_w // 2

        # Constraints: [150 < W < 45%] and [100 < H < 45%]
        min_w, max_w = 150, int(page_w * 0.45)
        min_h, max_h = 100, int(page_h * 0.45)

        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        regions = []
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            # Label as Image if it meets the criteria
            if min_w < w < max_w and min_h < h < max_h:
                column = 'left' if (x + w/2) < mid_x else 'right'
                regions.append({
                    'type': 'image',
                    'box': [y, x, y+h, x+w], # ymin, xmin, ymax, xmax
                    'column': column,
                    'y': y,
                    'x': x
                })

        # Sorting: Left column first, then Right. Within column, Top -> Bottom.
        left_regions = sorted([r for r in regions if r['column'] == 'left'], key=lambda r: r['y'])
        right_regions = sorted([r for r in regions if r['column'] == 'right'], key=lambda r: r['y'])
        
        return img, left_regions + right_regions

    def crop_region(self, img, box, output_path):
        ymin, xmin, ymax, xmax = box
        crop = img[ymin:ymax, xmin:xmax]
        cv2.imwrite(output_path, crop)
        return output_path

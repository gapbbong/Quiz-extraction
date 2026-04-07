import json
import os
import glob

s1_path = r'd:\App\Quiz-extraction\output\s1\ElectricExam2019_S1.json'
s2_path = r'd:\App\Quiz-extraction\output\s2\ElectricExam2019_S2.json'

with open(s1_path, 'r', encoding='utf-8') as f:
    s1_data = json.load(f)
with open(s2_path, 'r', encoding='utf-8') as f:
    s2_data = json.load(f)

print(f"Session 1: {len(s1_data)} questions")
print(f"Session 2: {len(s2_data)} questions")

# Combine
combined = s1_data + s2_data

combined_path = r'd:\App\Quiz-extraction\output\ElectricExam2019_Final.json'
with open(combined_path, 'w', encoding='utf-8') as f:
    json.dump(combined, f, ensure_ascii=False, indent=2)

print(f"Combined into {combined_path}")

# Check images
img_count = len(glob.glob(r'd:\App\Quiz-extraction\output\s*\images\*.png'))
print(f"Total images cropped: {img_count}")

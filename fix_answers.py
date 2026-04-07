import json
import os

files_to_fix = [
    r'd:\App\Quiz-extraction\output\s1\ElectricExam2019_S1.json',
    r'd:\App\Quiz-extraction\output\s2\ElectricExam2019_S2.json',
    r'd:\App\Quiz-extraction\output\ElectricExam2019_Final.json'
]

for file_path in files_to_fix:
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        fixed_count = 0
        for item in data:
            # We assume answers 0-3 are indexes and we want 1-4
            # We check if answer is integer and in [0, 3]
            # But to be safe, we just add 1 to all if they are indeed indices
            if isinstance(item.get("answer"), int):
                item["answer"] += 1
                fixed_count += 1
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"Updated {file_path}: {fixed_count} questions fixed.")
    else:
        print(f"File not found: {file_path}")

import os
import re

def normalize_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    # Pattern to find Choice 1 on the same line as "선택지:" header
    # Example: "* [cite_start]**선택지:** 1. $EI \cos \theta$"
    pattern = re.compile(r'^(\s*\*.*선택지:.*?)\s+(\d\.|①|1\))\s*(.*)$')
    
    for line in lines:
        match = pattern.match(line)
        if match:
            # Header part
            new_lines.append(match.group(1).strip() + "\n")
            # Choice part
            new_lines.append(f"    {match.group(2)} {match.group(3)}\n")
        else:
            new_lines.append(line)
            
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

if __name__ == "__main__":
    files = [
        "e:/3D studies/Dukigo+/data/2015_01회차.txt",
        "e:/3D studies/Dukigo+/data/2015_02회차.txt",
        "e:/3D studies/Dukigo+/data/2015_03회차.txt",
        "e:/3D studies/Dukigo+/data/2015_04회차.txt"
    ]
    for f in files:
        if os.path.exists(f):
            print(f"Normalizing {f}")
            normalize_txt(f)

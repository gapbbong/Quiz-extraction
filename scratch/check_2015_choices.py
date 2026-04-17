import json
import glob
import os

def check_choices():
    files = glob.glob('e:/3D studies/Dukigo+/data/2015_*_questions.json')
    report = {}
    
    for f in files:
        with open(f, 'r', encoding='utf-8') as j:
            data = json.load(j)
            file_name = os.path.basename(f)
            invalid = []
            for q in data:
                c_count = len(q.get('choices', []))
                if c_count != 4:
                    invalid.append({
                        "number": q.get('number'),
                        "count": c_count,
                        "choices": q.get('choices')
                    })
            if invalid:
                report[file_name] = invalid
    
    print(json.dumps(report, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    check_choices()

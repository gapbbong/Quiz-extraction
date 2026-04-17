import json
import os

b19 = r"e:\Quiz-extraction\backups_morning\ElectricExam2019_Final.json"
b20 = r"e:\Quiz-extraction\backups_morning\ElectricExam_MultiYear.json"
master = r"e:\Quiz-extraction\output\ElectricExam_MASTER_DB.json"

def rebuild():
    data_dir = r"e:\3D studies\Dukigo+\data"
    master = r"e:\Quiz-extraction\output\ElectricExam_MASTER_DB.json"
    
    all_data = []
    
    # Files to include (explicit or wildcard)
    for filename in os.listdir(data_dir):
        if filename.endswith("_questions.json"):
            path = os.path.join(data_dir, filename)
            print(f"Loading {filename}...")
            with open(path, 'r', encoding='utf-8') as f:
                d = json.load(f)
                # Try to extract year and round from filename (e.g., 2015_01_questions.json)
                parts = filename.split('_')
                year = parts[0]
                round_str = parts[1] if len(parts) > 1 else ""
                
                for q in d:
                    q['year'] = q.get('year') or year
                    q['round'] = q.get('round') or round_str
                    # Final format fix
                    q['number'] = str(q.get('number') or q.get('question_num') or q.get('question_number') or '00').zfill(2)
                    q['question'] = q.get('question') or q.get('question_text') or ''
                    q['choices'] = q.get('choices') or q.get('options') or []
                    q['explanation'] = q.get('explanation') or q.get('solution') or q.get('commentary') or ''
                    q['answer'] = str(q.get('answer', ''))
                    
                all_data.extend(d)

    with open(master, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)
    print(f"Rebuild Complete: {len(all_data)} total items.")

if __name__ == "__main__":
    rebuild()

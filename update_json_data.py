import json
import re
import os

# 파일 경로
json_path = r'd:\App\Quiz-extraction\output\ElectricExam2019_Final.json'

# ① ② ③ ④ 를 공백으로 치환하는 정규표현식
pattern = re.compile(r'[①②③④]\s*')

def clean_choice(text):
    if not isinstance(text, str):
        return text
    # ① ② ③ ④ 제거
    return pattern.sub('', text)

def process_quiz():
    if not os.path.exists(json_path):
        print(f"File not found: {json_path}")
        return

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for item in data:
        # 1. exam_title 강제 설정 (또는 삽입)
        item['exam_title'] = "2019년 제1회 CBT 기출복원문제"

        # 2. 선택지에서 ① ② ③ ④ 제거
        if 'choices' in item and isinstance(item['choices'], list):
            item['choices'] = [clean_choice(c) for c in item['choices']]

    # 변경된 데이터 저장
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("JSON 데이터 처리가 완료되었습니다.")

if __name__ == "__main__":
    process_quiz()

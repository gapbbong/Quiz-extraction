import json
import re
import os

def clean_text(text):
    if not text:
        return ""
    # Remove [cite: ...] and [cite_start]
    text = re.sub(r'\[cite:.*?\]', '', text)
    text = re.sub(r'\[cite_start\]', '', text)
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text

import urllib.parse

def add_image_tag(question_text, year, round_str, q_num):
    # Check if we have an image for this question
    img_dir = f"e:/3D studies/Dukigo+/public/images/exams/{year}/{round_str}"
    img_filename = f"q{int(q_num)}_1.webp" # Ensure it's like q4_1.webp
    abs_img_path = os.path.normpath(os.path.join(img_dir, img_filename))
    
    # If file exists, add an image tag for the verifier
    if os.path.exists(abs_img_path):
        encoded_path = urllib.parse.quote(abs_img_path)
        img_url = f"http://localhost:5001/serve-image?path={encoded_path}"
        return f"{question_text}<br><img src='{img_url}' style='max-width:300px; margin-top:10px; border-radius:8px; border:1px solid #444; display:block;'>"
    
    img_keywords = ["그림", "회로", "곡선", "다음과 같은", "그래프", "브리지", "어드미턴스", "리액턴스"]
    if any(kw in question_text for kw in img_keywords):
        if "[그림 참고]" not in question_text:
            return f"{question_text} <span style='color: #fbbf24; font-weight: bold;'>[그림 참고]</span>"
    return question_text

def clean_all_citations(text):
    if not text: return ""
    # Remove [cite: ...] and [cite_start] and [cite_end]
    text = re.sub(r'\[cite_start\]', '', text)
    text = re.sub(r'\[cite_end\]', '', text)
    text = re.sub(r'\[cite:.*?\]', '', text)
    return text.strip()

def parse_generic(content, q_pattern, opt_pattern, ans_pattern, exp_pattern, round_str, year=2015):
    # PRE-CLEAN EVERYTHING
    content = clean_all_citations(content)
    # Global fix: Convert \Omega to the actual Ω symbol for better display
    content = content.replace(r'\Omega', 'Ω')
    content = content.replace(r'[\Omega]', '[Ω]')
    
    questions_list = []
    matches = list(re.finditer(q_pattern, content, re.MULTILINE | re.DOTALL))
    
    for i, match in enumerate(matches):
        try:
            q_num_raw = match.group(1)
            q_num = int(q_num_raw)
            start_pos = match.end()
            end_pos = matches[i+1].start() if i + 1 < len(matches) else len(content)
            block = content[start_pos:end_pos]
            
            # Real Question Text Check
            q_text_match = re.search(r'(?:\*\*문제:\*\*|문제:)\s*(.*?)(?=\n\*|\n\s*1\.|\n\d\.|---|\Z)', block, re.DOTALL)
            
            question_raw = ""
            if q_text_match:
                question_raw = q_text_match.group(1).strip()
            
            if not question_raw or len(question_raw) < 5:
                header_text = match.group(2).strip()
                header_text = re.sub(r'^[\d\.\s]+', '', header_text)
                question_raw = header_text
            
            question = clean_text(question_raw)
            
            # Options
            options = []
            opt_matches = re.findall(opt_pattern, block, re.MULTILINE)
            if opt_matches:
                opts = []
                for m in opt_matches:
                    if isinstance(m, tuple): opts.extend([x for x in m if x])
                    else: opts.append(m)
                # Clean choices: remove stars like **1.2**
                options = [re.sub(r'^\*\*(.*?)\*\*', r'\1', clean_text(o)).strip() for o in opts if o.strip()]
                options = options[:4]
            
            # Answer - More flexible regex to find ① or **①** or 정답: 1 etc
            ans_match = re.search(r'(?:정답|답)[:\*\s]+([①-④1-4])', block)
            answer = 0
            if ans_match:
                ans_str = ans_match.group(1)
                ans_map = {'①': 1, '②': 2, '③': 3, '④': 4, '1': 1, '2': 2, '3': 3, '4': 4}
                answer = ans_map.get(ans_str, 0)
                
            # Explanation - Relaxed start pattern
            exp_match = re.search(r'(?:\*\*해설.*?\*\*|해설.*?)\s*[:]\s*(.*?)(?=\n\*|\n---|\Z)', block, re.DOTALL)
            explanation = clean_text(exp_match.group(1)) if exp_match else ""
            
            item = {
                "id": f"{year}_{round_str}_{q_num}",
                "year": year,
                "round": round_str,
                "number": str(q_num).zfill(2),
                "question": add_image_tag(question, year, round_str, q_num),
                "choices": options,
                "answer": answer,
                "explanation": explanation,
                "level": "하"
            }
            questions_list.append(item)
            
        except Exception as e:
            print(f"Error parsing match {i+1}: {e}")
    
    # Deduplicate
    final_dict = {}
    for q in questions_list:
        num = q["number"]
        if num not in final_dict:
            final_dict[num] = q
        else:
            if not final_dict[num]["choices"] and q["choices"]:
                final_dict[num] = q
            elif len(q["question"]) > len(final_dict[num]["question"]):
                final_dict[num] = q

    return [final_dict[n] for n in sorted(final_dict.keys())]

def main():
    data_dir = "e:/3D studies/Dukigo+/data"
    
    rounds = [
        {
            "file": "2015_01회차.txt", 
            "out": "2015_01_questions.json", 
            "round": "01", 
            "q": r'## \*\*(\d+)\.\s+(.*?)(?=\[cite|---|\n)', 
            "opt": r'^\s*\d\.\s*(.*?)$', 
            "ans": r'IGNORED', 
            "exp": r'IGNORED'
        },
        {
            "file": "2015_02회차.txt", 
            "out": "2015_02_questions.json", 
            "round": "02", 
            "q": r'\*\*(\d{2})\s+(.*?)\*\*', 
            "opt": r'[①-④]\s*(.*?)(?=[①-④]|\Z|\n)', 
            "ans": r'IGNORED', 
            "exp": r'IGNORED'
        },
        {
            "file": "2015_03회차.txt", 
            "out": "2015_04_questions.json", 
            "round": "04", 
            "q": r'### \*\*(\d+)\s+(.*?)\*\*', 
            "opt": r'[①-④]\s*(.*?)(?=[①-④]|\Z|\n)', 
            "ans": r'IGNORED', 
            "exp": r'IGNORED'
        },
        {
            "file": "2015_04회차.txt", 
            "out": "2015_05_questions.json", 
            "round": "05", 
            "q": r'\*\*(\d{2})\.\s+(.*?)\*\*', 
            "opt": r'[①-④]\s*(.*?)(?=[①-④]|\Z|\n)', 
            "ans": r'IGNORED', 
            "exp": r'IGNORED'
        }
    ]

    for rd in rounds:
        path = os.path.join(data_dir, rd["file"])
        if not os.path.exists(path):
            print(f"Skipping {rd['file']} (Not Found)")
            continue
            
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Unified parsing for all rounds since we improved patterns in parse_generic
            questions = parse_generic(
                content,
                q_pattern=rd["q"],
                opt_pattern=rd["opt"],
                ans_pattern="", 
                exp_pattern="",
                round_str=rd["round"]
            )
            out_path = os.path.join(data_dir, rd["out"])
            with open(out_path, 'w', encoding='utf-8') as out:
                json.dump(questions, out, ensure_ascii=False, indent=2)
            print(f"Generated {rd['out']} from {rd['file']} ({len(questions)} questions)")

    print("Re-conversion completed with robust patterns.")


if __name__ == "__main__":
    main()

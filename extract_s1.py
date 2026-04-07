import google.generativeai as genai
import PIL.Image
import os
import json
import glob
import re
from hybrid_analyzer import HybridVisionAnalyzer

# Configuration
API_KEY = "AIzaSyDIp6TJgOrhtFvcR1TAS8mQDNlDnZfdBys"
MODEL_NAME = "gemini-2.5-flash"
YEAR = "2019"
SESSION = "1"

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel(MODEL_NAME)
analyzer = HybridVisionAnalyzer()

image_dir = r'd:\App\Quiz-extraction\session_images\s1'
output_dir = r'd:\App\Quiz-extraction\output\s1'
os.makedirs(output_dir, exist_ok=True)
os.makedirs(os.path.join(output_dir, 'images'), exist_ok=True)

final_data = []

prompt_template = """
너는 하이브리드 비전 분석기야. 첨부된 시험지 이미지를 분석해서 모든 문제를 JSON 형식으로 추출해줘.

[데이터 추출 규칙]
1. 모든 문제를 누락 없이 순서대로 추출해.
2. `exam_title`: "{exam_title}".
3. `number`: 문제 번호만 숫자로 추출 (예: "01", "02").
3. `question`: 질문 텍스트. 그림이 위치한 곳에 [그림] 표시.
4. `choices`: 1~4번 보기를 담은 배열.
5. `answer`: 정답 보기 번호 (1-4).
6. `explanation`: 문제 풀이 핵심 원리 (1-2문장).
7. `image_boxes`: 
   - `question_box`: 질문 내 그림 영역이 있다면 [ymin, xmin, ymax, xmax] (픽셀 단위). 없으면 null.
   - `choice_boxes`: 보기 내 그림 영역이 있다면 각 보기에 대응하는 [[ymin, xmin, ymax, xmax], ...] 배열. 없으면 [].

[이미지 파일명 규칙] 
- 이미지는 코드에서 나중에 처리할 예정이니 JSON 필드에는 파일명만 미리 생성해줘:
- 질문용: img_{year}_{session}_<number>_q.png
- 선택지용: img_{year}_{session}_<number>_c<index>.png

오직 JSON 배열 형식으로만 응답해.
"""

page_files = sorted(glob.glob(os.path.join(image_dir, 'page_*.png')), key=lambda x: int(os.path.basename(x).split('_')[1].split('.')[0]))

for page_file in page_files:
    print(f"Processing {page_file}...")
    img, regions = analyzer.analyze_page(page_file)
    p_img = PIL.Image.open(page_file)
    
    try:
        response = model.generate_content([prompt_template.format(year=YEAR, session=SESSION, exam_title="2019년 제1회 CBT 기출복원문제")] + [p_img])
        raw_text = response.text
        
        # Robust JSON extraction
        match = re.search(r'\[.*\]', raw_text, re.DOTALL)
        if match:
            json_str = match.group(0)
            page_data = json.loads(json_str)
            
            for item in page_data:
                # Clean number
                q_num_str = str(item.get("number", ""))
                q_num = "".join(filter(str.isdigit, q_num_str)).zfill(2)
                item["number"] = q_num
                
                # Image processing
                boxes = item.get("image_boxes", {})
                
                # Question Image
                q_box = boxes.get("question_box")
                if q_box and isinstance(q_box, list) and len(q_box) == 4:
                    fname = f"img_{YEAR}_{SESSION}_{q_num}_q.png"
                    analyzer.crop_region(img, q_box, os.path.join(output_dir, 'images', fname))
                    item["image"] = fname
                else:
                    item["image"] = None
                
                # Choice Images
                c_boxes = boxes.get("choice_boxes", [])
                item["choice_images"] = []
                item["choice_boxes"] = []
                if c_boxes and isinstance(c_boxes, list):
                    for i, b in enumerate(c_boxes):
                        if b and len(b) == 4:
                            fname = f"img_{YEAR}_{SESSION}_{q_num}_c{i+1}.png"
                            analyzer.crop_region(img, b, os.path.join(output_dir, 'images', fname))
                            item["choice_images"].append(fname)
                            item["choice_boxes"].append(b)
                
                # Cleanup internal box helper
                if "image_boxes" in item: del item["image_boxes"]
                
                final_data.append(item)
        else:
            print(f"No JSON found in response for {page_file}")

    except Exception as e:
        print(f"Error processing {page_file}: {e}")

# Save final JSON for Session 1
with open(os.path.join(output_dir, 'ElectricExam2019_S1.json'), 'w', encoding='utf-8') as f:
    json.dump(final_data, f, ensure_ascii=False, indent=2)

print(f"Session 1 extraction complete. Total questions: {len(final_data)}")

import google.generativeai as genai
import PIL.Image
import os
import glob
import time

# Configure API
genai.configure(api_key="AIzaSyDIp6TJgOrhtFvcR1TAS8mQDNlDnZfdBys")
# Using the model user requested
model = genai.GenerativeModel('gemini-2.5-flash')

header_dir = r'd:\App\Quiz-extraction\preview'
header_files = sorted(glob.glob(os.path.join(header_dir, 'header_*.png')), key=lambda x: int(x.split('_')[-1].split('.')[0]))

# We'll check headers to find "2019년 제1회", "2019년 제2회"
prompt = """
첨부된 이미지들은 시험지의 상단 헤더 부분이야. 
이미지 번호(header_N)와 이미지에 적힌 회차 내용을 확인해서, 
각 회차가 시작되는 이미지 번호를 알려줘.
결과는 아래 JSON 형식으로만 응답해:
{
  "sessions": [
    {"title": "2019년 제1회", "start_page": 1},
    {"title": "2019년 제2회", "start_page": 13}
  ]
}
"""

images = []
for f in header_files[:40]: # First 40 headers
    try:
        img = PIL.Image.open(f)
        images.append(f"Image {os.path.basename(f)}:")
        images.append(img)
    except:
        continue

# Sending to Gemini
try:
    response = model.generate_content([prompt] + images)
    print(response.text)
except Exception as e:
    print(f"Error: {e}")

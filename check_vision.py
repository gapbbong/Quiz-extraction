import google.generativeai as genai
import PIL.Image
import os

genai.configure(api_key="AIzaSyDIp6TJgOrhtFvcR1TAS8mQDNlDnZfdBys")
model = genai.GenerativeModel('gemini-2.5-flash')

p_img = PIL.Image.open(r'd:\App\Quiz-extraction\session_images\s1\page_1.png')

response = model.generate_content(["이 이미지에서 무슨 내용이 보이는지 한 줄로 요약해줘.", p_img])
print(f"Summary: {response.text}")

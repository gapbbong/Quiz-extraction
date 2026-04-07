import google.generativeai as genai
import PIL.Image
import os

genai.configure(api_key="AIzaSyDIp6TJgOrhtFvcR1TAS8mQDNlDnZfdBys")
model = genai.GenerativeModel('gemini-2.5-flash')

for i in [1, 2]:
    p_img = PIL.Image.open(f'd:\\App\\Quiz-extraction\\session_images\\s1\\page_{i}.png')
    response = model.generate_content(["이 이미지에 있는 문제 번호와 문제 텍스트를 전부 나열해줘.", p_img])
    print(f"--- Page {i} ---")
    print(response.text)

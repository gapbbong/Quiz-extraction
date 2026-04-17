from flask import Flask, request, jsonify, send_from_directory, send_file
from flask_cors import CORS
import json
import os
import shutil
from PIL import Image
import fitz # PyMuPDF

app = Flask(__name__)
CORS(app) # Enable CORS for all routes

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
IMAGES_DIR = os.path.join(OUTPUT_DIR, "images")
SCAN_DIR = os.path.join(BASE_DIR, "scan")
JSON_PATH = os.path.join(OUTPUT_DIR, "ElectricExam_MASTER_DB.json")

@app.route('/')
def index():
    return send_from_directory(OUTPUT_DIR, 'viewer.html')

@app.route('/<path:path>')
def static_proxy(path):
    return send_from_directory(OUTPUT_DIR, path)

@app.route('/api/data', methods=['GET'])
def get_data():
    try:
        with open(JSON_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/update', methods=['POST'])
def update_data():
    try:
        data = request.json
        with open(JSON_PATH, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    # Save file
    filename = file.filename
    # Ensure images dir exists
    os.makedirs(IMAGES_DIR, exist_ok=True)
    file_path = os.path.join(IMAGES_DIR, filename)
    file.save(file_path)
    
    return jsonify({"success": True, "filename": filename})

@app.route('/api/pdf/<filename>')
def serve_pdf(filename):
    return send_from_directory(SCAN_DIR, filename)

@app.route('/api/delete_image', methods=['POST'])
def delete_image():
    try:
        data = request.json
        filename = data.get('filename')
        if not filename:
            return jsonify({"error": "No filename provided"}), 400
            
        file_path = os.path.join(IMAGES_DIR, filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            return jsonify({"success": True, "message": f"Deleted {filename}"})
        else:
            return jsonify({"success": False, "error": "File not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/crop', methods=['POST'])
def crop_image():
    try:
        data = request.json
        source_name = data.get('source') # e.g. page_138.png
        x = data.get('x')
        y = data.get('y')
        w = data.get('w')
        h = data.get('h')
        target_name = data.get('target') # e.g. q123_fig.png

        # 경로 설정 (images_v4 폴더에서 소스 가져오기 등 유동적 처리)
        # 여기서는 편의상 IMAGES_DIR (output/images) 기준으로 함
        # 필요시 source_path를 조정
        source_path = os.path.join(BASE_DIR, "images_v4", source_name)
        if not os.path.exists(source_path):
             source_path = os.path.join(IMAGES_DIR, source_name)
        
        if not os.path.exists(source_path):
             return jsonify({"error": "Source image not found"}), 404

        img = Image.open(source_path)
        cropped = img.crop((x, y, x + w, y + h))
        
        target_path = os.path.join(IMAGES_DIR, target_name)
        cropped.save(target_path)

        return jsonify({"success": True, "filename": target_name})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/process_pdf', methods=['POST'])
def process_pdf():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400
        file = request.files['file']
        page_num = int(request.form.get('page', 1))

        # Save temp PDF
        temp_pdf_path = os.path.join(IMAGES_DIR, "temp_upload.pdf")
        file.save(temp_pdf_path)

        # Extract page
        doc = fitz.open(temp_pdf_path)
        if page_num > len(doc): page_num = 1
        page = doc.load_page(page_num - 1)
        pix = page.get_pixmap(matrix=fitz.Matrix(2,2)) # High DPI
        
        temp_img_name = f"temp_page_{page_num}_{os.getpid()}.png"
        temp_img_path = os.path.join(IMAGES_DIR, temp_img_name)
        pix.save(temp_img_path)
        doc.close()
        
        return jsonify({"success": True, "filename": temp_img_name})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/serve-image')
def serve_image():
    path = request.args.get('path')
    if not path:
        return "No path", 400
    
    # Simple security check (allow only .png, .jpg, .webp)
    if not any(path.lower().endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.webp']):
        return "Invalid file type", 403
        
    try:
        # Normalize path for Windows
        safe_path = os.path.normpath(path)
        print(f"Serving image: {safe_path}")
        if not os.path.exists(safe_path):
            print(f"File not found: {safe_path}")
            return f"File not found: {safe_path}", 404
        return send_file(safe_path)
    except Exception as e:
        print(f"Error serving {path}: {e}")
        return str(e), 500

if __name__ == '__main__':
    port = 5001
    print(f"Server starting at http://localhost:{port}")
    # Disable debug/reloader for stability in background execution
    app.run(host='0.0.0.0', port=port, debug=False, threaded=True)

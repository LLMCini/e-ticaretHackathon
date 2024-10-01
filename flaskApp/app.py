import os
import base64
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
from flask_cors import CORS
import subprocess
from io import BytesIO
from PIL import Image
import uuid

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'webp'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        # Dosya adını güvenli hale getir
        filename = secure_filename(file.filename)
        
        # Dosyanın uzantısını al
        file_ext = os.path.splitext(filename)[1]
        
        # Benzersiz bir isim oluştur
        abcfilename = str(uuid.uuid4()) 
        unique_filename = abcfilename + file_ext
        outputfilename = abcfilename + "_00001_.png"
        # Dosya yolunu oluştur
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        
        # Dosyayı kaydet
        file.save(file_path)

        absolute_file_path = os.path.abspath(file_path)


        env = os.environ.copy()
        env['IMAGE_PATH'] = absolute_file_path
        env['IMAGE_NAME'] = abcfilename
        
        command = ['C:/Users/reg/Downloads/ComfyUI_windows_portable_nvidia/ComfyUI_windows_portable/python_embeded/python.exe',
         'C:/Users/reg/Downloads/ComfyUI_windows_portable_nvidia/ComfyUI_windows_portable/ComfyUI/demo.py', '--output', 'C:/Users/reg/Desktop/flask_project/outputs'
        ]

        try:
           subprocess.run(command, env=env, text=True)
        except subprocess.CalledProcessError as e:
            return jsonify({'error': f'Error in demo.py execution: {str(e)}'}), 500

        output_image_path = "static/" + (app.config['OUTPUT_FOLDER'] + "/" + outputfilename)  # Çıkış dosyası yolu

        # Yanıtı hazırlayın
        return jsonify({
            'api_response': {
                'suggested_title': 'Generated Title',
                'product_description': 'Generated Description',
                'tags': ['tag1', 'tag2'],
                'output_image': output_image_path
            }
        }), 200

    return jsonify({'error': 'File type not allowed'}), 400

if __name__ == '__main__':
    app.run(debug=True)

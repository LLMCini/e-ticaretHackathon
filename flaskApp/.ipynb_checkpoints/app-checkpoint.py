import os
import base64
from flask import Flask, request, jsonify, render_template, make_response
from werkzeug.utils import secure_filename
from flask_cors import CORS
import asyncio
import subprocess
from io import BytesIO
from PIL import Image
import uuid
import time 
import threading
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import json
import torch.backends.cudnn as cudnn

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'static/outputs'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'webp'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

cudnn.benchmark = True
# Global değişkenler
tokenizer = None
model = None

def load_model():
    global tokenizer, model
    model_id = "../../yedek/llamaDPO/model"
    
    tokenizer = AutoTokenizer.from_pretrained(model_id,local_files_only=True)
    
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        torch_dtype=torch.bfloat16,
        device_map="auto",
        low_cpu_mem_usage=True,
    )
# Uygulama başladığında modeli yükle
load_model()

def generate_response(custom_prompt):

    if not isinstance(custom_prompt, str):
        raise ValueError("custom_prompt must be a string")

    initial_messages = [
        {
            "role": "system", 
            "content": f"""## Job Description: Optimized Product Description and Title for E-commerce
                Create an e-commerce product title and description for: user_content
                Write in: Turkish
                1. Product Title (max 60 characters):
                - An SEO-optimized product title based on user_content.
                - Only use the information explicitly mentioned in the description. Do not invent or add any information that is not present in user_content.
                - Add one of these elements to each title: - Unique selling point - Key benefit - Target audience - Product feature -Power word 
                2. Product Description (150-200 words):
                - Highlight key features and benefits
                - Aim for a keyword density of 1-2% for the product name.
                - Technical specifications (if applicable)
                - Mention improved user_content 1 times naturally
                - Use short, clear sentences
                Output format:
                ***Product Title***
                [Generated title]
                ***Product Description***
                [Generated description]"""
        },
        {
            "role": "user", 
            "content": custom_prompt  # Ensure custom_prompt is passed correctly
        }
    ]

    input_ids = tokenizer.apply_chat_template(
        initial_messages,
        add_generation_prompt=True,
        return_tensors="pt"
    ).to(model.device)
    
    terminators = [
        tokenizer.eos_token_id,
        tokenizer.convert_tokens_to_ids("<|eot_id|>")
    ]
    
    with torch.cuda.amp.autocast():
        outputs = model.generate(
            input_ids,
            max_new_tokens=4096,
            eos_token_id=terminators,
            do_sample=True,
            temperature=0.2,
            top_p=0.9,
        )
    
    response = outputs[0][input_ids.shape[-1]:]
    response = tokenizer.decode(response, skip_special_tokens=True)    
    product_name = ""
    product_description = ""
    
    lines = response.split('\n')
    for i, line in enumerate(lines):
        if "Ürün Başlığı" in line and i + 1 < len(lines):
            product_name = lines[i + 1].strip().strip('"')
        if "Ürün Açıklaması" in line and i + 1 < len(lines):
            product_description = ' '.join(lines[i + 1:]).strip()
    
    product_name = " ".join(product_name.split())
    product_description = " ".join(product_description.split())

  
    return [product_name,product_description]

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

def run_background_task(command, env):
    try:
        subprocess.run(command, env=env, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running background task: {e}")

def image_background(absolute_file_path, abcfilename):
    env = os.environ.copy()
    env['IMAGE_PATH'] = absolute_file_path
    env['IMAGE_NAME'] = abcfilename

    command = [
        'python',
        '../ComfyUI/demo.py',
        '--output',
        'static/outputs'
    ]

    thread = threading.Thread(target=run_background_task, args=(command, env))
    thread.start()


        
@app.route('/ver', methods=['POST'])
def ver():
    # Gelen JSON verisinden token bilgisini alıyoruz
    data = request.get_json()
    token = data.get('token')
    
    # Token kontrolü
    if not token:
        return jsonify({"error": "Token is missing"}), 400
    
    # Token'e göre dosya yolunu oluşturuyoruz
    file_path = os.path.join("static/outputs/" + token)  # Örneğin dosya uzantısının .jpg olduğunu varsayıyoruz
    
    # Dosyanın var olup olmadığını kontrol ediyoruz
    if os.path.exists(file_path):
        # Eğer dosya varsa, dosya yolunu döndürüyoruz
        return jsonify({"api_response": {"output_image": file_path}}), 200
    else:
        # Dosya bulunamazsa, 202 kodu ile bekleniyor yanıtını döndürüyoruz
        return jsonify({"message": "File not yet available"}), 202
    

@app.route('/upload', methods=['POST'])
def upload_file():


    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    custom_prompt = request.form.get('inp')
    if not custom_prompt or len(custom_prompt) < 10:  # Minimum 10 karakter olsun gibi bir kontrol
        return jsonify({"error": "Description too short"}), 400
  
    tone_value = request.form.get('tone')
    if tone_value not in ['0', '1']:  # 0 ve 1 dışındaki değerleri reddet
        return jsonify({"error": "Invalid tone option"}), 400



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
        
        final_output = generate_response(custom_prompt)
    

        # Run the background task without waiting for it to finish
        image_background(absolute_file_path, abcfilename)
        # Yanıtı hazırlayın


        return jsonify({
            'api_response': {
                'suggested_title': final_output[0],
                'product_description': final_output[1],
                'token': outputfilename
            }
        }), 200
    return jsonify({'error': 'File type not allowed'}), 400

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=False)

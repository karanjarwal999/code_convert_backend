# app.py
from routes.code_converter import convert_code , debug_code , check_quality , add_css_prefixer
from routes.Pdf_reader import gethub_callback, Pdf_Question
from flask import Flask, request, jsonify,redirect
from dotenv import load_dotenv, find_dotenv
from flask_cors import CORS
import os
import sys

app = Flask(__name__)
CORS(app)

load_dotenv(find_dotenv())

sys.path.append('../..')
sys.stdout.reconfigure(encoding='utf-8')

@app.route('/')
def home_page():
    return "welcome to creative.AI api"

@app.route('/convert_code', methods=['POST'])
def convert_code_route():
    data= request.get_json()
    target_language,current_language,code,api_key = data.values()
    
    converted_code = convert_code(current_language,target_language, code,api_key)
    return jsonify({"Response":converted_code})


@app.route('/check_quality', methods=['POST'])
def check_quality_route():
    data = request.get_json()
    current_language,code,api_key = data.values()    

    quality_result = check_quality(current_language,code,api_key)
    return jsonify({'Response': quality_result})


@app.route('/debug_code', methods=['POST'])
def debug_code_route():
    data = request.get_json()
    current_language,code,api_key = data.values()

    debug_info = debug_code(current_language,code,api_key)
    return jsonify({'Response': debug_info})

@app.route('/css_prefixer', methods=['POST'])
def css_pre_fixer_route():
    data = request.get_json()
    code,api_key = data.values()

    new_code = add_css_prefixer(code,api_key)
    return jsonify({'Response': new_code})


@app.route('/git_login')
def login():
    return redirect(f'https://github.com/login/oauth/authorize?client_id={os.environ.get("GITHUB_CLIENT_ID")}&redirect_uri={os.environ.get("GITHUB_REDIRECT_URI")}&scope=repo')

@app.route('/callback')
def callback():
    code = request.args.get('code')
    return gethub_callback(code)


@app.route('/PDF_QA', methods=['POST'])
def PDF_QA():
    data = request.get_json()
    api_key,question = data.values()
    return Pdf_Question(api_key,question)


@app.route('/PDF_upload', methods=['POST'])
def PDF_uplode_route():
    #  for pdf reader
    DOCS_FOLDER = 'docs'
    app.config['DOCS_FOLDER'] = DOCS_FOLDER

    # Check if the request contains a file
    if 'file' not in request.files:
        return jsonify({'error': 'No file selected'}), 400

    file = request.files['file']

    # Check if the file has a name
    if file.filename == '':
        return jsonify({'error': 'File should have proper name'}), 400

    # Check if the file is a PDF
    if not file.filename.endswith('.pdf'):
        return jsonify({'error': 'Invalid file format. Please upload a PDF file'}), 400

    # Delete any existing PDF in the docs folder
    existing_pdf_path = os.path.join(app.config['DOCS_FOLDER'], 'test.pdf')
    if os.path.exists(existing_pdf_path):
        os.remove(existing_pdf_path)

    # Save the new PDF
    file.save(os.path.join(app.config['DOCS_FOLDER'], 'test.pdf'))
    
    return jsonify({'message': 'File uploaded successfully'})


if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')

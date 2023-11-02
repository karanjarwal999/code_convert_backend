# app.py
import os
from code_converter import convert_code , debug_code , check_quality , add_css_prefixer
from flask import Flask, request, jsonify,redirect
from dotenv import load_dotenv, find_dotenv
from flask_cors import CORS
import requests
import json

app = Flask(__name__)
CORS(app)

load_dotenv(find_dotenv())

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

    response = requests.post(os.environ.get("GITHUB_TOKEN_URL"), data={
        'client_id': os.environ.get("GITHUB_CLIENT_ID"),
        'client_secret': os.environ.get("GITHUB_CLIENT_SECRET"),
        'code': code,
        'redirect_uri': os.environ.get("GITHUB_REDIRECT_URI")
    }, headers={'Accept': 'application/json'})

    if response.status_code == 200:
        access_token = response.json()['access_token']
        # print(os.environ.get('FRONTEND_URL'))
        return redirect(f"{os.environ.get('FRONTEND_URL')}?token={access_token}")
    else:
        return 'Error fetching access token', 400


@app.route('/get_file_content', methods=['POST'])
def get_file():
    data = request.get_json()
    username,repo_name,file_path,branch,isprivate = data.values()
    if not isprivate:
        try:
            raw_url = f'https://raw.githubusercontent.com/{username}/{repo_name}/{branch}/{file_path}'
            print(raw_url)
            response = requests.get(raw_url)

            if response.status_code == 200:
                content = response.text
                return jsonify({'content': content})
            else:
                return jsonify({'error': f'Error fetching file: {response.status_code}'}), response.status_code

        except Exception as e:
            return jsonify({'error': str(e)}), 500
    return jsonify({'error': "this is private repository"})

if __name__ == '__main__':
    app.run(debug=True)

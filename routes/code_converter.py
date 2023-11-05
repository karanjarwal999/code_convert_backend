from langchain.llms import OpenAI
from openai import OpenAIError

def convert_code(current_language,target_language, code,api_key):
    try:    
        llm = OpenAI(openai_api_key=api_key)
        return llm.predict(f"convert the following {current_language} code into {target_language} : {code}")
    except OpenAIError as e:
        return f'\n\n\n{str(e)}'

def check_quality(current_language,code,api_key):
    try:
        llm = OpenAI(openai_api_key=api_key)
        return llm.predict(f"perform a quality check on follwing {current_language} code give rating explation why you gave this rating at last suggest changes : {code}")
    except OpenAIError as e:
        return f'\n\n\n{str(e)}'

def debug_code(current_language,code,api_key):
    try:
        llm = OpenAI(openai_api_key=api_key)
        return llm.predict(f" perform a debug on following {current_language} code and suggest changes : {code}")
    except OpenAIError as e:
        return f'\n\n\n{str(e)}'

def add_css_prefixer(code,api_key):
    try:
        llm = OpenAI(openai_api_key=api_key)
        return llm.predict(f"return the css code by adding all css prefixers and if its node valid css return appropriate response : {code}")
    except OpenAIError as e:
        return f'\n\n\n{str(e)}'

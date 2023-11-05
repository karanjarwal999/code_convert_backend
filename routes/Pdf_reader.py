from flask import jsonify,redirect
import requests
import os
import shutil

#  for pdf reader
import openai
from openai import OpenAIError
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI

def gethub_callback(code):
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


def Pdf_Question(api_key,question):
    try:

        openai.api_key=api_key
    
        # step 1 : getting a pdf file
        loader = PyPDFLoader('./docs/test.pdf')
        pages = loader.load()

        # step2 : dividing it into chunks
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
        )  

        docs = splitter.split_documents(pages)

        # step 3: embeddings 
        embedding = OpenAIEmbeddings(openai_api_key=api_key)

        persist_directory ='docs/chroma/'

        vectordb = Chroma.from_documents(
            documents=docs,
            embedding=embedding,
            persist_directory=persist_directory,
        )

        print(vectordb._collection.count())
        # every time it run it add it in croma so its size every time , so need to clear
        # print(question)
        # ans = vectordb.similarity_search(question,k=1)
        # print(ans[0].page_content)


        # step4 : Retrival
        llm= ChatOpenAI(model_name='gpt-3.5-turbo',temperature=0,openai_api_key=api_key)

        qa_chain = RetrievalQA.from_chain_type(
            llm,
            retriever=vectordb.as_retriever()
        )

        result= qa_chain({"query":question})
        return result['result']
    except OpenAIError as e:
        return f'\n\n\n{str(e)}'

    # before openai it was returning whole chunk but now its giving only ans 
    # ex.
    # before : Virat Kohli, born on No vember 5, 1988, in Delhi, India, stands as one of the most iconic ﬁgur es
    # after : The birth date of Virat Kohli is November 5, 1988.
    
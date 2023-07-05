# Healthcare

import os
import base64
from constants import openai_key
from langchain.llms import OpenAI
from langchain import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from PyPDF2 import PdfReader
import streamlit as st

os.environ['OPENAI_API_KEY'] = openai_key

#streamlit framwork

def add_logo_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    style = '''
            <style>
            .logo {
                position: absolute;
                top: -50px;
                left: -247px;
                z-index: 0;
            }

            </style>
            '''
    logo = f'<img class="logo" src="data:image/png;base64,{encoded_string}" width="120">'

    st.markdown(style, unsafe_allow_html=True)

    st.empty().markdown(logo, unsafe_allow_html=True)

add_logo_from_local(os.path.join(os.path.dirname(__file__), "images\logo.png"))
  

st.title('Entity Extractor')

with st.form('my_form'):
  uploaded_pdf = st.file_uploader(label='Upload PDF:', type='pdf')
  submitted = st.form_submit_button('Submit')

def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"jpg"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )
add_bg_from_local('images\BG_IMAGE3.jpg')

#Promp Template

template = '''You are an asssistant whose goal is to extract the following entitie'''
entity_prompt = PromptTemplate(
    input_variables=['passage'],
    template='''Given Passage:
    "{passage}"
    
    Find the following entities:
    1. Percentage Entity
    2. Corporate Entity
    2. Monetary Entity
    3. Location Entity
    4. Date Entity
    '''
)


llm = OpenAI(temperature=0)
chain = LLMChain(llm=llm, prompt=entity_prompt,
                 verbose=True, output_key='entity')

if uploaded_pdf is not None:
    pdf_reader = PdfReader(uploaded_pdf)

    text = ''
    for i, page in enumerate(pdf_reader.pages):
        content = page.extract_text()
        if content:
            text += content 
        
    text_splitter = CharacterTextSplitter(
    separator = "\n",
    chunk_size=5000,
    chunk_overlap=200,
    length_function=len
)
    splitted_texts = text_splitter.split_text(text)

    if splitted_texts:
        st.write(chain.run(splitted_texts))


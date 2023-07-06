import os
import base64
import PyPDF2
from langchain.llms import OpenAI
from langchain import PromptTemplate
from langchain.text_splitter import CharacterTextSplitter 
import streamlit as st
from constants import openai_key
from langchain.chains import LLMChain

    
os.environ['OPENAI_API_KEY'] = openai_key

#streamlit framework
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

with st.form('my_form'):
  uploaded_pdf = st.file_uploader(label='Upload PDF:', type='pdf')
  submitted = st.form_submit_button('Submit')

#langchain 
if submitted and uploaded_pdf is not None:
    def split_text(text):
        try:
            text_splitter = CharacterTextSplitter(
            separator='\n',
            chunk_size = 1000,
            chunk_overlap = 200,
            length_function = len)

            splitted_text = list(text_splitter.split_text(text))
            return [{'text':chunk} for chunk in splitted_text]
        except Exception as e:
                print(f"Error splitting the text: {str(e)}")
                return[]


    def read_pdf(file):
        try:
            pdf_reader = PyPDF2.PdfReader(file)
            num_pages = pdf_reader.getNumPages(page_num)

            text=''
            for page_num in range(num_pages):
                page = pdf_reader.getPage(page_num)
                text += page.extract_text()
            return text
        except:
            return ''
    pdf_text = read_pdf(uploaded_pdf)
    chunk_text = split_text(pdf_text)

    template = '''You are an asssistant whose goal is to extract the following entitie
            Given text:
            "{passage}"
            
            Find the following entities:
            1. Percentage Entity
            2. Corporate Entity
            2. Monetary Entity
            3. Location Entity
            4. Date Entity
            '''

    entity_prompt = PromptTemplate(
            input_variables=['passage'],
            template=template
        )

    llm = OpenAI(temperature=0)
    chain = LLMChain(llm=llm, prompt=entity_prompt,
                        verbose=True, output_key='entity')



    #Extracting Entities from each text chunk


    st.write(chain.run(chunk_text)) 

    


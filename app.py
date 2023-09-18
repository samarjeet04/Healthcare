import os
import base64
#from constants import openai_key
from langchain.llms import OpenAI
from langchain import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain
from langchain.memory import ConversationBufferMemory
import streamlit as st

openai_key = ''
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
  

st.title('Health Care App')

with st.form('my_form'):
  input_text = st.text_input('Enter the diagnosis:', )
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
add_bg_from_local('images\BG_IMAGE.jpg')



#Prompt Template1
first_input_prompt = PromptTemplate(
    input_variables=['diagnosis_name'],
    template='give the ICD Code of {diagnosis_name}'
    )

#Memory
icd_code_memory = ConversationBufferMemory(input_key='diagnosis_name', memory_key='chat_history')
descr_memory = ConversationBufferMemory(input_key='icd_code', memory_key='description_history')

#OPENAI LLMS
llm = OpenAI(temperature=0.1)
chain1 = LLMChain(llm=llm, prompt=first_input_prompt, verbose=True,
                   output_key='icd_code', memory=icd_code_memory)

#Prompt Template2
second_input_prompt = PromptTemplate(
    input_variables=['icd_code'],
    template='Tell me about {icd_code}'
)

chain2 = LLMChain(llm=llm, prompt=second_input_prompt, verbose=True, 
                  output_key='description', memory=descr_memory)



parent_chain = SequentialChain(chains=[chain1,chain2], input_variables=['diagnosis_name'],
                                output_variables=['icd_code', 'description'], verbose=True)

if input_text:
    st.write(parent_chain({input_text}))

    with st.expander('Diagnosis_name'):
        st.info(icd_code_memory)

    with st.expander('Description'):
        st.info(descr_memory)

import os
import base64
import json
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

st.title('Entity Identifier')

with st.form('my_form'):
  uploaded_pdf = st.file_uploader(label='Upload PDF:', type='pdf')
  submitted = st.form_submit_button('Submit')
  

template = '''You are an asssistant whose goal is to extract the following entities:
         Given text:
            "{passage}"
            
        Find the following entities:
        1. Percentage Entity
        2. Corporate Entity
        2. Monetary Entity
        3. Location Entity
        4. Date Entity

        Format the output as JSON with the following information:
        Entity Name,
        Entity Type,
        Start Index of Entity,
        End Index of Entity

        strictly use the following keys in json
        Entity_Name,
        Entity_Type,
        Start_Index,
        End_Index

        '''

entity_prompt = PromptTemplate(
        input_variables=['passage'],
        template=template
        )
llm = OpenAI(temperature=0)
chain = LLMChain(llm=llm, prompt=entity_prompt,
                        verbose=True, output_key='entity')

  
def read_pdf(file): 
    pdf_reader = PyPDF2.PdfReader(file) 
    num_pages = len(pdf_reader.pages) 
    text = '' 
    for page_num in range(num_pages): 
        page = pdf_reader.pages[page_num] 
        text += page.extract_text() 
    return text

def split_text(text): 
    text_splitter = CharacterTextSplitter(
        separator="\n", 
        chunk_size=800, 
        chunk_overlap=200, 
        length_function=len) 
    splitted_texts = text_splitter.split_text(text) 
    return splitted_texts

if submitted and uploaded_pdf: 
    pdf_text = read_pdf(uploaded_pdf)
    # Split the text into chunks    
    text_chunks = split_text(pdf_text)

# Extract entities from each text chunk
    entities = []
    for chunk in text_chunks:
        result = chain.run(passage =chunk)
        entities.append(result)
        
    json_data = json.dumps(entities, indent=4)

    st.download_button(
        label="Download JSON File",
        data=json_data.encode("utf-8"),
        file_name="extracted_entities.json",
        mime='application/json'
    )



import streamlit as st

# Define the function for the first page (Name, Age, Location input)
def get_user_info():
    st.title("User Information")
    name = st.text_input("Enter your name")
    age = st.number_input("Enter your age", min_value=0, max_value=150, step=1)
    location = st.text_input("Enter your location")
    
    if st.button("Submit"):
        # Store the user information in session state
        st.session_state.name = name
        st.session_state.age = age
        st.session_state.location = location

        # Direct to the second page (show_name)
        st.session_state.current_page = "show_name"

# Define the function for the second page (Display name)
def show_name():
    st.title("Hello!")
    st.write(f"Your name: {st.session_state.name}")
    col1, col2 = st.columns(2)
    if col1.button("Back"):
        # Go back to the first page (get_user_info)
        st.session_state.current_page = "get_user_info"
    if col2.button("Next Page"):
        # Direct to the third page (show_age)
        st.session_state.current_page = "show_age"

# Define the function for the third page (Display age)
def show_age():
    st.title("Your Age")
    st.write(f"Your age: {st.session_state.age}")
    col1, col2 = st.columns(2)
    if col1.button("Back"):
        # Go back to the second page (show_name)
        st.session_state.current_page = "show_name"
    if col2.button("Next Page"):
        # Direct to the fourth page (show_location)
        st.session_state.current_page = "show_location"

# Define the function for the fourth page (Display location)
def show_location():
    st.title("Your Location")
    st.write(f"Your location: {st.session_state.location}")
    if st.button("Back"):
        # Go back to the third page (show_age)
        st.session_state.current_page = "show_age"

# Main app
def main():
    # Initialize session state variables
    if "name" not in st.session_state:
        st.session_state.name = None

    if "age" not in st.session_state:
        st.session_state.age = None

    if "location" not in st.session_state:
        st.session_state.location = None

    if "current_page" not in st.session_state:
        st.session_state.current_page = "get_user_info"

    if st.session_state.current_page == "get_user_info":
        get_user_info()
    elif st.session_state.current_page == "show_name":
        show_name()
    elif st.session_state.current_page == "show_age":
        show_age()
    else:
        show_location()

if __name__ == "__main__":
    main()












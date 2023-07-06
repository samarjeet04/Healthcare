# Healthcare

import os
import base64
import streamlit as st
import PyPDF2
from langchain.llms import OpenAI
from langchain import PromptTemplate
from langchain.chains import LLMChain
from langchain.splitter import CharacterTextSplitter

os.environ['OPENAI_API_KEY'] = openai_key

# Streamlit framework
# ... (Existing code)

# Prompt Template
# ... (Existing code)

llm = OpenAI(temperature=0)
chain = LLMChain(llm=llm, prompt=entity_prompt, verbose=True, output_key='entity')

# Splitting the text using CharacterTextSplitter
def split_text(text):
    text_splitter = CharacterTextSplitter(separator="\n", chunk_size=8000, chunk_overlap=200, length_function=len)
    splitted_texts = text_splitter.split_text(text) if text else []
    return splitted_texts

# Read the PDF
def read_pdf(file):
    try:
        pdf_reader = PyPDF2.PdfReader(file)
        num_pages = len(pdf_reader.pages)
        text = ''
        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
        return text
    except:
        return ''

st.title('Entity Extractor')

# Upload PDF and process
with st.form('my_form'):
    uploaded_pdf = st.file_uploader(label='Upload the PDF', type='pdf')
    submitted = st.form_submit_button('Submit')

if submitted and uploaded_pdf:
    pdf_text = read_pdf(uploaded_pdf)

    if pdf_text:
        # Split the text into chunks
        text_chunks = split_text(pdf_text)

        if text_chunks:
            # Extract entities from each text chunk
            entities = []
            for chunk in text_chunks:
                chunk_entities = chain.run(passage=chunk['text'])
                entities.extend(chunk_entities)

            # Display entities
            st.subheader('Extracted Entities')
            for entity in entities:
                st.text(f'Entity: {entity["entity"]}, Type: {entity["type"]}, Start: {entity["start"]}, End: {entity["end"]}')
        else:
            st.text('Unable to split the text into chunks. Please try again with a different PDF.')
    else:
        st.text('Invalid or empty PDF file. Please try again.')

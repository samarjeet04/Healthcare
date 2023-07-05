# Healthcare

import os
import streamlit as st
from langchain.llms import OpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.document_loaders import PyPDFLoader
from langchain.vectorstores import Chroma
from langchain.agents.agent_toolkits import (
    create_vectorstore_agent,
    VectorStoreToolkit,
    VectorStoreInfo
)
from langchain.prompts import PromptTemplate

# Set API key for OpenAI Service
os.environ['OPENAI_API_KEY'] = 'youropenaiapikeyhere'

# Create instance of OpenAI LLM
llm = OpenAI(temperature=0.1, verbose=True)
embeddings = OpenAIEmbeddings()

# Create vectorstore info object
vectorstore_info = VectorStoreInfo(
    name="pdf_documents",
    description="PDF documents",
    vectorstore=None
)
toolkit = VectorStoreToolkit(vectorstore_info=vectorstore_info)

# Create end-to-end LC
agent_executor = create_vectorstore_agent(llm=llm, toolkit=toolkit, verbose=True)

# Prompt template
template = PromptTemplate(
    input_variables=['passage'],
    template='''Given Passage: "{passage}"

Find the following entities:
1. Percentage Entity
2. Corporate Entity
3. Monetary Entity
4. Location Entity
5. Date Entity
'''
)

# Function to extract entities from PDF
def extract_entities_from_pdf(pdf_path):
    # Create and load PDF Loader
    loader = PyPDFLoader(pdf_path)
    pages = loader.load_and_split()

    # Load documents into vector database (ChromaDB)
    store = Chroma.from_documents(pages, embeddings, collection_name='pdf_documents')
    toolkit.update_vectorstore(store)

    # Get the text content of the PDF
    text_content = ''.join([page.page_content for page in pages])

    # Generate the prompt using the template and the PDF content
    generated_prompt = template.generate(passage=text_content)

    # Run the generated prompt through the LC model
    response = agent_executor.run(generated_prompt)

    # Extract entities from the response metadata
    entities = response['metadata']['entities']
    percentage_entities = [entity['value'] for entity in entities if entity['type'] == 'PERCENTAGE']
    corporate_entities = [entity['value'] for entity in entities if entity['type'] == 'CORPORATE']
    monetary_entities = [entity['value'] for entity in entities if entity['type'] == 'MONEY']
    location_entities = [entity['value'] for entity in entities if entity['type'] == 'LOCATION']
    date_entities = [entity['value'] for entity in entities if entity['type'] == 'DATE']

    # Return the extracted entities
    return percentage_entities, corporate_entities, monetary_entities, location_entities, date_entities

# Streamlit app
st.title('🦜🔗 GPT Investment Banker')

with st.form('my_form'):
    uploaded_pdf = st.file_uploader(label='Upload PDF:', type='pdf')
    submitted = st.form_submit_button('Submit')

if submitted and uploaded_pdf is not None:
    # Save the uploaded PDF file
    with open('uploaded_pdf.pdf', 'wb') as f:
        f.write(uploaded_pdf.getvalue())

    # Extract entities from the uploaded PDF
    percentage_entities, corporate_entities, monetary_entities, location_entities, date_entities = extract_entities_from_pdf('uploaded_pdf.pdf')

    # Display the extracted entities
    if percentage_entities:
        st.write("Percentage Entities:")
        st.write(percentage_entities)

    if corporate_entities:
        st.write("Corporate Entities:")
        st.write(corporate_entities)

    if monetary_entities:
        st.write("Monetary Entities:")
        st.write(monetary_entities)

    if location_entities:
        st.write("Location Entities:")
        st.write(location_entities)

    if date_entities:
        st.write("Date Entities:")
        st.write(date_entities)

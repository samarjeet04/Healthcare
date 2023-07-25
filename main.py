import os
import base64
import json
import PyPDF2
import streamlit as st
from langchain.llms import OpenAI
from langchain import PromptTemplate
from langchain.text_splitter import CharacterTextSplitter 
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

add_logo_from_local(os.path.join(os.path.dirname(__file__), "images\logo.png"))
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
chain = LLMChain(llm=llm, prompt=entity_prompt, verbose=True, output_key='entity')

  
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
        result = chain.run(passage=chunk)
        entities.append(result)

    json_data = json.dumps(entities, indent=4)

    st.download_button(
        label="Download JSON File",
        data=json_data.encode("utf-8"),
        file_name="extracted_entities.json",
        mime='application/json'
    )

    st.subheader('Extracted Entities')
progress_bar = st.progress(0)  # Initialize the progress bar

for i, entity in enumerate(entities, 1):
    with st.expander(f'Entity {i}', style='background-color: white'):
        st.json(entity)
    progress = i / len(entities)  # Calculate the progress as a percentage
    progress_bar.progress(progress)  # Update the progress bar





#pie chart
import requests
import base64
import json

# Define the Kibana server URL and API key credentials
kibana_url = "http://localhost:5601"
api_key_id = ""
api_key = ""

# Encode the API key ID and key in Base64 format
api_key_encoded = base64.standard_b64encode(f"{api_key_id}:{api_key}".encode("utf-8")).decode("utf-8")


# Function to send requests to the Kibana API using the API key for authentication
def send_kibana_request(method, endpoint, data=None):
    headers = {
        "Authorization": f"ApiKey {api_key_encoded}",
        "kbn-xsrf": "true"
    }
    url = f"{kibana_url}{endpoint}"

    if method == "GET":
        response = requests.get(url, headers=headers)
    elif method == "POST":
        response = requests.post(url, headers=headers, json=data)
    elif method == "PUT":
        response = requests.put(url, headers=headers, json=data)
    elif method == "DELETE":
        response = requests.delete(url, headers=headers)
    else:
        raise ValueError("Invalid HTTP method.")

    return response

def create_pie_chart(index_pattern_id):
    # Define the endpoint for creating a new visualization
    endpoint = "/api/saved_objects/visualization"

    # Create the visualization configuration for the pie chart
    visualization_config = {
        "attributes": {
            "title": "Pie Chart",
            "visState": json.dumps({
                "type": "pie",
                "params": {
                    "addTooltip": True,
                    "addLegend": True,
                    "legendPosition": "right",
                    "isDonut": False,
                    "labels": {
                        "show": True,
                        "values": True,
                        "last_level": True,
                        "truncate": 100
                    },
                    "dimension": {
                        "accessor": 0,
                        "formatFn": None,
                        "params": {},
                        "aggType": "count"
                    },
                    "metric": {
                        "accessor": 1,
                        "formatFn": None,
                        "params": {}
                    },
                    "bucket": {
                        "accessor": 2,
                        "formatFn": None,
                        "params": {
                            "field": "customer_gender",
                            "size": 5,
                            "order": "desc",
                            "orderBy": "_key"
                        },
                        "aggType": "terms"
                    }
                },
                "aggs": [
                    {
                        "id": "2",
                        "type": "terms",
                        "schema": "segment",
                        "params": {
                            "field": "customer_gender",
                            "size": 5,
                            "order": {
                                "_key": "desc"
                            }
                        }
                    },
                    {
                        "id": "1",
                        "type": "cardinality",
                        "schema": "metric",
                        "params": {
                            "field": "order_date"
                        }
                    },
                    {
                        "id": "3",
                        "type": "terms",
                        "schema": "bucket",
                        "params": {
                            "field": "order_date",
                            "size": 0,
                            "order": {
                                "_key": "desc"
                            }
                        }
                    }
                ],
                "listeners": {}
            }),
            "uiStateJSON": "{}",
            "description": "",
            "version": 1,
            "kibanaSavedObjectMeta": {
                "searchSourceJSON": json.dumps({
                    "index": index_pattern_id,
                    "query": {
                        "query": "",
                        "language": "kuery"
                    },
                    "filter": []
                })
            }
        }
    }

    # Send the POST request to create the visualization
    response = send_kibana_request("POST", endpoint, data=visualization_config)

    if response.status_code == 200:
        print("Pie chart visualization created successfully!")
    else:
        print("Failed to create pie chart visualization. Status code:", response.status_code)
        print("Error message:", response.text)

# Your index pattern ID (replace this with the correct ID of your index pattern)
index_pattern_id = "kibana_sample_data_ecommerce"

# Call the function to create the pie chart visualization
create_pie_chart(index_pattern_id)


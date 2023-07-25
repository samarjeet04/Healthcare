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





#bar chart
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

    print("API Request:")
    print("Method:", method)
    print("Endpoint:", endpoint)
    print("Data:", data)

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

# Function to create a bar chart visualization with the provided aggregation query
def create_histogram_bar_chart(index_pattern_id):
    # Define the endpoint for creating a new visualization
    endpoint = "/api/saved_objects/visualization"

    # Create the visualization configuration for the histogram bar chart
    visualization_config ={
    "attributes": {
        "title": "Records Count by Day of the Week",
        "visState": json.dumps({
            "type": "histogram",
            "params": {
                "addLegend": True,
                "addTimeMarker": False,
                "addTooltip": True,
                "defaultYExtents": False,
                "legendPosition": "right",
                "scale": "linear",
                "setYExtents": False,
                "shareYAxis": True,
                "times": [],
                "yAxis": {
                    "id": "1",
                    "type": "metrics",
                    "schema": "metric",
                    "params": {
                        "field": "day_of_week_i",
                        "customLabel": "Count",
                        "orderAgg": "2",
                        "orderBy": "1"
                    }
                }
            },
            "aggs": [
                {
                    "id": "2",
                    "type": "count",
                    "schema": "metric",
                    "params": {}
                },
                {
                    "id": "3",
                    "type": "histogram",
                    "schema": "segment",
                    "params": {
                        "field": "day_of_week_i",
                        "interval": 1,
                        "min_doc_count": 0
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
                "index": "kibana_sample_ecommerce_data",
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
        print("Histogram bar chart visualization created successfully!")
    else:
        print("Failed to create histogram bar chart visualization. Status code:", response.status_code)
        print("Error message:", response.text)

# Your index pattern ID (replace this with the correct ID of your index pattern)
index_pattern_id = "kibana_sample_data_ecommerce"

# Call the function to create the histogram bar chart visualization
create_histogram_bar_chart(index_pattern_id)

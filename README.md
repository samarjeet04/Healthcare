#HEALTHCARE



import os
import base64
import pandas as pd
import streamlit as st
from langchain.llms import OpenAI
from langchain import PromptTemplate
from langchain.text_splitter import CharacterTextSplitter 
from langchain.agents import create_pandas_dataframe_agent
from constants import openai_key
from langchain.chains import LLMChain


os.environ['OPENAI_API_KEY'] = openai_key

#streamlit framework

st.title('**Issue Severity**')

with st.form('my_form'):
    uploaded_csv = st.file_uploader(label='Upload CSV:', type='csv')
    submitted = st.form_submit_button('Submit')
    if not uploaded_csv:
        st.stop()
    
    data = pd.read_csv(uploaded_csv)

    agent = create_pandas_dataframe_agent(OpenAI(temperature=0), data, verbose=True)



    template = ''' You are an assistant whose goals are as following:
               
               1. Precisely read the column "Issue Description" in the CSV file.
               2. Classify the issue to a primary impacted line of business and issue severity, this should 
                  done for each issue in the CSV file.
               3. Create a tabular data having 2 columns, these columns will contain Primary Impacted LOB and Issue Severity 
                  corresponding to the issue described in the CSV.

    '''

    if submitted:
        insights = agent.run(template)
        st.write(insights)

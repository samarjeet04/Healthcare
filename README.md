# Healthcare

import requests

import json

import streamlit as st





 # how to import this function in streamlit code, add this at top: from API_call_to_IICS import api_call_iics

def api_call_iics( username, password):

    # Define the API endpoint and job details

    session_url = ""

    #session_url =  ""

    api_url = ""

               




    # Define the request payload

    payload1 = {

        "username": username,

        "password": password

    }




    st.write(payload1)




    response = requests.post(session_url, json=payload1, headers={"Authorization":"Acces Token"})




    if response.status_code==200:

        st.write("Response",response.json())

        response_data = response.json()

        IDS_SESSION_ID = response_data.get("sessionId")

        st.success("Login API call successful." ,icon="✅")#,IDS_SESSION_ID, " generated")

    else:

        st.error("Login API call failed")




    payload2 = {

            "Content-Type": "application/json",

            "Accept": "application/json",

            "IDS-SESSION-ID": IDS_SESSION_ID

            }

   

    st.write(payload2)




    #response2 = requests.post(api_url, json=payload2, headers={"Authorization":"Acces Token"})




    response2 = requests.request("POST", api_url, headers=payload2)




    if response2.status_code==200:

        st.success("Job triggered successfully.",icon="✅")

        st.write("Response2",response2.json())

    else:

        st.error("API call failed")




#streamlit framework




st.title(':white[PDM Execution Engine]')

#st.markdown('WAB.jpg')




with st.form('myform'):

    input_text = st.text_input('Enter the User Name')

    password = st.text_input("Enter a password", type="password")

    submitted = st.form_submit_button('Login')




    if submitted:

        if input_text and password:

            api_call_iics(username=input_text, password=password)

        else:

            st.warning("Please enter all the required details")

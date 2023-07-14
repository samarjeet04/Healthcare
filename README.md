# Healthcare

import requests
import json
import streamlit as st

# Function to make the API call to IICS
def api_call_iics(username, password):
    # Define the API endpoint and job details
    session_url = ""
    api_url = ""

    # Define the request payload
    payload1 = {
        "username": username,
        "password": password
    }
    
    response = requests.post(session_url, json=payload1, headers={"Authorization": "Access Token"})

    if response.status_code == 200:
        response_data = response.json()
        IDS_SESSION_ID = response_data.get("sessionId")
        return IDS_SESSION_ID
    else:
        return None

# Streamlit app
st.title('PDM Execution Engine')

# Page 1: Login
if 'logged_in' not in st.session_state:
    st.header('Login')
    with st.form('login_form'):
        username = st.text_input('Enter the User Name')
        password = st.text_input('Enter a password', type='password')
        submitted = st.form_submit_button('Login')

    if submitted:
        if username and password:
            IDS_SESSION_ID = api_call_iics(username, password)
            if IDS_SESSION_ID:
                st.success('Login successful.')
                st.session_state['logged_in'] = True
                st.session_state['IDS_SESSION_ID'] = IDS_SESSION_ID
            else:
                st.error('Login failed. Please check your credentials.')
        else:
            st.warning('Please enter all the required details.')

# Page 2: API Call
if 'logged_in' in st.session_state:
    if st.session_state['logged_in']:
        st.header('API Call')
        st.write('Welcome to the second page.')

        # Make the second API call using IDS_SESSION_ID
        IDS_SESSION_ID = st.session_state['IDS_SESSION_ID']
        payload2 = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "IDS-SESSION-ID": IDS_SESSION_ID
        }
        response2 = requests.request("POST", api_url, headers=payload2)

        if response2.status_code == 200:
            st.success('API call successful.')
            st.write('Response2:', response2.json())
        else:
            st.error('API call failed.')

# Error message if not logged in
if 'logged_in' not in st.session_state:
    st.error('Please log in to continue.')





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


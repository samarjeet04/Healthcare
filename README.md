# Healthcare

# Displaying the extracted entities
    st.write("Extracted Entities:")
    for chunk in result:
        if 'entity' in chunk:
            st.write(chunk['entity'])

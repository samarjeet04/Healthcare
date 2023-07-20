# Healthcare



# Display entities
    st.subheader('Extracted Entities')
    for entity in entities:
        st.text(f'Entity: {entity}, Type: {chain.output_key}')

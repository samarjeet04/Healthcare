# Healthcare

result = chain.run(chunk_text)

    # Displaying the extracted entities
    st.write("Extracted Entities:")
    for chunk in result:
        if 'entity' in chunk:
            entities = chunk['entity']
            for entity_type, entity_values in entities.items():
                st.write(f"{entity_type}:")
                for value in entity_values:
                    st.write(f"- {value}")

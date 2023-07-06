# Healthcare

all_entities = []

    for chunk in chunk_text:
        result = chain.run(inputs=[chunk])
        entities = result.get('entity', {})
        all_entities.append(entities)

    # Displaying the extracted entities
    st.write("Extracted Entities:")

    for entities in all_entities:
        for entity_type, entity_values in entities.items():
            st.write(f"{entity_type}:")
            for value in entity_values:
                st.write(f"- {value}")

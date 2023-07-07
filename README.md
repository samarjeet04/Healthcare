# Healthcare

for chunk in text_chunks:
    result = chain.run(passage=chunk)
    for entity in result:
        entity_info = {
            "entity_type": chain.output_key,
            "page_number": 1,  # You can modify this based on your implementation
            "start_index": entity["start"],
            "end_index": entity["end"],
            "entity_text": entity["text"]
        }
        extracted_entities.append(entity_info)

# Healthcare

# Splitting the text using CharacterTextSplitter
def split_text(text):
    text_splitter = CharacterTextSplitter(separator="\n", chunk_size=8000, chunk_overlap=200, length_function=len)
    splitted_texts = text_splitter.split_text(text)
    return splitted_texts

# Read the PDF
def read_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    num_pages = len(pdf_reader.pages)
    text = ''
    for page_num in range(num_pages):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
    return text

st.title('Entity Extractor')

# Upload PDF and process
with st.form('my_form'):
    uploaded_pdf = st.file_uploader(label='Upload the PDF', type='pdf')
    submitted = st.form_submit_button('Submit')

if submitted and uploaded_pdf:
    pdf_text = read_pdf(uploaded_pdf)

    # Split the text into chunks
    text_chunks = split_text(pdf_text)

    # Extract entities from each text chunk
    entities = []
    for chunk in text_chunks:
        chunk_entities = chain.run(passage=chunk['text'])
        entities.extend(chunk_entities)

    # Display entities
    st.subheader('Extracted Entities')
    for entity in entities:
        st.text(f'Entity: {entity["entity"]}, Type: {entity["type"]}, Start: {entity["start"]}, End: {entity["end"]}')

with st.form('my_form'):
  uploaded_pdf = st.file_uploader(label='Upload PDF:', type='pdf')
  submitted = st.form_submit_button('Submit')
  

template = '''You are an asssistant whose goal is to extract the following entities:
         Given text:
            "{passage}"
            
        Find the following entities:
        1. Percentage Entity
        2. Corporate Entity
        2. Monetary Entity
        3. Location Entity
        4. Date Entity

        Format the output as JSON with the following keys:
        Entity Name:
        Entity Type:
        Start Index of Entity:
        End Index of Entity: 

        '''

entity_prompt = PromptTemplate(
        input_variables=['passage'],
        template=template
        )
llm = OpenAI(temperature=0)
chain = LLMChain(llm=llm, prompt=entity_prompt,
                        verbose=True, output_key='entity')

  
def read_pdf(file): 
    pdf_reader = PyPDF2.PdfReader(file) 
    num_pages = len(pdf_reader.pages) 
    text = '' 
    for page_num in range(num_pages): 
        page = pdf_reader.pages[page_num] 
        text += page.extract_text() 
    return text

def split_text(text): 
    text_splitter = CharacterTextSplitter(
        separator="\n", 
        chunk_size=800, 
        chunk_overlap=200, 
        length_function=len) 
    splitted_texts = text_splitter.split_text(text) 
    return splitted_texts

if submitted and uploaded_pdf: 
    pdf_text = read_pdf(uploaded_pdf)
    # Split the text into chunks
    text_chunks = split_text(pdf_text)

# Extract entities from each text chunk
    entities = []
    for chunk in text_chunks:
        result = chain.run(passage =chunk)
        entities.append(result)

# Display entities
    st.subheader('Extracted Entities')
    for entity in entities:
        st.text(f'Entity: {entity}, Type: {chain.output_key}')







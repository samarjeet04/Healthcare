import os
import re
import base64
import torch
import langchain
import streamlit as st
import PyPDF2
from langchain.llms import HuggingFacePipeline
from langchain.text_splitter import CharacterTextSplitter 
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig, pipeline



st.title("**Resume Ranker**")

with st.form('my_form'):
    job_description = st.text_area(label="Enter the Job Description")
    uploaded_resume = st.file_uploader(label='Upload The Resume/CV', type="pdf", accept_multiple_files=True)
    submitted = st.form_submit_button('submit')



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




model_id = 'vilsonrodrigues/falcon-7b-instruct-sharded'


quantization_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_use_double_quant=True,
)

model_4bit = AutoModelForCausalLM.from_pretrained(
        model_id, 
        device_map="auto",
        quantization_config=quantization_config,
        )

tokenizer = AutoTokenizer.from_pretrained(model_id)
    
pipeline = pipeline(
        "text-generation",
        model=model_4bit,
        tokenizer=tokenizer,
        use_cache=True,
        device_map="auto",
        max_length=296,
        do_sample=True,
        top_k=10,
        num_return_sequences=1,
        eos_token_id=tokenizer.eos_token_id,
        pad_token_id=tokenizer.eos_token_id,
)
template = '''You are an assistant whose goal is to rank resumes {passage} on the basis of the job description.
            The job description is the user input.

            The scores of the resumes should on the basis of:
            
            1. Skills
            2. Experience 
            3. Extraordianry Achievments
            
            The ranking should be done on the basis of the scores'''


prompt = PromptTemplate(
    input_variables=['passage'],
    template=template
)

llm = HuggingFacePipeline(pipeline=pipeline)

chain = LLMChain(prompt=prompt, llm=llm)


if submitted and uploaded_resume:
    pdf_text = read_pdf(uploaded_resume)
    # Split the text into chunks
    text_chunks = split_text(pdf_text)

    # Rank resumes based on the scores generated by the LLM
    ranked_resumes = []

    for chunk in text_chunks:
        # Clean up the chunk by removing extra spaces and newlines
        cleaned_chunk = re.sub(r'\s+', ' ', chunk).strip()
        # Generate a score for the resume using the LLM
        result = chain.run(passage=cleaned_chunk)
        
        # Access the LLM-generated score based on your model's output format
        score = result['score']  
        
        # Append the score and resume chunk to the list
        ranked_resumes.append((score, cleaned_chunk))

    # Sort the resumes based on scores in descending order
    ranked_resumes.sort(reverse=True, key=lambda x: x[0])

    # ranked_resumes contains resumes sorted by LLM-generated scores.
    
    #  print the ranked resumes and their scores:
    for i, (score, resume) in enumerate(ranked_resumes, start=1):
        print(f"Rank {i}: Score = {score}")
        print(resume)
        print("=" * 40)


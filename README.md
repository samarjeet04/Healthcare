# Healthcare

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from PyPDF2 import PdfReader

pdf_reader = PdfReader('budget_speech.pdf')

#reading text from pdf
text = ''
for i, page in enumerate(pdf_reader.pages):
    content = page.extract_text()
    if content:
        text += content

#splitting the text using charactersplitter
text_splitter = CharacterTextSplitter(
    separator = "\n",
    chunk_size=800,
    chunk_overlap=200,
    length_function=len
)
splitted_texts = text_splitter.split_text(text)

embeddings = OpenAIEmbeddings()


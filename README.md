# Healthcare

#splitting the text using charactersplitter
text_splitter = CharacterTextSplitter(
    separator = "\n",
    chunk_size=8000,
    chunk_overlap=200,
    length_function=len
)
splitted_texts = text_splitter.split_text(text)

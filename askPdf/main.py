import os
import sys
import random
from langchain.text_splitter import CharacterTextSplitter
from langchain import PromptTemplate
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from PyPDF2 import PdfReader


pdf_files = []

def extract_text_from_pdf(pdf_file):
    try:
        pdf_file = open(pdf_file, 'rb')
        pdf_reader = PdfReader(pdf_file)

        # Initialize an empty string to store the text content
        text_content = ''

        # This is a cheap way to limit the text and avoiding problem with the max token length of OpenAPI
        for page in pdf_reader.pages[8:9]:
            text_content += page.extract_text()

        # Close the PDF file
        pdf_file.close()

        return text_content

    except FileNotFoundError:
        print(f"Error: File '{pdf_file}' not found.")
        return None
    
def create_vectordb(pdf_files, persist_directory):

    text_content = ''
    for pdf_file in pdf_files:
        text_content += extract_text_from_pdf(pdf_file)

    text_splitter = CharacterTextSplitter(chunk_size=300, chunk_overlap=70)
    texts = text_splitter.split_text(text_content)


    embedding = OpenAIEmbeddings(model="text-embedding-ada-002")
    vectordb = Chroma.from_texts(
        texts=texts, embedding=embedding, persist_directory=persist_directory
    )
    
    vectordb.persist()
    return vectordb

def query(vectordb, query):
    prompt_template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.
    {context}
    Question: {question}
    Answer in italiano aulico
    """

    PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])


    qa = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo"),
    chain_type="stuff",
    retriever=vectordb.as_retriever(search_kwargs={"k": 1}),
    chain_type_kwargs={"prompt": PROMPT},
    )

    print("\n--- Query ---\n")
    print(query)
    print("\n--- Answer ---\n")
    print(qa.run(query))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python pdf_text_extractor.py file1.pdf [file2.pdf ...]")
        sys.exit(1)
    
    pdf_files = sys.argv[1:]
    
    # OpenAI API KEY Check
    if not os.environ.get("OPENAI_API_KEY"):
        raise "OPENAI_API_KEY not set"

    #directory path where persist the vectordb
    persist_directory = "db"
    
    embedding = OpenAIEmbeddings()
    
    # You can comment this line to avoid recreating the vectordb
    vectordb = create_vectordb(pdf_files)

    vectordb = Chroma(persist_directory=persist_directory, embedding_function=embedding)

    query(vectordb, "explain me the fefund policies")
    
    print("\n--- Summary ---\n")
    
    print("\n--- End of Summary ---\n")

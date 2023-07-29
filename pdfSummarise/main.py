import os
import sys
from langchain.text_splitter import CharacterTextSplitter
from langchain import PromptTemplate
from langchain.docstore.document import Document
from langchain.llms.openai import OpenAI
from langchain.chains.summarize import load_summarize_chain
from PyPDF2 import PdfReader

pdf_files = []

def extract_text_from_pdf(pdf_file):
    try:
        pdf_file = open(pdf_file, 'rb')
        pdf_reader = PdfReader(pdf_file)

        # Initialize an empty string to store the text content
        text_content = ''

        # Loop through all the pages and extract text
        for page in pdf_reader.pages:
            text_content += page.extract_text()

        # Close the PDF file
        pdf_file.close()

        return text_content

    except FileNotFoundError:
        print(f"Error: File '{pdf_file}' not found.")
        return None
    
def summarise_docs(pdf_files):
    # OpenAI API KEY Check
    if not os.environ.get("OPENAI_API_KEY"):
        raise "OPENAI_API_KEY not set"

    # Main prompt
    prompt_template = """
    {text}
    CONCISE SUMMARY IN ENGLISH:"""
    
    PROMPT = PromptTemplate(template=prompt_template, input_variables=["text"])
    text_content = ''
    for pdf_file in pdf_files:
        text_content += extract_text_from_pdf(pdf_file)
    
    if not text_content:
        raise "no text found in the PDFs"
        return
    
    print(f"--- {pdf_file} ---\n")
    print(text_content)
    print("\n--- End of content ---\n")

    # Split the source text
    text_splitter = CharacterTextSplitter(chunk_size=300, separator=' ')
    texts = text_splitter.split_text(text_content)

    # Create Document objects for the texts (max 3 pages)
    docs = [Document(page_content=t) for t in texts[:3]]

    # Initialize the OpenAI module, load and run the summarize chain
    llm = OpenAI(temperature=0)
    chain = load_summarize_chain(llm, chain_type="stuff", prompt=PROMPT)
    
    return chain.run(docs)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python pdf_text_extractor.py file1.pdf [file2.pdf ...]")
        sys.exit(1)
    
    pdf_files = sys.argv[1:]
    
    summary = summarise_docs(pdf_files)
    
    print("\n--- Summary ---\n")
    print(summary)
    print("\n--- End of Summary ---\n")

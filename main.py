import pytesseract
from langchain.schema import Document
from pdf2image import convert_from_path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
import os

pdfs_directory = 'pdfs/'

embeddings = OllamaEmbeddings(model="deepseek-r1:1.5b")
model = OllamaLLM(model="deepseek-r1:1.5b")

template = """
You are an assistant that answers questions. Using the following retrieved information, answer the user question. If you don't know the answer, say that you don't know. Use up to three sentences, keeping the answer concise.
Question: {question} 
Context: {context} 
Answer:
"""
def upload_pdf(file):
    os.makedirs(pdfs_directory, exist_ok=True)  
    with open(os.path.join(pdfs_directory, file.name), "wb") as f:
        f.write(file.getbuffer())  

def extract_text_from_images(pdf_path):
    images = convert_from_path(
        pdf_path,
        #poppler helps to read image pdf
        poppler_path=r"C:\pdf_chat\Release-24.08.0-0\poppler-24.08.0\Library\bin"
    )
    text = ""
    for image in images:
        text += pytesseract.image_to_string(image) 
    return text 

def create_vector_store(file_path):
    loader = PyPDFLoader(file_path)
    documents = loader.load()

    combined_text = " ".join([doc.page_content.strip() for doc in documents])
    if not combined_text or len(combined_text) < 30: # this threadhold is keep beacuse to check id pdf text is ectracted by pydfloader. checking meaningful enough or not
        print("No meaningful text found, trying OCR...") # if it does not have txt i will check the image and extra it 
        text = extract_text_from_images(file_path)
        documents = [Document(page_content=text, metadata={})] #metadata store additoanl data 
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=300,
        add_start_index=True
    )
    chunked_docs = text_splitter.split_documents(documents)
    db = FAISS.from_documents(chunked_docs, embeddings)
    return db

def retrieve_docs(db, query, k=3):
    return db.similarity_search(query, k)

def question_pdf(question, documents):
    context = "\n\n".join([doc.page_content for doc in documents])
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model 
    return chain.invoke({"question": question, "context": context})

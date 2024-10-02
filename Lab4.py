import streamlit as st
import chromadb
import openai
import os
from PyPDF2 import PdfReader
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
import chromadb 
import pysqlite3
# import protobu 
# Load OpenAI key from environment
openai.api_key = os.getenv("OPENAI_API_KEY")

st.title("Course Information Chatbot - Lab 4")

# Function to read PDF files and return text
def read_pdfs(pdf_files):
    texts = []
    for pdf_file in pdf_files:
        reader = PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        texts.append(text)
    return texts

# Embedding text using OpenAI embeddings
def embed_texts(texts):
    embeddings = openai.Embedding.create(input=texts, model="text-embedding-ada-002")['data']
    return [embedding['embedding'] for embedding in embeddings]

# Creating and store ChromaDB collection
def create_chromadb_collection():
    if 'Lab4_vectorDB' not in st.session_state:
        client = chromadb.Client()
        collection = client.create_collection(name="Lab4Collection")
        
        # Read PDFs and generate embeddings
        pdf_files = ["document1.pdf", "document2.pdf", "document3.pdf"]  # replace with actual PDF file paths
        texts = read_pdfs(pdf_files)
        embeddings = embed_texts(texts)
        
        # Add documents to ChromaDB
        collection.add(
            documents=texts,
            metadatas=[{"filename": pdf_file} for pdf_file in pdf_files],
            embeddings=embeddings
        )
        
        st.session_state.Lab4_vectorDB = collection
        st.write("ChromaDB collection created!")
    else:
        st.write("ChromaDB already initialized.")

# Initializing ChromaDB collection
if st.button("Initialize ChromaDB"):
    create_chromadb_collection()

# Query ChromaDB
def query_chromadb(query_text):
    collection = st.session_state.Lab4_vectorDB
    results = collection.query(query_texts=[query_text], n_results=3)
    return results['metadatas']

# Search query
query = st.text_input("Enter search query (e.g., Generative AI, Data Science)")
if query:
    results = query_chromadb(query)
    st.write("Top 3 matched documents:")
    for result in results:
        st.write(result['filename'])

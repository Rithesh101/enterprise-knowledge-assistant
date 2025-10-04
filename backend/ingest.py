import os
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings 
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv

load_dotenv()

def create_vector_store():
    """Processes documents and creates a FAISS vector store."""
    print("Starting document ingestion...")
    loader = DirectoryLoader('documents/', glob="*.pdf", loader_cls=PyPDFLoader)
    documents = loader.load()
    
    # Add department metadata from filename
    for doc in documents:
        filename = doc.metadata.get('source', '')
        if 'hr' in filename.lower():
            doc.metadata['department'] = 'HR'
        elif 'engineering' in filename.lower():
            doc.metadata['department'] = 'Engineering'
        else:
            doc.metadata['department'] = 'General'

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    docs = text_splitter.split_documents(documents)

    # Use the free HuggingFace model
    model_name = "all-MiniLM-L6-v2"
    embeddings = HuggingFaceEmbeddings(model_name=model_name) 
    
    print(f"Creating FAISS index from {len(docs)} document chunks...")
    vectorstore = FAISS.from_documents(docs, embeddings)
    vectorstore.save_local("faiss_index")
    print("FAISS index created and saved successfully!")

if __name__ == "__main__":
    create_vector_store()
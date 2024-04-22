
import pandas as pd
from langchain.document_loaders import DataFrameLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from fastapi import HTTPException
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter


def split_documents_into_chunks(data, column_name="article", chunk_size=500, chunk_overlap=50, separators=['\n\n', '\n', '.']):
    """
    Split documents into chunks.
    
    Args:
    data (DataFrame): Input data containing articles.
    column_name (str): Name of the column containing the articles.
    chunk_size (int): Size of each chunk.
    chunk_overlap (int): Overlap between chunks.
    separators (list): List of separators for splitting documents.
    
    Returns:
    list: List of document chunks.
    """
    articles = DataFrameLoader(data, page_content_column=column_name)
    document = articles.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=separators,
        length_function=len
    )

    document_chunks = text_splitter.split_documents(document)
    
    return document_chunks


def create_vector_database(doc_chunks, embedding_model, persist_directory="/WQ/WikiQuery/vector_db"):
    """
    Create a vector database from document chunks.
    
    Args:
    doc_chunks (list): List of document chunks.
    embedding_model: Embedding model for vectorization.
    persist_directory (str): Directory to persist the vector database.
    
    Returns:
    Chroma: database successful creation message.
    """
   
    try:
        vec_database = Chroma.from_documents(
            doc_chunks,
            embedding_model,
            persist_directory=persist_directory
        )
        
        return {"message": "Vector database created successfully"}

    except Exception as e:
        error_message = f"Error occurred: {str(e)}"
        raise HTTPException(status_code=500, detail=error_message)
    

def preprocess_data(data_file_path):
    
    """
    Preprocess data.
    
    Args:
    data_file_path: Path to the data.
    """
   
    try:
        crypto_wiki_articles = pd.read_csv(data_file_path)
        crypto_wiki_articles = crypto_wiki_articles.dropna()
        
        return crypto_wiki_articles

    except Exception as e:
        error_message = f"Error occurred: {str(e)}"
        raise HTTPException(status_code=500, detail=error_message)


def build_prompt():
    template = """You are an AI Assistant specialized in cryptocurrencies named WikiQuery. 
    You provide detailed answers to customer inquiries within the scope of cryptocurrency. 
    If a question is outside this scope, you politely decline without revealing additional information whatsoever. 
    Your demeanor is professional and amicable, and you aim to guide and assist users while maintaining ethical standards. 
    Your responses are concise and informative, limited to one paragraph. 
    Context: {context} 
    Question: {question} 
    Helpful Answer:"""


    prompt = PromptTemplate(input_variables=["context", "question"], template=template)
    return prompt




   
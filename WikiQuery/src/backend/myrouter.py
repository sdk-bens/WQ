from fastapi import APIRouter, Query
from fastapi.responses import HTMLResponse, JSONResponse
from langchain.vectorstores import Chroma
from ydata_profiling import ProfileReport
import tempfile
from langchain.chains import RetrievalQA
from langchain_mistralai.chat_models import ChatMistralAI
import os
from backend.utils import split_documents_into_chunks, create_vector_database, build_prompt, preprocess_data
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from local_model import build_model

import os

mistral_api_key = os.getenv("MISTRAL_API_KEY")
embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

router = APIRouter()

data_file_path = '/WQ/WikiQuery/data/Wikipedia_Crypto_Articles.csv'

@router.get("/generate_response")
async def generate_response(question: str = Query(...)):
    db3 = Chroma(persist_directory="/WQ/WikiQuery/vector_db",embedding_function=embedding_function)
    retriever = db3.as_retriever()
    # for easy and fast response generation, get an API KEY from mistral.ai and use in the line below
    mistral = ChatMistralAI(mistral_api_key=mistral_api_key)

    # Second option is to use the loaded model
    # Uncomment the line below to use.
    #local_mistral = build_model()

    QnA = RetrievalQA.from_chain_type(llm=mistral, # Replace mistral with local_mistral if you use the local model instead of using the API
                                  chain_type="stuff",
                                  retriever=retriever,
                                  verbose=False,
                                  chain_type_kwargs={"prompt": build_prompt()})
    
    answer = QnA.run(question)

    return JSONResponse(content={"response": answer})


@router.get("/experimental_data_analysis")
async def generate_eda():

    crypto_wiki_articles = preprocess_data(data_file_path)
    
    # Generate the profiling report
    profile = ProfileReport(crypto_wiki_articles, title="WikiQuery Project Dataset - Northeastern 2024")

    # Save the report to a temporary file
    with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as temp_file:
        profile.to_file(temp_file.name)

    # Read the report file and return it as a response
    with open(temp_file.name, "rb") as f:
        report_content = f.read()

    # Delete the temporary file
    temp_file.close()

    return HTMLResponse(content=report_content)


@router.get("/create_vector_db")
async def create_db():

    # Split documents into chunks
    crypto_wiki_articles = preprocess_data(data_file_path)

    # Split documents into chunks
    document_chunks = split_documents_into_chunks(crypto_wiki_articles)

    # Create vector database
    return create_vector_database(document_chunks, embedding_function)

    # return JSONResponse(content={"message": "Vector database created successfully"})


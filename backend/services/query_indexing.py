from llama_index.core import GPTVectorStoreIndex, Document
from llama_index.embeddings.openai import OpenAIEmbedding
from services.s3_reader import S3Reader
import threading
import time
import os
from dotenv import load_dotenv
load_dotenv()

openai_api_key = os.environ.get("OPENAI_API_KEY")

embedding = OpenAIEmbedding(api_key=openai_api_key)

index = None
clear_timer = None
timer = 600

def clear_index():
    global index
    print("Clearing the index...")
    index = None

def index_document(filename, text):
    global index, clear_timer, timer
    doc = Document(text=text, metadata={"filename": filename}) 
    
    if index is None:
        index = GPTVectorStoreIndex.from_documents([doc], embedding=embedding)      # Use Vector Indexing to index the document
    else:
        index.insert(doc)        # Add the document to the index        
    
    if clear_timer is not None:
        clear_timer.cancel()

    clear_timer = threading.Timer(timer, clear_index)
    clear_timer.start()
    
    return index

def query_index(query):
    if index is None:
        raise ValueError("Index not initialized. Please upload a document first.")
    query_engine = index.as_query_engine()          # Query the Indexed data
    return query_engine.query(query)
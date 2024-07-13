from llama_index.core import GPTVectorStoreIndex, Document
from llama_index.embeddings.openai import OpenAIEmbedding
from services.s3_reader import S3Reader
import os
from dotenv import load_dotenv
load_dotenv()

openai_api_key = os.environ.get("OPENAI_API_KEY")

embedding = OpenAIEmbedding(api_key=openai_api_key)

index = None

def index_document(filename, text):
    global index
    if index is None:
        doc = Document(text=text, metadata={"filename": filename})          # Create a compatible document format for Indexing
        index = GPTVectorStoreIndex.from_documents([doc], embedding=embedding)      # Use Vector Indexing to index the document
    else:
        s3_reader = S3Reader('your-s3-bucket-name')
        documents = s3_reader.load_data()
        
        # Update the existing index with new documents
        for doc in documents:
            index.insert(doc)
            
    return index

def query_index(query):
    if index is None:
        raise ValueError("Index not initialized. Please upload a document first.")
    query_engine = index.as_query_engine()          # Query the Indexed data
    return query_engine.query(query)
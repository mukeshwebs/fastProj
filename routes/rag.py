from fastapi import FastAPI, HTTPException, Body,APIRouter
from pydantic import BaseModel
import logging

# Import your existing functions
from rag_file import retrieve_rag_response, db

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")



# Pydantic model for query
class QueryRequest(BaseModel):
    query: str

router = APIRouter(prefix="/rag-agent", tags=["rag-agent"])

@router.post("/ask")
def ask_question(request: QueryRequest):
    """
    Endpoint to interact with the RAG agent. 
    Provide a query to retrieve an AI-generated response based on the documents.
    """
    if not db:
        raise HTTPException(status_code=500, detail="Vector database is not initialized.")
    
    try:
        logging.info(f"Received Query: {request.query}")
        response = retrieve_rag_response(request.query)
        return {"query": request.query, "response": response}
    except Exception as e:
        logging.error(f"Error processing query: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while processing the query.")
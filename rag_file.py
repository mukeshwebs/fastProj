import logging
import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import PGVector
from langchain.tools import Tool
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Load environment variables
load_dotenv()

# Database connection details
COLLECTION_NAME = "state_of_union_vectors"
DATABASE_URL = os.getenv("DATABASE_URL")

# Initialize Hugging Face embeddings
embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-large-en")

# Initialize Groq LLM (Mixtral-8x7B)
llm = ChatGroq(
    model_name="llama-3.3-70b-versatile",
    temperature=0.7,
    api_key=os.getenv("GROQ_API_KEY")
)

def initialize_vector_store():
    """Initialize or update the vector store using PGVector."""
    try:
        db = PGVector(
            embedding_function=embeddings,
            collection_name=COLLECTION_NAME,
            connection_string=DATABASE_URL
        )

        if not db.similarity_search("test_query", k=1):
            logging.info("No existing vectors found. Inserting documents into PGVector...")
            loader = PyPDFLoader("fitness.pdf")
            docs = loader.load()
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
            all_splits = text_splitter.split_documents(docs)
            texts = [doc.page_content for doc in all_splits]

            PGVector.from_texts(
                texts=texts,
                embedding=embeddings,
                collection_name=COLLECTION_NAME,
                connection_string=DATABASE_URL
            )
            logging.info("Documents successfully stored in PGVector.")
        else:
            logging.info("Existing vector store detected. No duplicate entries added.")
        return db
    
    except Exception as e:
        logging.error(f"Error initializing PGVector: {e}")
        return None

db = initialize_vector_store()

def retrieve_rag_response(query):
    """Retrieve and process RAG documents based on user query."""
    logging.info(f"Processing query: {query}")
    if not db:
        return "I'm sorry, but the vector database is not initialized."
    try:
        similar_docs = db.similarity_search_with_score(query, k=3)
        filtered_docs = [doc for doc in similar_docs if doc[1] >= 0.15]

        if not filtered_docs:
            return "I couldn't find relevant information. Can you clarify your question?"

        doc_texts = "\n".join([f"- {doc[0].page_content}" for doc in filtered_docs])

        prompt = f"""
        You are an AI assistant that retrieves relevant information from a knowledge base.
        Given the following retrieved documents, generate a clear and informative response to the user's query.
        User Query: {query}
        Retrieved Information:
        {doc_texts}
        - Keep your response concise yet informative.
        - Use a friendly and engaging tone.
        - Provide additional insights if applicable.
        """
        response = llm([HumanMessage(content=prompt)])
        return response.content

    except Exception as e:
        logging.error(f"Error processing RAG query: {e}")
        return "I'm sorry, but something went wrong while retrieving the information."

# Define the RAG tool
rag_tool = Tool(
    name="RAG_Agent",
    func=retrieve_rag_response,
    description="Retrieves relevant documents using semantic search and generates a natural response."
)  
logging.info("RAG tool initialized successfully.")

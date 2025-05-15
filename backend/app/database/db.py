import os
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.models.user_model import User  # Beanie Document class for User
from app.models.document_model import DocumentModel  # Beanie Document class for Document
from app.models.qna_model import QADocument, QAItem
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

# Global variable to hold the database client
db_client: Optional[AsyncIOMotorClient] = None

# Initialize the MongoDB client
async def connect_to_mongo():
    global db_client
    mongo_uri = os.getenv("MONGO_URI")
    MONGO_DB = os.getenv("MONGO_DB")
    if not mongo_uri:
        raise ValueError("MongoDB URI is missing in environment variables.")
    db_client = AsyncIOMotorClient(mongo_uri)
    print(f"Connected to MongoDB")

    # Initialize Beanie with the database and models (User and Document)
    if not MONGO_DB:
        raise ValueError("MongoDB database name is missing in environment variables.")
    database = db_client.get_database(MONGO_DB) 
    # Bind the Beanie Document classes (User, DocumentModel) to the collection
    models = [User, DocumentModel, QADocument]  # List of Beanie Document classes
    await init_beanie(database, document_models=models)
    print(f"Beanie initialized with database: {database.name}")

# Disconnect the MongoDB client
async def disconnect_from_mongo():
    global db_client
    if db_client:
        db_client.close()

# Get the database client
async def get_db():
    global db_client
    MONGO_DB = os.getenv("MONGO_DB")
    if db_client is None:
        raise RuntimeError("MongoDB client is not initialized.")
    return db_client.get_database(MONGO_DB)  

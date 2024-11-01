from fastapi import FastAPI
from .config import API_HOST, API_PORT

def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application
    """
    app = FastAPI(
        title="Customer Support Chatbot",
        description="An AI-powered customer support chatbot",
        version="1.0.0",
        docs_url="/api/docs",
        redoc_url="/api/redoc",
    )

    # Add any additional configuration or middleware here
    
    return app

# Application instance
app = create_app()

# Import routes after app creation to avoid circular imports
from .main import *  # This registers all routes

__version__ = "1.0.0"
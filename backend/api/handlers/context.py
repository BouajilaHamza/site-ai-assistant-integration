from fastapi import APIRouter, UploadFile, Form
from backend.services.vector_store import initialize_knowledge_base
from typing import Optional
import aiofiles
import logging
import nest_asyncio


nest_asyncio.apply() 
context_router = APIRouter()
logger = logging.getLogger(__name__)

@context_router.post("/get-context")
async def get_context(base_url_or_path: Optional[str] = Form(None), sitemap_file: Optional[UploadFile] = None):
    """
    Get context by initializing the knowledge base.

    Args:
        base_url_or_path (str): The base URL of the website or the path to a local sitemap file.
        sitemap_file (UploadFile, optional): An uploaded sitemap file.

    Returns:
        dict: A response indicating success or failure.
    """
    try:
        # Handle uploaded sitemap file
        if sitemap_file:
            file_path = f"/tmp/{sitemap_file.filename}"
            async with aiofiles.open(file_path, 'wb') as out_file:
                content = await sitemap_file.read()
                await out_file.write(content)
            base_url_or_path = file_path  # Use the uploaded file path

        logger.debug(f"Initializing knowledge base with: {base_url_or_path}")
        docs = await initialize_knowledge_base(base_url_or_path)
        return {"message": "Context initialized successfully", "total_documents": len(docs)}
    except Exception as e:
        logger.error(f"Error initializing context: {e}")
        return {"error": str(e)}

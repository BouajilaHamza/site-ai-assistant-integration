from fastapi import APIRouter, UploadFile, Form, HTTPException
from backend.services.context_service import initialize_knowledge_base
from typing import Optional
from pydantic import HttpUrl
import logging
import tempfile

context_router = APIRouter()
logger = logging.getLogger(__name__)

@context_router.post("/get-context")
async def get_context(
                    base_url : Optional[HttpUrl] = Form(None), 
                    sitemap_file     : Optional[UploadFile] = None,
                    urls_limit       : int = 2
                    ):
    """
    Initialize the knowledge base from URL or uploaded sitemap.
    """
    try:
        if sitemap_file:
            with tempfile.NamedTemporaryFile(delete=False) as tmp:
                tmp.write(await sitemap_file.read())
                tmp_path = tmp.name
            base_url = tmp_path

        if not base_url:
            raise HTTPException(status_code=400, detail="No input provided.")

        logger.debug(f"Initializing knowledge base with: {base_url}")
        docs = await initialize_knowledge_base(base_url, urls_limit)
        # if not docs:
        #     raise HTTPException(status_code=400, detail="No documents loaded from sitemap!")
        return {"message": "Context initialized successfully", "total_documents": len(docs)}

    except Exception as e:
        logger.exception("Error initializing context")
        raise HTTPException(status_code=500, detail=str(e))

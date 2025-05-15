from fastapi import APIRouter, Depends, HTTPException
from beanie import PydanticObjectId

from typing import List
from app.schemas.document_schema import DocumentResponse, UnlockDocumentResponse, UnlockDocumentRequest
from app.handlers.document_handler import fetch_user_documents, fetch_document_by_id, delete_document_handler, unlock_document_handler
from app.models.user_model import User
from app.utils.get_current_user import get_current_user  # assuming you have this

router = APIRouter()

@router.get("/documents", response_model=List[DocumentResponse])
async def get_all_user_documents(
    skip: int = 0, limit: int = 5,
    current_user: User = Depends(get_current_user)
):
    try:
        return await fetch_user_documents(current_user, skip, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/documents/{id}", response_model=DocumentResponse)
async def get_single_document(id: PydanticObjectId, current_user: User = Depends(get_current_user)):
    try:
        return await fetch_document_by_id(id, current_user)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.delete("/documents/{id}")
async def delete_document(id: PydanticObjectId, current_user: User = Depends(get_current_user)):
    return await delete_document_handler(id, current_user)


@router.post("/documents/{id}/unlock", response_model=UnlockDocumentResponse)
async def unlock_document(id: PydanticObjectId, request: UnlockDocumentRequest):
    return await unlock_document_handler(id, request)
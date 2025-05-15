from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException, status, Request
from typing import Optional
from app.schemas.upload_schema import DocumentUploadRequest, DocumentLinkUploadRequest, DocumentResponse
from app.handlers.upload_handler import handle_file_upload, handle_link_upload
from app.utils.get_current_user import get_current_user
from app.models.user_model import User

router = APIRouter()


@router.post("/file", response_model=DocumentResponse)
async def upload_file(
    request: Request,
    file: UploadFile = File(...),
    alias: str = Form(...),
    summary: Optional[str] = Form(None),
    is_confidential: str = Form(...),
    password: Optional[str] = Form(None),
    current_user: User = Depends(get_current_user)
):
    """
    Upload a file (audio, video, or document).
    """
    upload_data = DocumentUploadRequest(
        alias=alias,
        summary=summary,
        is_confidential=is_confidential,
        password=password
    )

    return await handle_file_upload(file, upload_data, current_user)


@router.post("/link", response_model=DocumentResponse)
async def upload_file_via_link(
    request: Request,
    upload_data: DocumentLinkUploadRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Upload a file via link (audio, video, or document).
    """
    return await handle_link_upload(upload_data, current_user)

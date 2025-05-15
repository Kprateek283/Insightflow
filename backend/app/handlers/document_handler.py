from fastapi import HTTPException
from beanie import PydanticObjectId
from base64 import urlsafe_b64encode
from app.services.document_service import get_documents_by_user, get_document_by_id, delete_document_by_id
from app.schemas.document_schema import DocumentResponse, UnlockDocumentRequest, UnlockDocumentResponse
from app.models.user_model import User
from app.services.document_service import unlock_confidential_document

async def fetch_user_documents(current_user: User, skip:int, limit:int):
    documents = await get_documents_by_user(current_user.id,skip, limit)

    response_docs = []
    for doc in documents:
        response_docs.append(
            DocumentResponse(
                id=str(doc.id),
                alias=doc.alias,
                summary=doc.summary,
                transcription=None if doc.is_confidential == "yes" else doc.transcription,
                filelink=doc.filelink,
                filetype=doc.filetype,
                is_confidential=doc.is_confidential,
                created_at=doc.created_at,
            )
        )
    return response_docs


async def fetch_document_by_id(doc_id: PydanticObjectId, current_user: User) -> DocumentResponse:
    document = await get_document_by_id(doc_id)

    if not document:
        raise HTTPException(status_code=404, detail="Document not found.")

    if document.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view this document.")

    return DocumentResponse(
        id=str(document.id),
        alias=document.alias,
        summary=document.summary,
        transcription=document.transcription,
        filelink=document.filelink,
        filetype=document.filetype,
        is_confidential=document.is_confidential,
        created_at=document.created_at,
    )


async def delete_document_handler(doc_id: PydanticObjectId, current_user: User):
    try:
        deleted_document = await delete_document_by_id(doc_id, current_user)
        if not deleted_document:
            raise HTTPException(status_code=404, detail="Document not found.")
        return {"message": "Document deleted successfully."}
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))

async def unlock_document_handler(doc_id: PydanticObjectId, request: UnlockDocumentRequest):
    try:
        # Decrypt both summary and transcription
        result = await unlock_confidential_document(doc_id, request.password)

        if result is None:
            raise HTTPException(status_code=404, detail="Document not found.")

        return UnlockDocumentResponse(summary=result['summary'], transcription=result['transcription'])

    except ValueError as e:
        raise HTTPException(status_code=403, detail=str(e))

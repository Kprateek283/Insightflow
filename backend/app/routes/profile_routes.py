# app/api/routes/profile_routes.py
from fastapi import APIRouter, Depends
from app.models.user_model import User
from app.models.document_model import DocumentModel
from app.schemas.profile_schema import ProfileSummary
from app.utils.get_current_user import get_current_user

router = APIRouter()

@router.get("/profile", response_model=ProfileSummary)
async def get_profile_summary(current_user: User = Depends(get_current_user)):
    total_uploads = await DocumentModel.find(DocumentModel.user_id == current_user.id).count() or 0
    total_qna = current_user.total_qna or 0

    total_documents = await DocumentModel.find({
        "user_id": current_user.id,
        "filetype": "document"
    }).count() or 0

    total_audio = await DocumentModel.find({
        "user_id": current_user.id,
        "filetype": "audio"
    }).count() or 0

    total_video = await DocumentModel.find({
        "user_id": current_user.id,
        "filetype": "video"
    }).count() or 0

    return ProfileSummary(
        name=current_user.name,
        email=current_user.email,
        total_uploads=total_uploads,
        total_qna=total_qna,
        total_documents=total_documents,
        total_audio=total_audio,
        total_video=total_video
    )


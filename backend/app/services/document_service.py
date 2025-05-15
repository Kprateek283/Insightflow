from app.models.document_model import DocumentModel
from app.models.user_model import User
from beanie import PydanticObjectId
from app.utils.verify_password import verify_password
from app.utils.decrypt_content import decrypt_content

async def get_documents_by_user(user_id: PydanticObjectId, skip: int = 0, limit: int = 5):
    return await DocumentModel.find(DocumentModel.user_id == user_id).skip(skip).limit(limit).to_list()


async def get_document_by_id(doc_id: PydanticObjectId):
    return await DocumentModel.get(doc_id)


async def delete_document_by_id(doc_id: PydanticObjectId, current_user: User):
    document = await DocumentModel.get(doc_id)

    if not document:
        return None

    if document.user_id != current_user.id:
        raise PermissionError("You are not authorized to delete this document.")

    # Delete the document
    await document.delete()

    # Update the user: remove the document ID from user's list
    if doc_id in current_user.documents:
        current_user.documents.remove(doc_id)
        await current_user.save()

    return document


async def unlock_confidential_document(doc_id: PydanticObjectId, password: str):
    document = await DocumentModel.get(doc_id)
    if not document:
        return None

    result = {}

    # Decrypt the summary if it exists
    if document.summary:
        if document.is_confidential == "yes":
            if not document.hashed_password:
                raise ValueError("Password is not set for this confidential document.")
            if not verify_password(password, document.hashed_password):
                raise ValueError("Incorrect password.")
            result['summary'] = await decrypt_content(document.summary, password)
        else:
            result['summary'] = document.summary

    # Decrypt the transcription if it exists
    if document.transcription:
        if document.is_confidential == "yes":
            if not document.hashed_password:
                raise ValueError("Password is not set for this confidential document.")
            if not verify_password(password, document.hashed_password):
                raise ValueError("Incorrect password.")
            result['transcription'] = await decrypt_content(document.transcription, password)
        else:
            result['transcription'] = document.transcription

    return result

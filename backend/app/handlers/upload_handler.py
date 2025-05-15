import os
import tempfile
from fastapi import UploadFile, HTTPException
from datetime import datetime
from tempfile import NamedTemporaryFile
import aiohttp

from app.schemas.upload_schema import DocumentUploadRequest, DocumentLinkUploadRequest, DocumentResponse
from app.models.user_model import User
from app.models.document_model import DocumentModel
from app.utils.encrypt_content import encrypt_content
from app.utils.hash_password import hash_password
from app.utils.file_utils import get_file_type, get_file_size, get_url_file_type
from app.services.file_service import extract_text_from_document, extract_audio_from_video
from app.services.transcription_service import transcribe_with_assemblyai
from app.services.youtube_service import download_youtube_audio
from app.utils.email_utils import send_upload_email
from app.utils.chunk_utils import split_text_into_chunks
from app.vectorstore.faiss_index import add_document_embeddings
from app.services.summary_service import summarize_and_store

MAX_VIDEO_SIZE_MB = 50
MAX_AUDIO_SIZE_MB = 50
MAX_DOC_SIZE_MB = 30
MAX_LINK_FILE_SIZE_MB = 100


async def handle_file_upload(file: UploadFile, upload_data: DocumentUploadRequest, current_user: User) -> DocumentResponse:
    file_type = get_file_type(file.filename)
    file_size_mb = await get_file_size(file)
    print(upload_data.is_confidential)
    is_confidential = upload_data.is_confidential

    tmp_file_path = None
    tmp_audio_path = None

    with tempfile.NamedTemporaryFile(delete=False, suffix=file.filename) as temp:
        temp.write(await file.read())
        temp.flush()
        tmp_file_path = temp.name

    try:
        if file_type == "video":
            if file_size_mb > MAX_VIDEO_SIZE_MB:
                raise HTTPException(status_code=400, detail="Video file exceeds 50MB limit.")
            tmp_audio_path = await extract_audio_from_video(tmp_file_path)
            transcription = await transcribe_with_assemblyai(tmp_audio_path)

        elif file_type == "audio":
            if file_size_mb > MAX_AUDIO_SIZE_MB:
                raise HTTPException(status_code=400, detail="Audio file exceeds 50MB limit.")
            tmp_audio_path = tmp_file_path
            transcription = await transcribe_with_assemblyai(tmp_audio_path)

        elif file_type == "document":
            if file_size_mb > MAX_DOC_SIZE_MB:
                raise HTTPException(status_code=400, detail="Document file exceeds 30MB limit.")
            transcription = await extract_text_from_document(tmp_file_path)

        else:
            raise HTTPException(status_code=400, detail="Unsupported file type.")

        if is_confidential=="true":
            encrypted_text = await encrypt_content(transcription, upload_data.password)
            hashed_pwd = hash_password(upload_data.password)
            document = DocumentModel(
                user_id=current_user.id,
                alias=upload_data.alias,
                summary=upload_data.summary,
                transcription=encrypted_text,
                hashed_password=hashed_pwd,
                filetype=file_type,
                is_confidential="yes",
            )
        else:
            document = DocumentModel(
                user_id=current_user.id,
                alias=upload_data.alias,
                summary=upload_data.summary,
                transcription=transcription,
                filetype=file_type,
                is_confidential="no",
            )

        await document.insert()
        current_user.documents.append(document.id)
        await current_user.save()

        transcript_text = transcription
        document_id = document.id
        chunks = await split_text_into_chunks(transcript_text)
        print("Chunks done")
        await add_document_embeddings(str(document_id), chunks)
        
        await summarize_and_store(document_id)
        
        send_upload_email(current_user.email, upload_data.alias)

        return DocumentResponse(
            id=str(document.id),
            alias=document.alias,
            summary=document.summary,
            transcription=document.transcription,
            filelink=None,
            filetype=file_type,
            is_confidential=document.is_confidential,
            created_at=document.created_at or datetime.now(),
        )

    finally:
        if tmp_file_path and os.path.exists(tmp_file_path):
            os.remove(tmp_file_path)
        if tmp_audio_path and tmp_audio_path != tmp_file_path and os.path.exists(tmp_audio_path):
            os.remove(tmp_audio_path)


async def handle_link_upload(upload_data: DocumentLinkUploadRequest, current_user: User) -> DocumentResponse:
    file_url = str(upload_data.filelink)
    is_confidential = upload_data.is_confidential.lower() == "yes"

    tmp_path = None
    audio_path = None

    try:
        if "youtube.com" in file_url or "youtu.be" in file_url:
            file_type = "video"
            audio_path = await download_youtube_audio(file_url)

        else:
            async with aiohttp.ClientSession() as session:
                async with session.head(file_url) as resp:
                    if resp.status != 200 or "Content-Length" not in resp.headers:
                        raise ValueError("Could not determine file size from the URL")
                    file_size_mb = int(resp.headers["Content-Length"]) / (1024 * 1024)
                    if file_size_mb > MAX_LINK_FILE_SIZE_MB:
                        raise ValueError("File size exceeds 100MB limit")

            file_type = get_url_file_type(file_url)
            if file_type not in ["audio", "video"]:
                raise ValueError("Only audio and video links are allowed")

            async with aiohttp.ClientSession() as session:
                async with session.get(file_url) as resp:
                    if resp.status != 200:
                        raise ValueError("Failed to download the file")
                    with NamedTemporaryFile(delete=False, suffix=".tmp") as tmp_file:
                        tmp_file.write(await resp.read())
                        tmp_path = tmp_file.name

            audio_path = await extract_audio_from_video(tmp_path) if file_type == "video" else tmp_path

        transcription = await transcribe_with_assemblyai(audio_path)

        if is_confidential:
            encrypted_text = await encrypt_content(transcription, upload_data.password)
            hashed_pw = hash_password(upload_data.password)
            document = DocumentModel(
                user_id=current_user.id,
                alias=upload_data.alias,
                summary=upload_data.summary,
                original_filename=os.path.basename(file_url),
                filelink=file_url,
                transcription=encrypted_text,
                hashed_password=hashed_pw,
                filetype=file_type,
                is_confidential="yes",
            )
        else:
            document = DocumentModel(
                user_id=current_user.id,
                alias=upload_data.alias,
                summary=upload_data.summary,
                original_filename=os.path.basename(file_url),
                filelink=file_url,
                transcription=transcription,
                filetype=file_type,
                is_confidential="no",
            )

        await document.insert()
        current_user.documents.append(document.id)
        await current_user.save()

        transcript_text = transcription
        document_id = document.id
        chunks = await split_text_into_chunks(transcript_text)
        await add_document_embeddings(str(document_id), chunks)
        
        await summarize_and_store(document.id)
        
        send_upload_email(current_user.email, upload_data.alias)

        return DocumentResponse(
            id=str(document.id),
            alias=document.alias,
            summary=document.summary,
            transcription=None if is_confidential else document.transcription,
            filelink=document.filelink,
            filetype=file_type,
            is_confidential=document.is_confidential,
            created_at=document.created_at or datetime.utcnow(),
        )

    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)
        if audio_path and os.path.exists(audio_path) and audio_path != tmp_path:
            os.remove(audio_path)

from app.services.llm_service import generate_answer
from app.services.fallback_service import fallback_answer
from app.models.qna_model import QADocument, QAItem
from datetime import datetime, timezone
from fastapi import HTTPException
from app.schemas.auth_schema import UserResponse

async def process_qa(document_id: str, question: str, current_user: UserResponse) -> QADocument:
    try:
        # Let generate_answer handle both retrieval & generation
        answer = await generate_answer(question, document_id)
        used_fallback = False

        # If you want sources, you'll need to get them from inside generate_answer and return separately
        sources = None  # Optionally extend generate_answer to return sources
    except Exception as e:
        print(f"LLM error: {e}")
        answer = await fallback_answer(question)
        used_fallback = True
        sources = None

    # Fetch or create the document for storing Q&A
    qaDocument = await QADocument.find_one(QADocument.document_id == str(document_id))
    if not qaDocument:
        qaDocument = QADocument(
            document_id=str(document_id),
            qas=[],
            total_qas=0
        )

    # Append the new QA pair
    qa_item = QAItem(
        question=question,
        answer=answer,
        timestamp=datetime.now(timezone.utc),
        used_fallback=used_fallback,
        sources=sources,
    )
    qaDocument.qas.append(qa_item)
    qaDocument.total_qas += 1
    await qaDocument.save()

    return qaDocument

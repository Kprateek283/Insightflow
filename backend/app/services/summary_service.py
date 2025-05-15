# app/services/summary_service.py

from transformers import BartForConditionalGeneration, BartTokenizer
from app.models.document_model import DocumentModel
from beanie import PydanticObjectId
import torch
import textwrap
from app.utils.encrypt_content import encrypt_content

# Load the model and tokenizer once
tokenizer = BartTokenizer.from_pretrained("facebook/bart-large-cnn")
model = BartForConditionalGeneration.from_pretrained("facebook/bart-large-cnn")

# Automatically use GPU if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)


async def summarize_text(transcription: str) -> str:
    """
    Summarizes a long transcription using BART.
    If text exceeds token limit, it summarizes in chunks.
    """
    # BART has a token limit of ~1024; safe limit with tokenizer padding
    max_chunk_length = 950

    # Wrap into manageable chunks (by char count, not token)
    chunks = textwrap.wrap(transcription, 1800)

    summarized_chunks = []
    for chunk in chunks:
        inputs = tokenizer.encode(chunk, return_tensors="pt", truncation=True, max_length=max_chunk_length).to(device)
        summary_ids = model.generate(inputs, max_length=150, min_length=30, length_penalty=2.0, num_beams=4, early_stopping=True)
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        summarized_chunks.append(summary)

    return " ".join(summarized_chunks)


async def summarize_and_store(document_id: PydanticObjectId):
    """
    Fetches the transcription from the document, summarizes it,
    and updates the `summary` field in the database.
    """
    doc = await DocumentModel.get(document_id)
    if not doc:
        raise ValueError("Document not found")

    if not doc.transcription:
        raise ValueError("No transcription found for this document")

    summary = await summarize_text(doc.transcription)

    # Update the summary field
    doc.summary = summary
    await doc.save()
    return summary

import mimetypes
import os
from fastapi import UploadFile

import mimetypes
from typing import Union
from pydantic import AnyUrl

import mimetypes
from typing import Union
from pydantic import AnyUrl

def get_file_type(file_name: Union[str, AnyUrl]) -> str:
    """
    Returns the type of the file based on its extension or MIME type.
    Possible return values: 'audio', 'video', 'document'
    """
    file_str = str(file_name)
    mimetype, _ = mimetypes.guess_type(file_str)

    print(f"[DEBUG] file_name: {file_str}")
    print(f"[DEBUG] guessed mimetype: {mimetype}")

    if mimetype:
        if mimetype.startswith("audio"):
            return "audio"
        elif mimetype.startswith("video"):
            return "video"
        elif mimetype in [
            "application/pdf",
            "application/msword",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "text/plain",
            "application/vnd.ms-powerpoint",
            "application/vnd.openxmlformats-officedocument.presentationml.presentation",
            "application/vnd.ms-excel",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        ]:
            return "document"

    raise ValueError("Unsupported file type")


import requests
import magic
import yt_dlp

def get_url_file_type(url: str) -> str:
    """
    Detects the type of file from a given URL. Supports YouTube links.
    Args:
        url (str): URL of the file or YouTube video
    Returns:
        str: 'audio', 'video', or 'document'
    """
    try:
        # Make sure it's a string
        url = str(url)

        # Check for YouTube links and extract direct URL
        if "youtube.com" in url or "youtu.be" in url:
            ydl_opts = {
                'quiet': True,
                'format': 'bestaudio/best',
                'skip_download': True,
                'noplaylist': True
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                direct_url = info.get("url")
                if not direct_url:
                    raise ValueError("Could not extract direct media URL from YouTube link.")
                url = direct_url  # Use actual file URL

        # Download and check MIME type
        response = requests.get(url, stream=True, timeout=10)
        if response.status_code != 200:
            raise ValueError(f"Failed to fetch file: Status code {response.status_code}")

        sample = response.raw.read(2048)

        mime = magic.Magic(mime=True)
        mime_type = mime.from_buffer(sample)

        document_mime_types = [
            "application/pdf",
            "application/msword",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "application/vnd.oasis.opendocument.text",
            "text/plain",
        ]

        if mime_type.startswith("audio"):
            return "audio"
        elif mime_type.startswith("video"):
            return "video"
        elif mime_type in document_mime_types:
            return "document"
        else:
            raise ValueError(f"Unsupported file type: {mime_type}")

    except Exception as e:
        raise ValueError(f"Error detecting file type: {e}")


async def get_file_size(file: UploadFile) -> float:
    contents = await file.read()
    size_bytes = len(contents)
    await file.seek(0)  # Reset file pointer for future reads
    size_mb = size_bytes / (1024 * 1024)
    return size_mb

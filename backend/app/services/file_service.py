import textract
from moviepy import VideoFileClip
import tempfile


async def extract_text_from_document(file_path: str) -> str:
    """
    Extracts text from a document file using textract.

    Supported formats: PDF, DOCX, TXT, etc.

    Args:
        file_path (str): Path to the document file.

    Returns:
        str: Extracted text content.
    """
    try:
        text = textract.process(file_path)
        return text.decode('utf-8')
    except Exception as e:
        raise RuntimeError(f"Failed to extract text: {str(e)}")


async def extract_audio_from_video(video_file_path: str) -> str:
    """
    Extracts audio from a video file.

    Args:
        video_file_path (str): Path to the video file.

    Returns:
        str: Path to the temporary audio file extracted from the video.
    """
    try:
        # Load the video file
        video = VideoFileClip(video_file_path)
        
        # Extract audio from video
        audio = video.audio
        
        # Create a temporary file to store the audio
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio_file:
            audio.write_audiofile(temp_audio_file.name)
            return temp_audio_file.name
    except Exception as e:
        raise RuntimeError(f"Failed to extract audio from video: {str(e)}")

import requests
import time
import os

BASE_URL = "https://api.assemblyai.com"
API_KEY = os.getenv("ASSEMBLYAI_API_KEY")  # Make sure to set your API key as an environment variable
HEADERS = {"authorization": API_KEY}

async def upload_to_assemblyai(filepath: str) -> str:
    """
    Upload a local audio file to AssemblyAI and return the upload URL.
    """
    with open(filepath, "rb") as f:
        response = requests.post(f"{BASE_URL}/v2/upload", headers=HEADERS, data=f)

    if response.status_code != 200:
        print(f"Upload error: {response.status_code}, {response.text}")
        response.raise_for_status()

    return response.json()["upload_url"]

async def transcribe_with_assemblyai(audio_source: str) -> str:
    """
    Transcribe audio file via AssemblyAI API and return the transcript.

    Args:
        audio_source (str): Path to local file or public URL of the audio.

    Returns:
        str: Transcription text from AssemblyAI.
    """
    # Step 0: If local file, upload it to get a URL
    if os.path.exists(audio_source):
        print("Uploading local file to AssemblyAI...")
        audio_url = await upload_to_assemblyai(audio_source)
    else:
        audio_url = audio_source

    data = {
        "audio_url": audio_url,
        "speaker_labels": True
    }

    # Step 1: Send a transcription request
    response = requests.post(f"{BASE_URL}/v2/transcript", headers=HEADERS, json=data)

    if response.status_code != 200:
        print(f"Error: {response.status_code}, Response: {response.text}")
        response.raise_for_status()

    # Get the transcript ID
    transcript_json = response.json()
    transcript_id = transcript_json["id"]

    # Step 2: Poll for the transcription result
    polling_endpoint = f"{BASE_URL}/v2/transcript/{transcript_id}"

    while True:
        transcript = requests.get(polling_endpoint, headers=HEADERS).json()

        if transcript["status"] == "completed":
            full_transcript = transcript["text"]
            print(f"\nFull Transcript: \n\n{full_transcript}")

            if 'utterances' in transcript:
                print("\nSpeaker Segmentation:\n")
                for utterance in transcript["utterances"]:
                    print(f"Speaker {utterance['speaker']}: {utterance['text']}\n")

            return full_transcript

        elif transcript["status"] == "error":
            raise RuntimeError(f"Transcription failed: {transcript['error']}")

        else:
            time.sleep(3)
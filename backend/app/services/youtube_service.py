import yt_dlp

async def download_youtube_audio(link: str) -> str:
    output_path = "/tmp/%(id)s.%(ext)s"

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'ffmpeg_location': '/usr/bin/ffmpeg',
        'postprocessor_args': [
            '-loglevel', 'error'  # Optional: reduces noise
        ],
        'quiet': False,
        'no_warnings': True,
    }
    if(has_audio_stream(link)):
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=True)
            audio_path = ydl.prepare_filename(info_dict).rsplit(".", 1)[0] + ".mp3"
            return audio_path

def has_audio_stream(link: str) -> bool:
    with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
        info = ydl.extract_info(link, download=False)
        return any(f.get('acodec') != 'none' for f in info.get('formats', []))

import os
import sys
import uuid
import shutil
import zipfile
import yt_dlp
import time

def cleanup_temp_folder(temp_base):
    if not os.path.exists(temp_base):
        return
    now = time.time()
    for f in os.listdir(temp_base):
        f_path = os.path.join(temp_base, f)
        if os.path.isdir(f_path):
            # If older than 1 hour, remove it
            if os.stat(f_path).st_mtime < now - 3600:
                try:
                    shutil.rmtree(f_path)
                except Exception:
                    pass

def get_temp_folder():
    """Returns a unique temporary folder inside the app directory."""
    temp_base = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'temp_downloads')
    cleanup_temp_folder(temp_base)
    
    temp_dir = os.path.join(temp_base, str(uuid.uuid4()))
    os.makedirs(temp_dir, exist_ok=True)
    return temp_dir

def download_audio(url):
    temp_folder = get_temp_folder()
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(temp_folder, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'noplaylist': False,
        'quiet': False,
        'extractor_args': {
            'youtube': ['client=ANDROID', 'client=IOS']
        },
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    downloaded_files = os.listdir(temp_folder)
    
    if len(downloaded_files) == 0:
        raise Exception("No files were downloaded.")
    elif len(downloaded_files) == 1:
        return os.path.join(temp_folder, downloaded_files[0])
    else:
        zip_filename = os.path.join(temp_folder, "playlist.zip")
        with zipfile.ZipFile(zip_filename, 'w') as zipf:
            for file in downloaded_files:
                file_path = os.path.join(temp_folder, file)
                zipf.write(file_path, arcname=file)
                os.remove(file_path) # clean up the individual file
        return zip_filename

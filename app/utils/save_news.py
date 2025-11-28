import shutil
from pathlib import Path
from fastapi import UploadFile

def save_upload_file(upload_file: UploadFile, destination: Path) -> str:
    try:
        destination.mkdir(parents=True, exist_ok=True)

        destination = destination / upload_file.filename


        with destination.open('wb') as buffer:
            shutil.copyfileobj(upload_file.file, buffer)

    finally:
        upload_file.file.close()

    return str(destination).replace("\\", "/")
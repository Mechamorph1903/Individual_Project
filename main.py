import os
import uuid
from hashlib import blake2b
from pathlib import Path

from fastapi import FastAPI, HTTPException, UploadFile

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Image API is running"}


@app.post("/turkey/images")
async def upload_image(file: UploadFile):
    img_hash = blake2b()

    img_filename = file.filename
    img_content_type = file.content_type

    # file validation
    if img_content_type != "image/jpeg":
        raise HTTPException(
            status_code=415,
            detail=f"File Type {img_content_type} not supported. Only JPEG Images are supported",
        )

    content = await file.read()
    img_size_bytes = len(content)
    img_hash.update(content)
    img_digest = img_hash.hexdigest()

    # blob
    blob_dir = Path("blobs")
    new_blob = False
    digest_file = img_digest + ".jpg"

    blob_path = blob_dir / digest_file

    if not blob_path.exists():
        new_blob = True
        blob_dir.mkdir(exist_ok=True)
        try:
            # temp file
            temp_filename = f"{uuid.uuid4()!s}.tmp"
            temp_path = blob_dir / temp_filename

            temp_path.write_bytes(content)
            os.replace(temp_path, blob_path)
        except OSError:
            raise HTTPException(status_code=500, detail="Failed to store image")
        finally:
            temp_path.unlink(missing_ok=True)

    return {
        "filename": img_filename,
        "content_type": img_content_type,
        "size_bytes": img_size_bytes,
        "digest": img_digest,
        "new_blob": new_blob,
        "blob_path": blob_path,
    }

# Request Files
# source: https://fastapi.tiangolo.com/tutorial/request-files/

# We can define files to be uploaded by the client using `File`




from fastapi import FastAPI, File, UploadFile
import logfire
from typing import Annotated
from pydantic import BaseModel

app = FastAPI()
logfire.configure()
logfire.instrument_fastapi(app)

@app.post('/files/')
async def create_file(file: Annotated[bytes, File()]): # multipart form data
    return {"file_size": len(file)}

@app.post('/upload/file/')
async def create_upload_file(file: UploadFile): # multipart form data
    return {"filename": file.filename}

# Define `File` Parameters
# Create file parameters the same way we would for `Body` or `Form`.

# `File` is inherits directly from `Form`.
# The files will be uploaded as "form data"
# If we delcare the tyoe of our path operation function aprameter as `bytes`, FastAPI will read the file for us and we will receive the contents as `bytes`.
# The whole contents of the file will be stored in memory. and it will work well for small files.

# File Parameters with `UploadFile`
# using `UploadFile` has several advantages over `bytes`:
'''
- we don't have to sue `File()` in the default vlue of the parameter.
- it uses a "spooled" file:
    - A file stored in memory up to a maximum size limit, and after passing this limit it will be stored in disk.
- this means that it will workf well for large files like images, videos, large binaries etc. without consuming all the memory.
- we can get metadata from the uploaded file
- it has a `file-like` `async` interface.
- It exposes an acutual python `SpooledTemporaryFile` object that we can pass directly to other libraries that expect a file-like object.
more? https://fastapi.tiangolo.com/tutorial/request-files/#uploadfile
'''

# `UploadFile` has the following `async` methods.
# write(data): write data(str or bytes) to the file
# read(data): read size(int) bytes/character of the file
# seek(offset): goes to the byte position offset(int) in the file.
    # e.g., `await myfile.seek(0) would go to the start of the file.
    # this is especially useful if we run `awaut myfile.read()` once and then need to read the contents again.
# close(): close the file.

# # all these methods are `async` methods, we need to "await" them.

# for instance, we can get the contents with:
@app.post('/file/read/')
async def return_file_contents(file: UploadFile):
    return {
        "filename": file.filename,
        "contents": await file.read()
    }
# note: when we use the `async` methods, FastAPI runs the files methods in a threadpool and awaits for them.

# What is `Form Data`
# HTML forms (<form></form>) sends the data to the server normally uses a "special" encoding for the data, it's different from JSON.
'''
Data from `forms` is normally encoded using the "media type" `application/x-www-form-urlencoded` when it doesn't include files.

read more about encodings and form fields, head for the : https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/POST
'''

# We can declare multiple `File` and `Form` parameters in a path operation, but we can't also declare `Body` fields that we expect to receive as JSON, as the request will have the body encoded using `multipart`/form-data instead of `application/json`
# this is a limitation of HTTP protocol

# Optional File Upload
@app.post('/optional/file/')
async def optiona_file(file: Annotated[bytes | None, File()] = None):
    if not file:
        return {"message": "No file sent"}
    else:
        return {"file_size": len(file)}

@app.post('/optional/uploadfile/')
async def optional_upload_file(file: UploadFile | None = None):
    if not file:
        return {"message": "No upload file sent"}
    else:
        return {"filename": file.filename}
    

# `UploadFile` with Additional Metadata
# We can use `File()` with `UploadFile`, for example, to set additional metadata:

@app.post('/file/additional-metadata/')
async def additional_metadata(file: Annotated[bytes, File(description="A file read as bytes")]):
    return {"file_size": len(file)}

@app.post('/upload/file/additional-metadata')
async def upload_file_additional_metadata(
    file: Annotated[UploadFile, File(description="A file read as UploadFile")]
):
    return {"filename": file.filename}

# Multiple File Uploads
# It's possible to upload several files at the same time. they would be associated to the same "form field" sent using "form data"
# To use that, declare a list of `bytes` or `UploadFile`:
from fastapi.responses import HTMLResponse

@app.post('/multiple-file-uploads/files/')
async def multiple_file_uploads(files: Annotated[list[bytes], File()]):
    return {
        "file_size": [len(file) for file in files]
    }

@app.post('/multiple-files-uploads/files/uploadfile/')
async def multiple_file_uploads_uploadfile(files: list[UploadFile]):
    return {
        "filename": [file.filename for file in files]
    }

#note:: UploadFile is faster than bytes>File
@app.get('/multiple-file-upload/')
async def main():
    content = """
                <body>
                    <form action="/multiple-file-uploads/files/" enctype="multipart/form-data" method="post">
                        <input name="files" type="file" multiple>
                        <input type="submit">
                    </form>
                    <form action="/multiple-files-uploads/files/uploadfile/" enctype="multipart/form-data" method="post">
                        <input name="files" type="file" multiple>
                        <input type="submit">
                    </form>
                </body>
            """
    return HTMLResponse(content=content)
# check in browser: http://localhost:8000/multiple-file-upload/





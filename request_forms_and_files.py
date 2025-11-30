# Request Forms and Files
# source: https://fastapi.tiangolo.com/tutorial/request-forms-and-files/
# 
#  # We can define files and form fields at the same time using `File` and `Form`.
# Import `File` and `Form`
from typing import Annotated
from fastapi import FastAPI, File, Form, UploadFile
import logfire

app = FastAPI()
logfire.configure()
logfire.instrument_fastapi(app)

@app.post('/request-forms-files/')
async def init_files(
    file: Annotated[bytes, File()],
    fileb: Annotated[UploadFile, File()],
    token: Annotated[str, Form()],
):
    return {
        "file_size": len(file),
        "token": token,
        "fileb_content_type": fileb.content_type,
    }

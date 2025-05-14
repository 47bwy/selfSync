# -*- encoding: utf-8 -*-
'''
@Time    :   2025/04/29 09:44:45
@Author  :   47bwy
@Desc    :   None
'''

from typing import Annotated, Union

from fastapi import APIRouter, File, Form, UploadFile
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

func = APIRouter()


class FormData(BaseModel):
    username: str
    password: str
    model_config = {"extra": "forbid"}


@func.post("/login/")
async def login(username: str = Form(), password: str = Form()):
    return {"username": username}

@func.post("/login2/")
async def login2(data: Annotated[FormData, Form()]):
    return data


@func.post("/files/")
async def create_file(file: bytes = File(description="A file read as bytes")):
    return {"file_size": len(file)}

@func.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(description="A file read as UploadFile")):
    return {"filename": file.filename}


@func.post("/files/")
async def create_file(
    file: bytes = File(), fileb: UploadFile = File(), token: str = Form()
):
    return {
        "file_size": len(file),
        "token": token,
        "fileb_content_type": fileb.content_type,
    }

@func.get("/myfiles")
async def main():
    content = """
<body>
<form action="/files/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
<form action="/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)




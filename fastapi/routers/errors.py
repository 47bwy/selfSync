# -*- encoding: utf-8 -*-
'''
@Time    :   2025/04/29 11:21:52
@Author  :   47bwy
@Desc    :   None
'''

from fastapi import APIRouter, HTTPException, status


class UnicornException(HTTPException):
    def __init__(self, name: str):
        self.name = name
        super().__init__(status_code=418, detail=f"Unicorns are not real: {name}")


error = APIRouter()

@error.get("/error_items/{item_id}")
async def read_item(item_id: int):
    if item_id == 3:
        raise HTTPException(status_code=418, detail="Nope! I don't like 3.")
    return {"item_id": item_id}


@error.get("/unicorns/{name}")
async def read_unicorn(name: str):
    if name == "yolo":
        raise UnicornException(name=name)
    return {"unicorn_name": name}



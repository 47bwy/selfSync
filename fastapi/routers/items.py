# -*- encoding: utf-8 -*-
'''
@Time    :   2025/04/27 15:21:24
@Author  :   47bwy
@Desc    :   None
'''


from datetime import datetime, timedelta, timezone
from typing import Annotated, Union

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

from fastapi.depends import (CommonQueryParams, authenticate_user,
                             common_parameters, create_access_token,
                             fake_hash_password, get_current_active_user,
                             get_current_user, oauth2_scheme,
                             query_or_cookie_extractor, verify_key,
                             verify_token)
from fastapi.fakedb import fake_users_db
from fastapi.schemas import (FilterParams, Item, ItemExtra, ModelName, Token,
                             User, UserIn, UserInDB, UserOut,
                             fake_password_hasher, fake_save_user)

ACCESS_TOKEN_EXPIRE_MINUTES = 30
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


class Item(BaseModel):
    title: str
    size: int


item = APIRouter()


@item.get("/")
def read_root():
    return {"Hello": "World"}


@item.get("/item/")
# def read_item(item_id: int, q: Union[list[str], None] = Query(default=None, min_length=1, max_length=50)):
async def read_item(q: Union[str, None] = Query(default=None, min_length=1, max_length=50, title="Query string", description="Query string")):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


@item.get("/items/{item_id}")
async def read_items(item_id: Annotated[int, Path(title="The ID of the item to get")],
                     q: Annotated[str | None, Query(alias="item-query")] = None):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results


@item.get("/items/")
async def read_items(filter_query: Annotated[FilterParams, Query()]):
    return filter_query


@item.get("/greet/{name}")
def greet(name: str):
    return {"greeting": f"Hello {name}!"}


@item.get("/db_items/")
def read_items(skip: int = 0, limit: int = 10):
    return fake_items_db[skip: skip + limit]


@item.get("/model/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep learning is great!"}
    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeNet is a classic!"}
    return {"model_name": model_name, "message": "Model not found!"}


@item.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id, "price": item.price}


@item.put("/items_extra/{item_id}")
async def update_item(item_id: int, item_extra: ItemExtra):
    results = {"item_id": item_id, "item": item_extra}
    return results


@item.post("/users/")
def create_user(user: User):
    if user.user_id < 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User ID must be a positive integer")
    return {"Hello": user.username}


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The Bar fighters", "price": 62, "tax": 20.2},
    "baz": {
        "name": "Baz",
        "description": "There goes my baz",
        "price": 50.2,
        "tax": 10.5,
    },
}


@item.get(
    "/items/{item_id}/name",
    response_model=Item,
    response_model_include={"name", "description"},
)
async def read_item_name(item_id: str):
    return items[item_id]


@item.get("/items/{item_id}/public", response_model=Item, response_model_exclude={"tax"})
async def read_item_public_data(item_id: str):
    return items[item_id]


@item.post("/user/", response_model=UserOut)
async def create_user(user_in: UserIn):
    user_saved = fake_save_user(user_in)
    return user_saved


@item.post("/invalid_item/")
async def create_invalid_item(item: Item):
    return item


@item.get("/my_depends")
async def read_my_depends(commons: dict = Depends(common_parameters)):
    return commons


@item.get("/my_class_depends")
# async def read_my_class_depends(commons: CommonQueryParams = Depends(CommonQueryParams)):
async def read_my_class_depends(commons: CommonQueryParams = Depends()):
    response = {}
    if commons.q:
        response.update({"q": commons.q})
    items = fake_items_db[commons.skip: commons.skip + commons.limit]
    response.update({"items": items})
    return commons


@item.get("/my_nested_depends")
async def read_my_nested_depends(query_or_default: str = Depends(query_or_cookie_extractor)):
    return {"q_or_cookie": query_or_default}


@item.get("/my_decorator_depends", dependencies=[Depends(verify_token), Depends(verify_key)])
async def read_my_decorator_depends():
    return {"message": "Hello World!"}


@item.get("/my_auth_depends")
async def read_my_auth_depends(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}


@item.post("/token")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return Token(access_token=access_token, token_type="bearer")


@item.get("/users/me/", response_model=User)
async def read_users_me(current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user


@item.get("/users/me/items/")
async def read_own_items(current_user: Annotated[User, Depends(get_current_active_user)]):
    return [{"item_id": "Foo", "owner": current_user.username}]

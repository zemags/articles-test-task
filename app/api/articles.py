from typing import List

from app.api import crud
from app.api.models import ArticleDB, ArticleSchema
from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.post("/", response_model=ArticleDB, status_code=201)
async def create_article(payload: ArticleSchema):
    result = await crud.crete_article(payload)
    response_object = {
        "id": result["id"],
        "username": payload.username,
        "text": payload.text,
        "version": result["version"],
    }
    return response_object


@router.get("/{id}/", response_model=ArticleDB)
async def read_article(id: int):
    article = await crud.get(id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article


@router.get("/", response_model=List[ArticleDB])
async def read_all_articles():
    return await crud.get_all()


@router.put("/{id}/")
async def update_article(payload: ArticleDB):
    article = await crud.get(payload.id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    updated_row = await crud.update(payload)

    response_object = {
        "id": updated_row["id"],
        "username": updated_row["username"],
        "text": updated_row["text"],
        "version": updated_row["version"]
    }

    if updated_row:
        response_object[
            "detail"] = f"Successfully updated article, new version: " \
                        f"{response_object['version']}"
    else:
        response_object[
            "detail"] = f"Someone updated article before you, new version: " \
                        f"{response_object['version']}"
    return response_object

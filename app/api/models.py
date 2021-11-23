from typing import Optional

from pydantic import BaseModel


class ArticleSchema(BaseModel):
    username: str
    text: str


class ArticleDB(ArticleSchema):
    id: int
    version: Optional[int] = None

from app.api.models import ArticleSchema, ArticleDB
from app.db import articles, database


async def crete_article(payload: ArticleSchema):
    version = 0
    query = articles.insert().values(username=payload.username,
                                     text=payload.text,
                                     version=version)
    last_id = await database.execute(query=query)
    return {"id": last_id, "version": version}


async def get(id: int):
    query = articles.select().where(id == articles.c.id)
    return await database.fetch_one(query=query)


async def get_all():
    query = articles.select()
    return await database.fetch_all(query=query)


async def update(payload: ArticleDB, **kwargs):
    article = await get(payload.id)
    older_version = payload.version or article["version"]
    data = {"username": payload.username, "text": payload.text,
            "version": article["version"] + 1, "id": payload.id,
            "older_version": older_version}
    statement = """
                update articles
                set username = :username,
                    text = :text,
                    version = :version
                where id = :id and version = :older_version
                returning id, username, text, version"""
    return await database.fetch_one(statement, data)

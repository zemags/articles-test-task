from app.api import articles
from app.app_events import startup, shutdown
from app.db import metadata, engine
from fastapi import FastAPI

metadata.create_all(engine)


def get_app() -> FastAPI:
    app = FastAPI(
        title="Articles API",
        description="Create and update articles"
    )
    app.add_event_handler("startup", startup(app))
    app.add_event_handler("shutdown", shutdown(app))

    metadata.create_all(engine)

    app.include_router(articles.router, prefix="/articles", tags=["articles"])

    return app


app = get_app()

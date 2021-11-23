from typing import Callable

from app.db import database
from fastapi import FastAPI


def startup(app: FastAPI) -> Callable:
    async def start_app() -> None:
        await database.connect()

    return start_app


def shutdown(app: FastAPI) -> Callable:
    async def stop_app() -> None:
        await database.disconnect()

    return stop_app

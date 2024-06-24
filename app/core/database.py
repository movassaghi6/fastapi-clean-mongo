from typing import Callable
from contextlib import contextmanager
from fastapi import FastAPI
from loguru import logger
from pymongo import MongoClient

from app.core.config import (
    MONGODB_URL, MONGODB_MAX_CONNECTIONS_COUNT, MONGODB_MIN_CONNECTIONS_COUNT,
)


class MongoDB:
    client: MongoClient = None

mongo_db = MongoDB()

def mongodb_startup(app: FastAPI) -> None:
    logger.info('connect to the MongoDB...')
    mongo_client = MongoClient(
        MONGODB_URL,
        MaxPoolSize = MONGODB_MAX_CONNECTIONS_COUNT,
        MinPoolSize = MONGODB_MIN_CONNECTIONS_COUNT,
    )
    mongo_db.client = mongo_client
    app.state.mongo_client = mongo_client
    logger.info('MongoDB connection succeeded! ')

def mongodb_shutdown(app: FastAPI) -> None:
    logger.info('Closing the MongoDB connection...')
    app.state.mongo_client.close()
    logger.info('MondoDB connection closed! ')


def create_start_app_handler(app: FastAPI) -> Callable:
    def start_app() -> None:
        mongodb_startup(app)
    return start_app

def create_stop_app_handler(app: FastAPI) -> Callable:
    @logger.catch
    def stop_app() -> None:
        mongodb_shutdown(app)
    return stop_app

@contextmanager
def get_mongodb():
    try:
        with MongoClient() as client:
            db = client["clean-database"]
            yield db
    except Exception as e:
        print(f'Error: {e}')
        raise
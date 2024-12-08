import asyncio

import databases
import sqlalchemy
from sqlalchemy.exc import OperationalError, DatabaseError
from sqlalchemy.ext.asyncio import create_async_engine
from asyncpg.exceptions import (    # type: ignore
    CannotConnectNowError,
    ConnectionDoesNotExistError,
)

from quizapi.config import config

metadata = sqlalchemy.MetaData()

quiz_table = sqlalchemy.Table(
    "quizzes",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("title", sqlalchemy.String),
    # sqlalchemy.Column(
    #     "question",
    #     sqlalchemy.ForeignKey("question.id"),
    #     nullable=False,
    # ),
    sqlalchemy.Column("player_id", sqlalchemy.Integer),
    sqlalchemy.Column("description", sqlalchemy.String),
)

question_table = sqlalchemy.Table(
    "questions",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("text", sqlalchemy.String),
    sqlalchemy.Column("option_one", sqlalchemy.String),
    sqlalchemy.Column("option_two", sqlalchemy.String),
    sqlalchemy.Column("option_three", sqlalchemy.String),
    sqlalchemy.Column("option_four", sqlalchemy.String),
    sqlalchemy.Column("correct_answer", sqlalchemy.String),
    sqlalchemy.Column(
        "quiz_id",
        sqlalchemy.ForeignKey("quizzes.id"),
        nullable=False,
    ),
)

player_table = sqlalchemy.Table(
    "players",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("username", sqlalchemy.String),
)

db_uri = (
    f"postgresql+asyncpg://{config.DB_USER}:{config.DB_PASSWORD}"
    f"@{config.DB_HOST}/{config.DB_NAME}"
)

engine = create_async_engine(
    db_uri,
    echo=True,
    future=True,
    pool_pre_ping=True,
)

database = databases.Database(
    db_uri,
    force_rollback=True,
)


async def init_db(retries: int = 5, delay: int = 5) -> None:
    """Function initializing the DB.

    Args:
        retries (int, optional): Number of retries of connect to DB.
            Defaults to 5.
        delay (int, optional): Delay of connect do DB. Defaults to 2.
    """
    for attempt in range(retries):
        try:
            async with engine.begin() as conn:
                await conn.run_sync(metadata.create_all)
            return
        except (
            OperationalError,
            DatabaseError,
            CannotConnectNowError,
            ConnectionDoesNotExistError,
        ) as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            await asyncio.sleep(delay)

    raise ConnectionError("Could not connect to DB after several retries.")
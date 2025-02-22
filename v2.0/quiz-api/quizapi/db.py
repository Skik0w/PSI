"""A module providing database access."""

import asyncio
import databases
import sqlalchemy
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.exc import OperationalError, DatabaseError
from sqlalchemy.ext.asyncio import create_async_engine
from asyncpg.exceptions import (    # type: ignore
    CannotConnectNowError,
    ConnectionDoesNotExistError,
)
from quizapi.config import config

metadata = sqlalchemy.MetaData()

player_table = sqlalchemy.Table(
    "players",
    metadata,
    sqlalchemy.Column(
        "id",
        UUID(as_uuid=True),
        primary_key=True,
        server_default=sqlalchemy.text("gen_random_uuid()")
    ),
    sqlalchemy.Column("username", sqlalchemy.String, unique=True),
    sqlalchemy.Column("email", sqlalchemy.String, unique=True),
    sqlalchemy.Column("password", sqlalchemy.String),
    sqlalchemy.Column("balance", sqlalchemy.Integer, default=0),
)

quiz_table = sqlalchemy.Table(
    "quizzes",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("title", sqlalchemy.String),
    sqlalchemy.Column(
        "player_id",
        sqlalchemy.ForeignKey("players.id"),
        nullable=False,
    ),
    sqlalchemy.Column("description", sqlalchemy.String),
    sqlalchemy.Column("shared", sqlalchemy.Boolean),
    sqlalchemy.Column("reward", sqlalchemy.String, nullable=False, unique=True),
)

question_table = sqlalchemy.Table(
    "questions",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("question_text", sqlalchemy.String),
    sqlalchemy.Column("option_one", sqlalchemy.String),
    sqlalchemy.Column("option_two", sqlalchemy.String),
    sqlalchemy.Column("option_three", sqlalchemy.String),
    sqlalchemy.Column("option_four", sqlalchemy.String),
    sqlalchemy.Column("correct_option", sqlalchemy.String),
    sqlalchemy.Column(
        "quiz_id",
        sqlalchemy.ForeignKey("quizzes.id"),
        nullable=False,
    )
)

history_table = sqlalchemy.Table(
    "history",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column(
        "player_id",
        sqlalchemy.ForeignKey("players.id"),
        nullable=False,
    ),
    sqlalchemy.Column(
        "quiz_id",
        sqlalchemy.ForeignKey("quizzes.id"),
    ),
    sqlalchemy.Column("total_questions", sqlalchemy.Integer),
    sqlalchemy.Column("correct_answers", sqlalchemy.Integer),
    sqlalchemy.Column("effectiveness", sqlalchemy.Float),
    sqlalchemy.Column("timestamp", sqlalchemy.DateTime(timezone=True)),
)

tournament_table = sqlalchemy.Table(
    "tournaments",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("description", sqlalchemy.String),
    sqlalchemy.Column("quizzes_id", sqlalchemy.ARRAY(sqlalchemy.Integer), nullable=False),
    sqlalchemy.Column("participants", sqlalchemy.ARRAY(UUID(as_uuid=True)), nullable=False),
)

reward_table = sqlalchemy.Table(
    "rewards",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column(
        "quiz_id",
        sqlalchemy.ForeignKey("quizzes.id"),
        nullable=False,
    ),
    sqlalchemy.Column(
        "player_id",
        sqlalchemy.ForeignKey("players.id"),
        nullable=False,
    ),
    sqlalchemy.Column(
        "reward",
        sqlalchemy.ForeignKey("quizzes.reward"),
        nullable=False,
    ),
    sqlalchemy.Column("value", sqlalchemy.Integer, nullable=False),
)

shop_table = sqlalchemy.Table(
    "shops",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("value", sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column(
        "quiz_id",
        sqlalchemy.ForeignKey("quizzes.id"),
        nullable=False,
    )
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
            print(f"Attempt {attempt + 1} fai led: {e}")
            await asyncio.sleep(delay)

    raise ConnectionError("Could not connect to DB after several retries.")
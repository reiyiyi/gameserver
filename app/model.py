import json
import uuid
from enum import Enum, IntEnum
from typing import Optional

from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.exc import NoResultFound

from api import LiveDifficulty

from .db import engine


class InvalidToken(Exception):
    """指定されたtokenが不正だったときに投げる"""


class SafeUser(BaseModel):
    """token を含まないUser"""

    id: int
    name: str
    leader_card_id: int

    class Config:
        orm_mode = True


def create_user(name: str, leader_card_id: int) -> str:
    """Create new user and returns their token"""
    token = str(uuid.uuid4())
    # NOTE: tokenが衝突したらリトライする必要がある.
    with engine.begin() as conn:  # トランザクション開始！
        result = conn.execute(  # 第1引数でSQL,第2引数で値提供
            text(
                "INSERT INTO `user` (name, token, leader_card_id) VALUES (:name, :token, :leader_card_id)"
            ),
            {"name": name, "token": token, "leader_card_id": leader_card_id},
        )
        # print(result)
    return token


def _get_user_by_token(conn, token: str) -> Optional[SafeUser]:
    # TODO: 実装
    conn = engine.connect()
    result = conn.execute(
        text("select * from user where token=:token"),
        dict(token=token),
    )
    try:
        row = result.one()
    except NoResultFound:
        return None
    return SafeUser.from_orm(row)


def get_user_by_token(token: str) -> Optional[SafeUser]:
    with engine.begin() as conn:
        return _get_user_by_token(conn, token)


def update_user(token: str, name: str, leader_card_id: int) -> None:
    # このコードを実装してもらう
    with engine.begin() as conn:
        result = conn.execute(  # 第1引数でSQL,第2引数で値提供
            text(
                "UPDATE `user` SET name=:name, leader_card_id=:leader_card_id WHERE token=:token"
            ),
            {"name": name, "token": token, "leader_card_id": leader_card_id},
        )

def create_room(live_id: int, select_difficulty: LiveDifficulty) -> int:
    with engine.begin() as conn:  # トランザクション開始！
        result = conn.execute(
            text(
                "INSERT INTO `room` (live_id, joined_user_count) VALUES (:live_id, :joined_user_count)"
            ),
            {"live_id": live_id, "joined_user_count": 1},
        )

        room_id = "xxx"
        user_id = 

        result2 = conn.execute(
            text(
                "INSERT INTO `room_member` (room_id, user_id, name, leader_card_id, select_difficulty, is_host) \
                    VALUES (:room_id, :user_id, name, :leader_card_id, :select_difficulty, :is_host)"
            ),
            {
                "room_id": room_id,
                "user_id": user_id,
                "name": name,
                "leader_card_id": leader_card_id,
                "select_difficulty": select_difficulty,
                "is_host": True
                },
        )

    return room_id
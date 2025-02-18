from typing import Annotated

from database import Cache, Querying
from fastapi import Cookie, Depends, HTTPException
from redis import Redis


async def get_db():
    db = Querying()
    return db

def does_token_exist(r: Annotated[Redis, Depends(Cache.get_connection)], token: str) -> bool:
    return r.get(f"auth:{token}")

async def is_in_session(r: Annotated[Redis, Depends(Cache.get_connection)], session_id: Annotated[str | None, Cookie()] = None) -> bool:
    s = r.get(f"session:{session_id}")
    if not s:
        raise HTTPException(status_code=400, detail="Bad request, session is missing")
    return True
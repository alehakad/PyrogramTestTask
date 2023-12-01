from sqlalchemy import select

from .connection import AsyncSession
from .models import User


async def check_user(user_id: int, username: str):
    async with AsyncSession() as session:
        existing_user = await session.execute(
            select(User).where(User.username == "example")
        ).scalar()
        if not existing_user:
            new_user = User(user_id=user_id, username=username)
            session.add(new_user)
            await session.commit()

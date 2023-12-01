from sqlalchemy import select, func
from loguru import logger
from .connection import AsyncSession
from .models import User


async def check_user(user_id: int, username: str):
    async with AsyncSession() as session:
        user = await session.execute(select(User).where(User.user_id == user_id))
        user_exists = user.scalar()
        user_exists_bool = False
        if user_exists:
            user_exists_bool = True
        logger.info(f"User {user_id} {user_exists_bool}")
        if not user_exists_bool:
            logger.info("New user created")
            new_user = User(user_id=user_id, username=username)
            session.add(new_user)
            await session.commit()
        return user_exists_bool


async def count_users():
    async with AsyncSession() as session:
        user_count = await session.scalar(
            select(func.count()).where(User.time_created >= func.current_date())
        )
        logger.info(f"{user_count=}")
        return user_count

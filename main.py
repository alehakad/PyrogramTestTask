#!/usr/bin/env python3
import asyncio
from datetime import datetime, timedelta

from loguru import logger
from pyrogram import Client, filters
from dotenv import load_dotenv
import os

from pyrogram.types import Message
from utils import lexicon
from db.create_tables import create_tables
from db.queries import check_user, count_users


load_dotenv()


api_id = os.environ.get("tg_api_id")
api_hash = os.environ.get("tg_api_hash")


async def send_message(client: Client, message: Message, user_id: int):
    recent_messages = await client.get_messages(chat_id=user_id, limit=5)
    if not any("Хорошего дня" in msg.text for msg in recent_messages):
        await message.reply_text("Скоро вернусь с новым материалом!")


async def main():
    app = Client("my_account", api_id=api_id, api_hash=api_hash)
    await app.start()
    admin_info = await app.get_me()
    ADMIN_ID = admin_info.id

    logger.info("Creating tables")
    create_tables()

    # command users_today
    @app.on_message(
        filters=filters.user(ADMIN_ID) & filters.command("users_today", prefixes="/")
    )
    async def user_count(client: Client, message: Message):
        user_id = message.from_user.id
        users_today = await count_users()
        await client.send_message(chat_id=user_id, text=f"{users_today=}")
        logger.info(f"Registered users today: {users_today}")

    @app.on_message(filters=filters.private)
    async def welcome(client: Client, message: Message):
        time_received = datetime.now()
        # check db
        user_id, username = message.from_user.id, message.from_user.username
        logger.info(f"Message from {user_id} received")
        user_exists_bool = await check_user(user_id=user_id, username=username)

        if not user_exists_bool:
            # 10 minutes message
            await client.send_message(
                chat_id=user_id,
                text=lexicon.message_10_min,
                schedule_date=time_received + timedelta(seconds=10),
            )
            logger.info(f"10 minutes message scheduled")
            # 90 minutes message
            await client.send_message(
                chat_id=user_id,
                text=lexicon.message_90_min,
                schedule_date=time_received + timedelta(seconds=90),
            )
            logger.info(f"90 minutes message scheduled")
            # 90 minutes photo
            await client.send_photo(
                chat_id=user_id,
                photo="media/img.jpg",
                schedule_date=time_received + timedelta(seconds=91),
            )
            logger.info(f"90 minutes photo scheduled")

    while True:
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())

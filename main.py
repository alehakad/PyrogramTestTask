#!/usr/bin/env python3
import asyncio
from datetime import datetime, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler
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


async def main():
    app = Client("my_account", api_id=api_id, api_hash=api_hash)
    await app.start()
    admin_info = await app.get_me()
    ADMIN_ID = admin_info.id

    logger.info("Creating tables")
    create_tables()

    # scheduler functions
    async def send_message_with_check(user_id, message_text):
        to_send = True
        async for message in app.get_chat_history(user_id):
            if (
                message.from_user.id == ADMIN_ID
                and message.text == lexicon.check_message
            ):
                to_send = False
        if to_send:
            await app.send_message(chat_id=user_id, text=message_text)
            logger.info(f"Message {message_text} sent to {user_id}")
        else:
            logger.info(f"Message {message_text} is not sent to {user_id}")

    async def send_message_no_check(user_id, message_text):
        await app.send_message(chat_id=user_id, text=message_text)
        logger.info(f"Message {message_text} sent to {user_id}")

    async def send_message_photo_no_check(user_id, message_text, photo_path):
        await app.send_message(chat_id=user_id, text=message_text)
        await app.send_photo(
            chat_id=user_id,
            photo=photo_path,
        )
        logger.info(f"Message {message_text} and photo {photo_path} sent to {user_id}")

    scheduler = AsyncIOScheduler()
    scheduler.start()

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
            # 1 вариант - schedule_date argument - проблема с проверкой при отправке последнего сообщения
            # # 10 minutes message
            # await client.send_message(
            #     chat_id=user_id,
            #     text=lexicon.message_10_min,
            #     schedule_date=time_received + timedelta(seconds=10),
            # )
            # logger.info(f"10 minutes message scheduled")
            # # 90 minutes message
            # await client.send_message(
            #     chat_id=user_id,
            #     text=lexicon.message_90_min,
            #     schedule_date=time_received + timedelta(seconds=90),
            # )
            # logger.info(f"90 minutes message scheduled")
            # # 90 minutes photo
            # await client.send_photo(
            #     chat_id=user_id,
            #     photo="media/img.jpg",
            #     schedule_date=time_received + timedelta(seconds=91),
            # )
            # logger.info(f"90 minutes photo scheduled")

            # 2 вариант - apscheduler
            scheduler.add_job(
                send_message_no_check,
                "date",
                run_date=time_received + timedelta(seconds=10),
                args=[user_id, lexicon.message_10_min],
            )
            scheduler.add_job(
                send_message_photo_no_check,
                "date",
                run_date=time_received + timedelta(seconds=90),
                args=[user_id, lexicon.message_90_min, "media/img.jpg"],
            )
            scheduler.add_job(
                send_message_with_check,
                "date",
                run_date=time_received + timedelta(seconds=120),
                args=[user_id, lexicon.message_2_hours],
            )

    while True:
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())

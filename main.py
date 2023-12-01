#!/usr/bin/env python3
import asyncio
from datetime import datetime, timedelta

from loguru import logger
from pyrogram import Client
from dotenv import load_dotenv
import os

from pyrogram.types import Message

from db.create_tables import create_tables
from db.queries import check_user


load_dotenv()
create_tables()

api_id = os.environ.get("tg_api_id")
api_hash = os.environ.get("tg_api_hash")


async def send_message(client: Client, message: Message, user_id: int):
    recent_messages = await client.get_messages(chat_id=user_id, limit=5)
    if not any("Хорошего дня" in msg.text for msg in recent_messages):
        await message.reply_text("Скоро вернусь с новым материалом!")


async def main():
    app = Client("my_account", api_id=api_id, api_hash=api_hash)
    await app.start()

    @app.on_message()
    async def welcome(client: Client, message: Message):
        # check db
        user_id, username = message.from_user.id, message.from_user.username
        check_user(user_id=user_id, username=username)

        await client.send_message(chat_id=user_id, message="Hi", schedule_date=datetime.now()+timedelta(minutes=1))

    while True:
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())

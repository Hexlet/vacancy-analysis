import asyncio
import os
from telethon.sync import TelegramClient
from dotenv import load_dotenv

load_dotenv()


class TelegramChannelClient:
    def __init__(self, client):
        self.client = client

    @classmethod
    async def create(cls):
        client = TelegramClient(
            os.getenv('TELEGRAM_SESSION'),
            int(os.getenv('TELEGRAM_API_ID')),
            os.getenv('TELEGRAM_API_HASH')
        )
        await client.start()
        return cls(client)


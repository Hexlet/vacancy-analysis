import asyncio

from asgiref.sync import sync_to_async
from django.core.management.base import BaseCommand
from dotenv import load_dotenv

from app.services.telegram.telegram_channels.models import Channel
from app.services.telegram.telegram_parser.views import TelegramParserView

load_dotenv()


class Command(BaseCommand):
    help = 'Запускает Telegram слушатель'

    def handle(self, *args, **kwargs):
        asyncio.run(self.start_listener())

    async def start_listener(self):
        parser = TelegramParserView()
        await parser.initialize()  # Инициализация клиента
        print("слушатель телеграм работает!")

        listened_channels = set()

        while True:

            channels = await sync_to_async(
                lambda: list(
                    Channel.objects.filter(status='active').values_list(
                        'username', flat=True)))()

            new_channels = [c for c in channels if c not in listened_channels]

            for channel in new_channels:
                print(f"▶️ Подключение к новому каналу: {channel}")
                asyncio.create_task(parser.channel_listener(channel))
                listened_channels.add(channel)

            await asyncio.sleep(300)

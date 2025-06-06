import os
import asyncio
from django.core.management.base import BaseCommand
from dotenv import load_dotenv
from app.services.telegram.telegram_parser.views import TelegramParser


load_dotenv()


class Command(BaseCommand):
    help = 'Запускает Telegram слушатель'

    def handle(self, *args, **kwargs):
        parser = TelegramParser()
        print("слушатель телеграм работает!")
        asyncio.run(parser.run_listener('@cwa_my_test'))
        print("слушатель телеграм не работает")
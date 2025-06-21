from telethon import events
from dotenv import load_dotenv
from .parser.keyword_extractor import KeywordExtractor
from .parser.vacancy_parser import VacancyParser
from .parser.save_vacancy import SaveDataVacancy
from app.services.telegram.telegram_client import TelegramChannelClient

load_dotenv()


class TelegramParserView:
    def __init__(self):
        self.client = None
        self.keywords = KeywordExtractor()
        self.vacancy = VacancyParser()
        self.save = SaveDataVacancy()

    async def initialize(self):
        client_wrapper = await TelegramChannelClient.create()
        self.client = client_wrapper.client
        self.vacancy = VacancyParser()
        self.keywords = KeywordExtractor()
        await self.keywords.load_keywords()

    async def channel_listener(self, channel_username):
        @self.client.on(events.NewMessage(chats=channel_username))
        async def new_post_handler(event):
            try:
                message = event.message.message
                parsed = await self.vacancy.parse_vacancy_from_text(message)
                if parsed:
                    await self.save.save_vacancy(parsed, event.message.date)
                    print("Сохранено в БД")
            except Exception as e:
                print(f"Ошибка при обработке сообщения: {e}")

        try:
            await self.client.start()
            print(f"Слушатель запущен для канала: {channel_username}")
            await self.client.run_until_disconnected()
        except Exception as e:
            print(f"Ошибка в работе клиента: {e}")
        finally:
            print("Слушатель остановлен")

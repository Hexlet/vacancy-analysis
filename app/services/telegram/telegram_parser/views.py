import os
import re
from telethon.sync import TelegramClient
from telethon import events
from .models import Vacancy, KeyWord
from dotenv import load_dotenv
from asgiref.sync import sync_to_async

load_dotenv()


class KeywordExtractor:
    def __init__(self):
        self.keywords = {
            'company': [],
            'salary': [],
            'city': [],
            'busyness': [],
            'post': []
        }
        self.load_keywords()

    def load_keywords(self):
        for kw in KeyWord.objects.all():
            for field in self.keywords:
                value = getattr(kw, field)
                if value:
                    self.keywords[field] += [v.strip().lower() for v in value.split(',')]

    def matches(self, line, field):
        return any(kw in line.lower() for kw in self.keywords[field])


class LineParser:
    @staticmethod
    def extract_value(line):
        parts = re.split(r'[:\-\u2014]', line, maxsplit=1)
        return parts[1].strip() if len(parts) > 1 else line.strip()

    @staticmethod
    def extract_salary(line, keywords):
        cleaned_line = line
        for kw in keywords:
            cleaned_line = re.sub(kw, '', cleaned_line, flags=re.IGNORECASE)
        match = re.search(r'(от\s*)?\d[\d\s.,]{3,}', cleaned_line.lower())
        return match.group().strip() if match else None

    @staticmethod
    def extract_phone(line):
        match_username = re.search(r'@\w+', line)
        if match_username:
            return match_username.group()
        match_phone = re.search(r'(\+7|8)?[\s\-]?\(?\d{3}\)?[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}', line)
        return match_phone.group() if match_phone else None

    @staticmethod
    def extract_link(line):
        match = re.search(r'https?://[^\s]+|t\.me/[^\s]+', line)
        return match.group() if match else None


class TelegramParser:
    def __init__(self, api_id=os.getenv('TELEGRAM_API_ID'), api_hash=os.getenv('TELEGRAM_API_HASH'), session_name=os.getenv('TELEGRAM_SESSION')):
        self.api_id = api_id
        self.api_hash = api_hash
        self.session_name = session_name
        self.client = TelegramClient(self.session_name, self.api_id, self.api_hash, system_version="4.10.5 beta x64")
        self.keywords = KeywordExtractor()

    @sync_to_async
    def parse_vacancy_from_text(self, text):
        lines = text.strip().splitlines()
        parser = LineParser()

        data = dict.fromkeys(['post', 'company', 'city', 'salary', 'link', 'busyness', 'phone'])
        data['post'] = next((line.strip() for line in lines if line.strip()), None)

        actions = [
            ('company', lambda line: parser.extract_value(line) if self.keywords.matches(line, 'company') else None),
            ('salary',
             lambda line: parser.extract_salary(line, self.keywords.keywords['salary']) if self.keywords.matches(line,
                                                                                                                 'salary') else None),
            ('city', lambda line: parser.extract_value(line) if self.keywords.matches(line, 'city') else None),
            ('busyness', lambda line: parser.extract_value(line) if self.keywords.matches(line, 'busyness') else None),
            ('phone', parser.extract_phone),
            ('link', parser.extract_link)
        ]

        for line in lines:
            line = line.strip()
            for key, func in actions:
                if not data[key]:
                    value = func(line)
                    if value:
                        data[key] = value

        return data

    @sync_to_async
    def save_vacancy(self, parsed, date):
        Vacancy.objects.create(
            post=parsed['post'],
            company=parsed['company'],
            city=parsed['city'],
            salary=parsed['salary'],
            date=date,
            link=parsed['link'],
            phone=parsed['phone'],
            busyness=parsed['busyness'],
        )
        print("Запись в модель")

    async def run_listener(self, channel_username):
        @self.client.on(events.NewMessage(chats=channel_username))
        async def new_post_handler(event):
            message = event.message.message
            parsed = await self.parse_vacancy_from_text(message)
            if parsed:
                await self.save_vacancy(parsed, event.message.date)
                print("Сохранено в БД")

        await self.client.start()
        await self.client.run_until_disconnected()

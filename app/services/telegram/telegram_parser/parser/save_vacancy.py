from ..models import Vacancy
from asgiref.sync import sync_to_async


class SaveDataVacancy:
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

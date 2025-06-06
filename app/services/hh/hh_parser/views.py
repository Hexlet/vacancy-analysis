import requests
from bs4 import BeautifulSoup
import time
from django.http import JsonResponse
from .models import Vacancy


def vacancy_list(request):
    Vacancy.objects.all().delete()
    query = 'Python'
    area = 1
    per_page = 4

    url = 'https://api.hh.ru/vacancies'
    headers = {"User-Agent": "HH-User-Agent"}
    params = {
        'text': query,
        'area': area,
        'per_page': per_page,
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        vacancy_ids = [item['id'] for item in response.json()['items']]

        saved_count = 0
        errors = []

        for vacancy_id in vacancy_ids:
            try:
                time.sleep(0.3)

                detail_url = f'https://api.hh.ru/vacancies/{vacancy_id}'
                detail_response = requests.get(detail_url, headers=headers)
                detail_response.raise_for_status()
                item = detail_response.json()

                address = item.get('address', {})
                city = address.get('city', '') \
                    if isinstance(address, dict) else ''
                street = address.get('street', '') \
                    if isinstance(address, dict) else ''
                building = address.get('building', '') \
                    if isinstance(address, dict) else ''

                salary_data = item.get('salary', {})
                salary = None
                if salary_data:
                    salary_parts = []
                    if salary_data.get('from'):
                        salary_parts.append(f"от {salary_data['from']}")
                    if salary_data.get('to'):
                        salary_parts.append(f"до {salary_data['to']}")
                    if salary_data.get('currency'):
                        salary_parts.append(salary_data['currency'])
                    salary = ' '.join(salary_parts)

                description = BeautifulSoup(
                    item.get('description', ''),
                    'html.parser'
                ).get_text()

                work_format = ', '.join(
                    [work['name'] for work in item.get('work_format', [])]
                )
                skills = ', '.join(
                    [skill['name'] for skill in item.get('key_skills', [])]
                )

                area_name = item.get('area')
                experience = item.get('experience')
                schedule = item.get('schedule')
                Vacancy.objects.update_or_create(
                    hh_id=item.get('id'),
                    defaults={
                        'title': item.get('name', ''),
                        'company_name': item.get(
                            'employer', {}).get('name', ''),
                        'company_id': item.get('employer', {}).get('id', ''),
                        'area': area_name.get('name', '') if area_name else '',
                        'salary': salary,
                        'published_at': item.get('published_at', ''),
                        'url': item.get('alternate_url', ''),
                        'experience': experience.get(
                            'name', '') if experience else '',
                        'schedule': schedule.get(
                            'name', '') if schedule else '',
                        'work_schedule_by_days': item.get(
                            "work_schedule_by_days", [{}])[0].get("name", ""),
                        'working_hours': item.get(
                            "working_hours", [{}])[0].get("name", ""),
                        'work_format': work_format,
                        'key_skills': skills,
                        'description': description,
                        'city': city,
                        'street': street,
                        'building': building,
                        'employment': item.get(
                            'employment', {}).get('name', ''),
                        'contacts': item.get('contacts', {}),
                    }
                )

                saved_count += 1

            except Exception as e:
                errors.append(f"Вакансия {vacancy_id}: {str(e)}")
                continue

        return JsonResponse({
            'status': 'success',
            'saved_count': saved_count,
            'errors': errors,
            'message': f'Успешно сохранено {saved_count} вакансий'
        }, status=200)

    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'Ошибка при парсинге: {str(e)}'
        }, status=500)

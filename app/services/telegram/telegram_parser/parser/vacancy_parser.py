from .keyword_extractor import KeywordExtractor
from .line_parser import LineParser


class VacancyParser(KeywordExtractor):
    def __init__(self):
        super().__init__()

    async def parse_vacancy_from_text(self, text):
        await self.load_keywords()

        lines = text.strip().splitlines()
        parser = LineParser()

        data = dict.fromkeys([
            'post',
            'company',
            'city',
            'salary',
            'link',
            'busyness',
            'phone'])
        data['post'] = next(
            (line.strip() for line in lines if line.strip()), None)

        actions = [
            ('company',
             lambda line: parser.extract_value(line)
             if self.matches(line, 'company') else None),
            ('salary',
             lambda line: parser.extract_salary(line, self.keywords['salary'])
             if self.matches(line, 'salary') else None),
            ('city',
             lambda line: parser.extract_value(line)
             if self.matches(line, 'city') else None),
            ('busyness',
             lambda line: parser.extract_value(line)
             if self.matches(line, 'busyness') else None),
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

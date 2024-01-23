import requests
from datetime import timedelta, datetime
import re


def get_vacancy_details(vacancy_id: str):
    resp = requests.get(f'https://api.hh.ru/vacancies/{vacancy_id}')
    return resp.json()


def get_vacancies():
    params = {
        'text': 'android',
        'period': 1,
        'search_field': 'name'
    }

    resp = requests.get('https://api.hh.ru/vacancies', params=params)
    print(resp.json())
    return resp.json()


def empty():
    return 'Не указано'


def load_vacancies_from_hh():
    vacancies_list = []
    counter = 0
    for vacancy in get_vacancies()['items']:
        if counter == 10:
            break
        data = get_vacancy_details(vacancy['id'])
        name = data['name']

        skills = ''
        for skill in data['key_skills']:
            skills += f"{skill['name']}, "
        skills = skills[:-2]

        try:
            salary = data['salary']['from']
            currency = data['salary']['currency']
        except TypeError:
            salary = empty()
            currency = ''

        if not skills:
            skills = empty()

        if not salary:
            salary = empty()
            currency = ''

        region = data['area']['name']

        template = re.compile('<.*?>')
        description = re.sub(template, '', data['description'])
        template = re.compile('&.*?;')
        description = re.sub(template, '', description)

        company = data['employer']['name']

        date_published = data['published_at'].split('T')[0]

        vacancies_list.append(
            {
                'name': name,
                'desc': description,
                'skills': skills,
                'company': company,
                'price': f"{salary} {currency}",
                'region': region,
                'date_published': date_published
            }
        )
        counter += 1
    return vacancies_list


if __name__ == '__main__':
    load_vacancies_from_hh()

import asyncio

import aiohttp
import requests
import re


async def get_vacancy_details(vacancy_id: str):
    async with aiohttp.ClientSession(trust_env=True) as session:
        async with session.get(f'https://api.hh.ru/vacancies/{vacancy_id}') as resp:
            json = await resp.json()
            return json



#Функция не асинхронна т.к вызывается 1 раз
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


async def load_vacancy_info():
    counter = 0

    remote_vacancies = get_vacancies()['items']

    tasks = []

    for vacancy in remote_vacancies:
        if counter == 10:
            break
        tasks.append(get_vacancy_details(vacancy['id']))
        counter += 1

    detailed_vacancy = await asyncio.gather(*tasks)
    return detailed_vacancy


async def load_vacancies_from_hh():
    vacancies_list = []

    for data in await load_vacancy_info():
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
    return vacancies_list


if __name__ == '__main__':
    load_vacancies_from_hh()

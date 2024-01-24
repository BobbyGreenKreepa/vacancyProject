from django.shortcuts import render

from application.data.vacancies.get_vacancies_from_hh import load_vacancies_from_hh


async def vacancies(request):
    data = await load_vacancies_from_hh()
    content = {'data': data}
    return render(
        request,
        'application/vacancies.html',
        context=content
    )


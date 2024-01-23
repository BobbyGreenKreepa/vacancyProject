from django.shortcuts import render

from application.data.vacancies.get_vacancies_from_hh import load_vacancies_from_hh


def vacancies(request):
    data = load_vacancies_from_hh()
    content = {'data': data}
    return render(
        request,
        'application/vacancies.html',
        context=content
    )


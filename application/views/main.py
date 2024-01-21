from django.shortcuts import render

from application.domain.Vacancy import Vacancy


def main_view(request):
    vacancies = Vacancy.objects.all()
    context = {'data': vacancies}
    for i in vacancies:
        print(i.image)
    return render(
        request,
        'application/main.html',
        context=context
    )
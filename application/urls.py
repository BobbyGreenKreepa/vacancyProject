from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import main, demand, geo, skills, vacancies

urlpatterns = [
    path('demand/', demand.demand),
    path('geo/', geo.geo),
    path('vacancies/', vacancies.vacancies),
    path('skills/', skills.skills),
    path('', main.main_view),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

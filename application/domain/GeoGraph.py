from deprecated.classic import deprecated
from django.db import models

geo_name = 'Название графика'
geo_image = 'Изображение графика'
geo_value = 'Данные зарплат по годам'

geo_verbose_name = 'Гео график'
geo_verbose_name_plural = 'Гео графики'


@deprecated(version='1.1',
            reason="Требования требуют наличие картинки @field: image как поля и возможность загрузки через админку")
class GeoGraph(models.Model):
    title = models.CharField(geo_name, max_length=100)
    image = models.ImageField(geo_image, upload_to='charts/', null=True, blank=True)
    geo_to_vacancy: dict = models.JSONField(geo_value)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = geo_verbose_name
        verbose_name_plural = geo_verbose_name_plural


class GeoModelView:

    def __init__(self, data: dict, image_url: str, title: str):
        self.data = data
        self.image_url = image_url
        self.title = title

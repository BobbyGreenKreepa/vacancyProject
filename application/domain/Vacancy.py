from django.db import models

title = 'Название Вакансии'
description = 'Описание'
image_field = 'Фотография'

verbose_name = 'Профессия'
verbose_name_plural = 'Профессии'


class Vacancy(models.Model):
    title = models.CharField(image_field, max_length=100)
    description = models.TextField(description)
    image = models.ImageField(image_field, blank=True, upload_to='pictures/')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = verbose_name
        verbose_name_plural = verbose_name_plural

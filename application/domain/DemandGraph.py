from django.db import models
from deprecated import deprecated

demand_name = 'Название графика'
demand_image = 'Изображение графика'
demand_value = 'Данные зарплат по годам'

demand_verbose_name = 'График востребованности'
demand_verbose_name_plural = 'Графики востребованности'


class DemandsManager(models.Manager):

    def save_demand_graph(self, title: str, salary_to_year):
        demand_graph = self.create(title=title, salary_to_year=salary_to_year, image=None)
        demand_graph.save()


@deprecated(version='1.1',
            reason="Требования требуют наличие картинки @field: image как поля и возможность загрузки через админку")
class DemandGraph(models.Model):
    title = models.CharField(demand_name, max_length=100)
    image = models.ImageField(demand_image, upload_to='charts/', null=True, blank=True)
    salary_to_year: dict = models.JSONField(demand_value)

    def __str__(self):
        return self.title

    objects = DemandsManager()

    class Meta:
        verbose_name = demand_verbose_name
        verbose_name_plural = demand_verbose_name_plural

from django.contrib import admin
from .domain.DemandGraph import DemandGraph
from .domain.GeoGraph import GeoGraph
from .domain.SkillsGraph import SkillsGraph
from .domain.Vacancy import Vacancy

# Register your models here.

admin.site.register(Vacancy)
admin.site.register(DemandGraph)
admin.site.register(GeoGraph)
admin.site.register(SkillsGraph)

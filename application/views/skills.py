import asyncio

from asgiref.sync import sync_to_async
from django.shortcuts import render

from application.data.skills.get_skills_model_view import get_skills_model_view
from application.domain.SkillsGraph import SkillsGraph


async def skills(request):
    graphs = await sync_to_async(list)(SkillsGraph.objects.all())
    tasks = [get_skills_model_view(graph) for graph in graphs]
    graphs_model_view = await asyncio.gather(*tasks)
    content = {'graphs': graphs_model_view}
    return render(
        request,
        'application/skills.html',
        context=content
    )

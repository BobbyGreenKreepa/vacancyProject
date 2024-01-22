import asyncio

from asgiref.sync import sync_to_async
from django.shortcuts import render

from application.data.geo.get_geo_model_view import get_geo_model_view
from application.domain.GeoGraph import GeoGraph


async def geo(request):
    graphs = await sync_to_async(list)(GeoGraph.objects.all())
    tasks = [get_geo_model_view(graph) for graph in graphs]
    graphs_model_view = await asyncio.gather(*tasks)

    content = {'graphs': graphs_model_view}
    return render(
        request,
        'application/geo.html',
        context=content
    )
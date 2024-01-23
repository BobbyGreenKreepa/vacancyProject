import asyncio

import aiohttp
from asgiref.sync import sync_to_async

from django.shortcuts import render

from application.data.demand.get_demand_model_view import map_demand_to_demand_mv_task
from application.domain.DemandGraph import DemandGraph


async def demand(request):
    graphs = await sync_to_async(list)(DemandGraph.objects.all())
    tasks = [map_demand_to_demand_mv_task(graph) for graph in graphs]
    graphs_model_view = await asyncio.gather(*tasks)
    content = {'graphs': graphs_model_view}
    return render(
        request,
        'application/demand.html',
        context=content
    )

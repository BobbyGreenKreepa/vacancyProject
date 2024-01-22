import random

import aiohttp

from application.domain.SkillsGraph import SkillsGraph, SkillsModelView


async def get_skills_model_view(graph: SkillsGraph):
    graph_data = graph.geo_to_vacancy
    quickchart_url = 'https://quickchart.io/chart/create'

    post_data = {'chart':
        {
            "type": 'bar',
            "data": {
                "labels": list(graph_data.keys()),
                "datasets": [
                    {
                        "label": 'Упоминания',
                        "data": list(graph_data.values()),
                        "backgroundColor": 'rgba(54, 162, 235, 0.5)',
                        "borderColor": 'rgb(54, 162, 235)',
                        "borderWidth": 1,
                    },
                ],
            },
            }
        }
    if graph.image:
        return SkillsModelView(
            data=graph_data,
            image_url=graph.image.url,
            title=graph.title
        )
    async with aiohttp.ClientSession() as session:
        async with session.request(
                method='post',
                url=quickchart_url,
                json=post_data,
                headers={"Content-Type": "application/json"}
        ) as resp:
            response = await resp.json()
            if resp.status != 200:
                return SkillsModelView(
                    data=graph_data,
                    image_url=graph.image.url,
                    title=graph.title
                )
            else:
                return SkillsModelView(
                    data=graph_data,
                    image_url=response['url'],
                    title=graph.title
                )


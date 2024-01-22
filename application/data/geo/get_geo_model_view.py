import random

import aiohttp

from application.domain.GeoGraph import GeoGraph, GeoModelView


async def get_geo_model_view(graph: GeoGraph):
    graph_data = graph.geo_to_vacancy
    quickchart_url = 'https://quickchart.io/chart/create'
    color = ["#" + ''.join([random.choice('0123456789ABCDEF') for j in range(6)])
             for i in range(len(graph_data))]
    post_data = {'chart':
                     {'type': 'outlabeledPie',
                      'data': {'labels':
                                   list(graph_data.keys()),
                               'datasets': [{
                                   'label': graph.title,
                                   'data': list(graph_data.values()),
                                   'backgroundColor': color,
                                }]
                               },
                      "options": {
                          "plugins": {
                              "legend": True,

                          }
                      }
                      }
                 }
    if graph.image:
        return GeoModelView(
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
                return GeoModelView(
                    data=graph_data,
                    image_url=graph.image.url,
                    title=graph.title
                )
            else:
                return GeoModelView(
                    data=graph_data,
                    image_url=response['url'],
                    title=graph.title
                )


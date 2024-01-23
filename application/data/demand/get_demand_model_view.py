import aiohttp

from application.domain.DemandGraph import DemandGraph


async def map_demand_to_demand_mv_task(graph: DemandGraph):
    graph_data = graph.salary_to_year
    quickchart_url = 'https://quickchart.io/chart/create'
    post_data = {'chart':
                     {'type': 'bar',
                      'data': {'labels':
                                   list(graph_data.keys()),
                               'datasets': [
                                   {'label': 'Уровень зарплаты', 'data': list(graph_data.values())
                                    }
                               ]
                            }
                      }
                 }
    if graph.image:
        return DemandModelView(
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
                return DemandModelView(
                    data=graph_data,
                    image_url=graph.image.url,
                    title=graph.title
                )
            else:
                return DemandModelView(
                    data=graph_data,
                    image_url=response['url'],
                    title=graph.title
                )


class DemandModelView:

    def __init__(self, data: dict, image_url: str, title: str):
        self.data = data
        self.image_url = image_url
        self.title = title


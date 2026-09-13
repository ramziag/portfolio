from os import getenv

import requests
from dotenv import load_dotenv

load_dotenv()
api_key = getenv("datawrapper_api_key")


# 1- DatawrapperBarChart: A class to handle configuration and point plotting a locator map in Datawrapper created by this library's "create_map" factory function.
class DatawrapperBarChart:
    # 1.1- Initializing parameters for DatawrapperBarChart class.
    def __init__(self, graphId: str):
        self.graphId = graphId

    ###

    # 1.2- write_metadata: A method used to write metadata needed for a Datawrapper graphic to display properly. Returns a requests.Response object.
    def write_metadata(
        self,
        graphId: str,
        byline: str,
        publish_dimensions: dict,
        title: str | None = None,
        name: str | None = None,
        url: str | None = None,
        intro: str | None = None,
    ):

        headers = {
            "Authorization": f"Bearer {api_key}",
            "content-type": "application/json",
        }
        json_data = {
            "title": title,
            "metadata": {
                "data": {
                    "transpose": False,
                    "vertical-header": True,
                    "horizontal-header": True,
                },
                "publish": {
                    "embed-width": publish_dimensions["embed-width"],
                    "chart-height": publish_dimensions["chart-height"],
                    "embed-height": publish_dimensions["embed-height"],
                },
                "annotate": {"notes": ""},
                "describe": {
                    "intro": intro,
                    "byline": byline,
                    "source-url": url,
                    "source-name": name,
                    "number-append": "",
                    "number-format": "-",
                    "number-divisor": 0,
                    "number-prepend": "",
                },
                "visualize": {
                    "rules": False,
                    "thick": False,
                    "sort-asc": True,
                    "force-grid": False,
                    "resort-bars": False,
                    "block-labels": False,
                    "tick-position": "top",
                    "show-color-key": True,
                    "label-alignment": "left",
                    "value-label-row": True,
                    "value-label-mode": "left",
                    "custom-grid-lines": "",
                    "date-label-format": "YYYY",
                    "hide-group-labels": False,
                    "stack-percentages": False,
                    "highlighted-series": [],
                    "highlighted-values": [],
                    "value-label-format": "0,0.[00]",
                    "value-label-visibility": "show",
                },
                "json_error": "Syntax error",
            },
            "language": "en-US",
        }

        response = requests.patch(
            f"https://api.datawrapper.de/v3/charts/{graphId}",
            headers=headers,
            json=json_data,
        )
        # print("This is the JSON data being passed:")
        # print(json_data)
        # print("These are the params passed:")
        # print(locals())

        return response

    ###

    # 1.3 write_data:
    def write_data(self, graphId: str, chart_data):
        headers = {
            "Authorization": f"Bearer {api_key}",
            "content-type": "text/csv",
        }

        response = requests.put(
            f"https://api.datawrapper.de/v3/charts/{graphId}/data",
            headers=headers,
            data=chart_data,
        )

        return response

    ###

    # 1.4 publish_chart:
    def publish_chart(self, graphId: str):
        headers = {
            "Authorization": f"Bearer {api_key}",
        }
        response = requests.post(
            f"https://api.datawrapper.de/v3/charts/{graphId}/publish?fitchart=true",
            headers=headers,
        )
        return response.json()

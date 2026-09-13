from os import getenv

import requests
from dotenv import load_dotenv

load_dotenv()
api_key = getenv("datawrapper_api_key")


# 1- DatawrapperLineChart: A class to handle configuration and point plotting a locator map in Datawrapper created by this library's "create_map" factory function.
class DatawrapperLineChart:
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
            "metadata": {
                "annotate": {"notes": ""},
                "axes": {},
                "data": {
                    "changes": [],
                    "horizontal-header": True,
                    "transpose": False,
                    "upload-method": "copy",
                    "vertical-header": True,
                },
                "describe": {
                    "aria-description": "",
                    "byline": byline,
                    "intro": intro,
                    "number-append": "",
                    "number-divisor": 0,
                    "number-format": "-",
                    "number-prepend": "",
                    "source-name": name,
                    "source-url": url,
                },
                "publish": {
                    "embed-width": publish_dimensions["embed-width"],
                    "chart-height": publish_dimensions["chart-height"],
                    "embed-height": publish_dimensions["embed-height"],
                },
                "visualize": {
                    "base-color": 0,
                    "chart-type-set": True,
                    "color-category": {"map": {}},
                    "connector-lines": True,
                    "custom-area-fills": [],
                    "custom-range-x": ["", ""],
                    "custom-range-y": ["", ""],
                    "custom-ticks-x": "",
                    "custom-ticks-y": "",
                    "dark-mode-invert": True,
                    "highlighted-series": [],
                    "highlighted-values": [],
                    "interpolation": "linear",
                    "label-colors": False,
                    "label-margin": 0,
                    "overlays": [],
                    "pie_size": {"inside_labels": 75, "outside_labels": 50},
                    "plotHeightFixed": 300,
                    "plotHeightMode": "fixed",
                    "plotHeightRatio": 0.5,
                    "range-annotations": [],
                    "scale-y": "linear",
                    "show-tooltips": True,
                    "text-annotations": [],
                    "value-label-colors": True,
                    "x-grid": "off",
                    "x-grid-format": "auto",
                    "y-grid": "on",
                    "y-grid-format": "auto",
                    "y-grid-label-align": "left",
                    "y-grid-labels": "auto",
                    "y-grid-subdivide": True,
                },
            },
            "title": title,
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

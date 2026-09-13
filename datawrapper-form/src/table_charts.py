from os import getenv

import requests
from dotenv import load_dotenv

load_dotenv()
api_key = getenv("datawrapper_api_key")


# 1- DatawrapperTableChart: A class to handle configuration and point plotting a table chart in Datawrapper created by this library's "create_chart" factory function.
class DatawrapperTableChart:
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
                    "columns": {},
                    "connector-lines": True,
                    "custom-area-fills": [],
                    "custom-range-x": ["", ""],
                    "custom-range-y": ["", ""],
                    "custom-ticks-x": "",
                    "custom-ticks-y": "",
                    "dark-mode-invert": True,
                    "firstColumnIsSticky": False,
                    "firstRowIsHeader": False,
                    "header": {
                        "borderBottom": "2px",
                        "borderBottomColor": "#2e2e2e",
                        "borderTop": "none",
                        "borderTopColor": "#333333",
                        "style": {
                            "background": "#256686",
                            "bold": True,
                            "color": False,
                            "fontSize": 1.1,
                            "italic": False,
                        },
                    },
                    "heatmap": {
                        "categoryLabels": {},
                        "categoryOrder": [],
                        "colors": [],
                        "customStops": [],
                        "hideValues": False,
                        "interpolation": "equidistant",
                        "map": {},
                        "mode": "continuous",
                        "palette": 0,
                        "rangeCenter": "",
                        "rangeMax": "",
                        "rangeMin": "",
                        "stopCount": 5,
                        "stops": "equidistant",
                    },
                    "highlighted-series": [],
                    "highlighted-values": [],
                    "interpolation": "linear",
                    "label-colors": False,
                    "label-margin": 0,
                    "legend": {
                        "customLabels": [],
                        "enabled": False,
                        "hideItems": [],
                        "interactive": False,
                        "labelCenter": "medium",
                        "labelMax": "high",
                        "labelMin": "low",
                        "labels": "ranges",
                        "position": "above",
                        "reverse": False,
                        "size": 170,
                        "title": "",
                    },
                    "lines": {},
                    "markdown": False,
                    "mergeEmptyCells": False,
                    "mobileFallback": False,
                    "overlays": [],
                    "pagination": {"enabled": True, "position": "bottom"},
                    "perPage": 10,
                    "pie_size": {"inside_labels": 75, "outside_labels": 50},
                    "plotHeightFixed": 300,
                    "plotHeightMode": "fixed",
                    "plotHeightRatio": 0.5,
                    "range-annotations": [],
                    "rows": {},
                    "scale-y": "linear",
                    "searchable": False,
                    "show-tooltips": True,
                    "showHeader": True,
                    "showRank": True,
                    "sortDirection": "desc",
                    "sortTable": False,
                    "striped": True,
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

from os import getenv

import requests
from dotenv import load_dotenv

load_dotenv()
api_key = getenv("datawrapper_api_key")


# 1- DatawrapperLocatorMap: A class to handle configuration and point plotting a locator map in Datawrapper created by this library's "create_map" factory function.
class DatawrapperLocatorMap:
    # 1.1- Initializing parameters for DatawrapperLocatorMap class.
    def __init__(self, mapId: str):
        self.mapId = mapId

    ###

    # 1.2- write_metadata: A method used to write metadata needed for a Datawrapper graphic to display properly. Returns a request object.
    def write_metadata(
        self,
        mapId,
        views: dict,
        byline: str,
        publish_dimensions: dict,
        title: str | None = "",
        name: str | None = None,
        url: str | None = None,
        intro: str | None = None,
        zoom: float = 9.0,
    ):

        headers = {
            "Authorization": f"Bearer {api_key}",
            "content-type": "application/json",
        }
        json_data = {
            "title": title,
            "metadata": {
                "describe": {
                    "source-name": name,
                    "source-url": url,
                    "intro": intro,
                    "byline": byline,
                },
                "data": {
                    "json": True,
                },
                "theme": "ACBJ",
                "publish": {
                    "embed-width": publish_dimensions["locator-map"]["embed-width"],
                    "chart-height": publish_dimensions["locator-map"]["chart-height"],
                    "embed-height": publish_dimensions["locator-map"]["embed-height"],
                },
                "visualize": {
                    "view": {
                        "center": views["center"],
                        "zoom": zoom,
                        "fit": {
                            "top": views["fit"]["top"],
                            "right": views["fit"]["right"],
                            "bottom": views["fit"]["bottom"],
                            "left": views["fit"]["left"],
                        },
                        "pitch": 0,
                        "bearing": 0,
                    },
                    "style": "dw-earth",
                    "visibility": {
                        "boundary_country": True,
                        "boundary_state": True,
                        "building": True,
                        "green": True,
                        "mountains": True,
                        "roads": True,
                        "urban": True,
                        "water": True,
                        "building3d": False,
                    },
                    "mapLabel": True,
                    "scale": False,
                    "compass": False,
                    "miniMap": {
                        "enabled": False,
                        "bounds": [],
                    },
                    "key": {
                        "enabled": False,
                        "title": "",
                        "items": [],
                    },
                },
            },
        }

        response = requests.patch(
            f"https://api.datawrapper.de/v3/charts/{mapId}",
            headers=headers,
            json=json_data,
        )

        return response

    ###

    # 1.3- create_points: A method that will create all points on the map. Because this is a "PUT" request, a helper function (build_marker) takes all coordinates in a list and creates them at the same time, resulting in a list of "markers" that is passed as the "PUT" request's "json" argument. Returns the HTTP request's status code.
    def create_points(self, mapId: str, locations: list):

        # 1.3.1- build_marker: A helper function that can be called to batch create multiple markers from inside a list comprehension.
        def build_marker(
            coordinates: list, title: str | None = None, tooltip_text: str | None = None
        ):
            return {
                "type": "point",
                "title": title,
                "icon": {
                    "path": "M714 487a367 367 0 0 0-32-151c-56-125-325-486-325-486s-268 361-325 486a367 367 0 0 0-32 151 360 360 0 0 0 357 363 360 360 0 0 0 357-363z",
                    "height": 700,
                    "width": 1000,
                },
                "scale": 1.2,
                "markerColor": "#256789",
                "anchor": "bottom-center",
                "offsetY": 0,
                "offsetX": 0,
                "text": {"color": "#333333", "fontSize": 15, "halo": "#f2f3f0"},
                "rotate": 0,
                "visibility": {"enabled": "true"},
                "coordinates": coordinates,
                "tooltip": {"text": tooltip_text},
            }

        ###

        headers = {
            "Authorization": f"Bearer {api_key}",
            "content-type": "application/json",
        }

        markers = [
            build_marker(x["coords"], x["title"], x["tooltip"]) for x in locations
        ]

        response = requests.put(
            f"https://api.datawrapper.de/v3/charts/{mapId}/data",
            headers=headers,
            json={"markers": markers},
        )
        return response.status_code

    ###

    # 1.4- publish_map: A method to publish a Datawrapper locator map based on the map ID. Returns the response in JSON format.
    def publish_map(self, mapId):
        headers = {
            "Authorization": f"Bearer {api_key}",
        }
        response = requests.post(
            f"https://api.datawrapper.de/v3/charts/{mapId}/publish?fitchart=true",
            headers=headers,
        )
        return response.json()

    ###

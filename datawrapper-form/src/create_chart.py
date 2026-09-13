from os import getenv

import requests
from dotenv import load_dotenv

# Load & initialize environment variables
load_dotenv()
api_key = getenv("datawrapper_api_key")


# 1- create_chart: A factory function for initializing a Datawrapper chart, viewable on user's Datawrapper dashboard after running the function. Returns a chart ID which can be passed as the argument when initializing a DatawrapperLocatorMap object.
def create_chart(chart_title: str, type: str) -> str:

    # Request headers including API key
    headers = {
        "Authorization": f"Bearer {api_key}",
        "content-type": "application/json",
    }

    # Data to be passed into POST request, map title should go here
    json_data = {
        "title": chart_title,
        "type": type,
    }

    response = requests.post(
        "https://api.datawrapper.de/v3/charts", headers=headers, json=json_data
    )
    response_id: str = response.json()["publicId"]

    return response_id


###

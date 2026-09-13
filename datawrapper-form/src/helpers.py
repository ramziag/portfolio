import requests


# 1- A helper function to geocode single-string and return x & y values in a list. Address should be entered as a single string.
def geocode_address(address: str) -> list:
    url = "https://geocoding.geo.census.gov/geocoder/locations/onelineaddress"

    payload: dict = {
        "address": address,
        "format": "json",
        "benchmark": "4",
        "vintage": "420",
    }

    response = requests.get(url, params=payload)
    r_json = response.json()

    return [
        r_json["result"]["addressMatches"][0]["coordinates"]["x"],
        r_json["result"]["addressMatches"][0]["coordinates"]["y"],
    ]


###


# 2- compute_view: A function to compute the centroid coordinates and bounds of a Datawrapper locator map.
def compute_view(coords, padding: float = 0.1) -> dict:
    lons: list = [c[0] for c in coords]
    lats: list = [c[1] for c in coords]
    lon_pad: float = (max(lons) - min(lons)) * padding
    lat_pad: float = (max(lats) - min(lats)) * padding
    return {
        "center": [sum(lons) / len(lons), sum(lats) / len(lats)],
        "fit": {
            "top": [(min(lons) + max(lons)) / 2, max(lats) + lat_pad],
            "bottom": [(min(lons) + max(lons)) / 2, min(lats) - lat_pad],
            "left": [min(lons) - lon_pad, (min(lats) + max(lats)) / 2],
            "right": [min(lons) + lon_pad, (min(lats) + max(lats)) / 2],
        },
    }



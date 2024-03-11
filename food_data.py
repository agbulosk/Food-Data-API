"""
Sample API to get food recipes from https://developer.edamam.com/edamam-docs-recipe-api?cms=published
"""

import json

import pandas as pd
import requests


def main():
    r = get_request()
    parse_data(r)


# test


def get_request():
    app_id = "b2fb016a"
    app_key = "65d2e261e108d69493c989446fa678e2"
    link = "https://api.edamam.com/api/recipes/v2"
    params = {
        "type": "public",
        "app_id": app_id,
        "app_key": app_key,
        "cuisineType": "Italian",
    }
    r = requests.get(link, params=params)
    if r.status_code != 200:
        r.raise_for_status()
    else:
        return r


def parse_data(r):
    data_dict = json.loads(r.text)
    hit = data_dict["hits"][0]
    # figure out how to print the first 10 columns and 10 rows
    print(pd.json_normalize(hit))


if __name__ == "__main__":
    main()

"""
Sample API to get food recipes from https://developer.edamam.com/edamam-docs-recipe-api?cms=published
"""

import json
from pathlib import Path

import pandas as pd
import requests


def main() -> None:
    """
    Main function for extracting data from the API to get recipes and visualize data into a report.

    Returns:
        None.
    """
    r = get_request()
    df = parse_data(r)
    cleaned_df = convert_data(df)
    export_data(df)


def get_request() -> requests.models.Response:
    """
    Connects to the API to get a response object.

    Returns:
        Response object.
    """
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


def parse_data(r: requests.models.Response) -> pd.DataFrame:
    """
    Parse the JSON data and extract data from the "hits" key and flattens the data into a DataFrame.

    Args:
        r: Response object.

    Returns:
        DataFrame.
    """
    data_dict = json.loads(r.text)
    hits = data_dict["hits"]
    keys_to_extract = [
        "url",
        "label",
        "dietLabels",
        "healthLabels",
        "ingredientLines",
        "ingredients",
        "calories",
        "cuisineType",
        "mealType",
        "dishType",
        "instructions",
        "tags",
        "totalNutrients",
    ]
    flattened_hits = []
    for hit in hits:
        recipe_data = {
            key: hit["recipe"][key] for key in hit["recipe"] if key in keys_to_extract
        }
        flattened_recipe = pd.json_normalize(recipe_data)
        flattened_hits.append(flattened_recipe)

    # Concatenate all flattened recipes into one DataFrame
    return pd.concat(flattened_hits, ignore_index=True)


def convert_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the data for reporting use.

    Args:
        df: DataFrame.

    Returns:
        DataFrame.
    """


def export_data(df: pd.DataFrame) -> None:
    """
    Export the dataframe to a CSV file.

    Args:
        df: DataFrame.

    Returns:
        None.
    """
    # Get the path to the Downloads folder
    filename = "food"
    output_folder = Path(r"C:\Users\kevin\Downloads") / filename
    df.to_excel(output_folder.with_suffix(".xlsx"), index=False)


if __name__ == "__main__":
    main()

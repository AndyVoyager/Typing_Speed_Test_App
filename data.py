__author__ = "AndyVoyager"

import requests
import os

API = os.environ.get("TEXT_API")  # your API in TextCortex
URL = "https://api.textcortex.com/v1/texts/blogs"


# _______________________________Bacon Version:________________________________________________________________________
# PARAMETERS = {"type": "all-meat",
#               "paras": 10,
#               "sentences": 20}
# URL = "https://baconipsum.com/api/?"
#
#
# def get_data():
#     """
#     Function to retrieve data from a specified URL using GET request with parameters and returning the first element
#     from the JSON response.
#     """
#     response = requests.get(url=URL, params=PARAMETERS)
#     response.raise_for_status()
#     return response.json()[0]


# _______________________________TextCortex Version:___________________________________________________________________
def get_data(theme):
    """
    Retrieves data from a specified URL using a POST request with JSON payload and returns the first output text.

    Parameters:
        theme (str): The context or theme for the data retrieval.

    Returns:
        str: The first output text from the response JSON.
    """
    payload = {
        "context": theme,
        "formality": "default",
        "keywords": ["string"],
        "max_tokens": 2048,
        "model": "chat-sophos-1",
        "n": 1,
        "source_lang": "en",
        "target_lang": "en",
        "temperature": 0.65,
        "title": "string",
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API}"
    }

    response = requests.request("POST", URL, json=payload, headers=headers)
    # print(response.json())
    return response.json()["data"]["outputs"][0]["text"]

# print(get_data())

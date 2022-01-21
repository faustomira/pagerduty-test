import requests
import json
import logging
from commons.utils import setup_logging
import os

SOURCE_KEY = os.getenv('SOURCE_API_TOKEN')
TARGET_KEY = os.getenv('TARGET_API_TOKEN')

base_url = "https://api.pagerduty.com/teams"

headers = {
    "Content-Type": "application/json",
    "Accept": "application/vnd.pagerduty+json;version=2"
}

logger = setup_logging()

def retrieve_teams_id(api_key):
    headers["Authorization"] = f"Token token={api_key}"
    response = requests.request("GET", base_url, headers=headers)

    status_code = response.status_code

    id_list = []

    for r in response.json()['teams']:
        id_list.append(r["id"])

    return id_list


def retrieve_teams_details(api_key):
    id_list = retrieve_teams_id(api_key)
    teams_list = []
    headers["Authorization"] = f"Token token={api_key}"
    # iterate over each ID to retrieve full information
    for item in id_list:
        url = f"{base_url}/{item}"

        response = requests.request("GET", url, headers=headers)
        #print(response.text)
        teams_list.append(response.json())

    return teams_list


def insert_teams_target(payload: dict(), api_key):
    headers["Authorization"] = f"Token token={api_key}" 
    response = requests.request("POST", base_url, headers=headers, json=payload)

    if response.status_code == 201:
        logger.info(f"Team '{payload['team']['name']}' successfuly migrated")
        return response
    elif response.status_code == 400:
        logger.error("Invalid arguments provided")
    elif response.status_code == 401:
        logger.error("Wrong credentials provided")    
    else:
        logger.error(f"Error log: failure upon replicating data: {payload}")    


def handle_migrate():

    teams_list = retrieve_teams_details(SOURCE_KEY)
    for team in teams_list:
        logger.info(f"Migrating '{team['team']['name']}' team")
        payload = {"team": {
            "type": "team",
            "name": team['team']['name'] + " (invalid team)",
            "description": team['team']['description']}}
        response = insert_teams_target(payload, TARGET_KEY)
        logger.info(response.json())


if __name__ == "__main__":
    handle_migrate()
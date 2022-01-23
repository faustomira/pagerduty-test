import requests
import json
import logging
from commons.utils import setup_logging
import os

SOURCE_KEY = os.getenv('SOURCE_API_TOKEN')
TARGET_KEY = os.getenv('TARGET_API_TOKEN')

base_url = "https://api.pagerduty.com"

headers = {
    "Content-Type": "application/json",
    "Accept": "application/vnd.pagerduty+json;version=2"
}

logger = setup_logging()

def retrieve_entity_id(api_key, entity):
    url = f"{base_url}/{entity}"
    headers["Authorization"] = f"Token token={api_key}"
    response = requests.request("GET", url, headers=headers)

    status_code = response.status_code

    id_list = []

    if status_code == 200:
        for r in response.json()[entity]:
            id_list.append(r["id"])
    
    return id_list


def retrieve_entity_details(api_key, entity):
    id_list = retrieve_entity_id(api_key, entity)
    entity_list = []
    headers["Authorization"] = f"Token token={api_key}"
    # iterate over each ID to retrieve full information
    for item in id_list:
        url = f"{base_url}/{entity}/{item}"

        response = requests.request("GET", url, headers=headers)
        #print(response.text)
        entity_list.append(response.json())

    return entity_list


def retrieve_entity_full(api_key, entity):
    """Retrieves the complete response of a certain entity like teams and users.
    This exempts the need to retrieve each instance of a certain entity 
    by invoking the GET verb upon base_url/{entity}/{id} individually

    Args:
        api_key (str): API Token to be passsed as auth
        entity (str): Which entity one needs to access

    Returns:
        list: A list of appended resulting responses
    """
    entity_list = []
    headers["Authorization"] = f"Token token={api_key}"
    url = f"{base_url}/{entity}"
    response = requests.request("GET", url, headers=headers).json()

    # iterate over each ID to retrieve full information
    for item in response[entity]:
        #print(response.text)
        entity_list.append(item)

    return entity_list


def insert_entity_target(payload: dict(), api_key, entity):
    url = f"{base_url}/{entity}"
    headers["Authorization"] = f"Token token={api_key}" 
    response = requests.request("POST", url, headers=headers, json=payload)

    if response.status_code == 201:
        logger.info(f"{entity} '{payload['name']}' successfuly migrated")
    elif response.status_code == 400:
        logger.error("Invalid arguments provided")
    elif response.status_code == 401:
        logger.error("Wrong credentials provided")    
    else:
        logger.error(f"Error log: failure upon replicating data: {payload}")

    return response

def handle_migrate():

    teams_list = retrieve_entity_full(SOURCE_KEY, 'teams')
    users_list = retrieve_entity_full(SOURCE_KEY, 'users')

    for team in teams_list:
        logger.info(f"Migrating '{team['name']}' team")
        team["name"] += " (invalid team)"
        response = insert_entity_target(team, TARGET_KEY, 'teams')
        logger.info(response.json())

    for user in users_list:
        logger.info(f"Migrating '{user['name']}' user")

        user['name'] += " (invalid user)"
        response = insert_entity_target(user, TARGET_KEY, 'users')
        logger.info(response.json())

if __name__ == "__main__": 
    handle_migrate()
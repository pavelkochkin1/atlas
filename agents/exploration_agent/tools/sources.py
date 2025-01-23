from typing import List

import requests


def get_db_schema() -> List[str]:
    url = "http://sources_examples:8043/schema"
    response = requests.get(url)
    response_json = response.json()

    return response_json["tables"]


def get_code_from_gitlab(table_name: str) -> str:
    url = "http://sources_examples:8043/gitlab"
    response = requests.get(url, params={"table": table_name})

    respose_json = response.json()

    result = f"file_name: {respose_json['results'][0]['file_name']}\n\ncontet:\n{respose_json['results'][0]['content']}"

    return result


def get_code_from_confluence(table_name: str) -> str:
    url = "http://sources_examples:8043/confluence"
    response = requests.get(url, params={"table": table_name})

    respose_json = response.json()

    result = f"file_name: {respose_json['results'][0]['file_name']}\n\ncontet:\n{respose_json['results'][0]['content']}"

    return result


def get_teams() -> str:
    url = "http://atlas_backend:8073/api/entities/teams/"
    response = requests.get(url)

    respose_json = response.json()

    return respose_json


def get_person(email: str) -> str:
    url = f"http://atlas_backend:8073/api/entities/persons/{email}"
    response = requests.get(url)

    respose_json = response.json()

    return respose_json

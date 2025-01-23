from typing import List

import requests


def get_processed_tables() -> List[str]:
    url = "http://atlas_backend:8073/api/entities/tables/"
    response = requests.get(url)

    tables = []
    for table in response.json():
        tables.append(table["name"])

    return tables

import json
import re


def str2json(s: str) -> dict:
    pattern = r"\{.*\}"
    match = re.search(pattern, s, flags=re.DOTALL)

    if not match:
        print("Не удалось найти JSON-объект в тексте")
        return {}

    json_str = match.group(0)

    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        print("Ошибка при разборе JSON:", e)
        return {}

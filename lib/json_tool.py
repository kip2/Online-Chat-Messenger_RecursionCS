import json


def save_json(dic: dict, filepath: str) -> None:
    with open(filepath, "w") as f:
        json.dump(dic, f)

def load_json(filepath: str) -> None:
    with open(filepath, "r") as f:
        d = json.load(f)
    return d
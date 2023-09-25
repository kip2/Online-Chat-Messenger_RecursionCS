import json

def save_json(dic: dict, filepath: str) -> None:
    with open(filepath, "w") as f:
        json.dump(dic, f)

def load_json(filepath: str) -> None:
    with open(filepath, "r") as f:
        d = json.load(f)
    return d

def save_arr_json(arr: list, filepath: str) -> None:
    with open(filepath, "w") as f:
        json.dump(arr, f)

def test_save_arr_json():
    arr = []
    arr.append(("name1", "message1"))
    arr.append(("name3", "message3"))
    arr.append(("name2", "message2"))
    filepath = "./temp/test.json"
    save_arr_json(arr, filepath)

def test_load_arr_json():
    filepath = "./temp/test.json"
    d = load_json(filepath)
    print(d)

if __name__ == "__main__":
    # test_save_arr_json()
    test_load_arr_json()

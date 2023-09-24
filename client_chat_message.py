import json
import ndjson

FILEPATH = "./json/save_test.json"

# nameとmessage取得は別に行う必要がある

class ClientChatMessage():
    def __init__(self,number:int, name:str, message:str):
        self.number = number
        self.name = name
        self.message = message

    def tansfer_json(self) -> dict:
        data = {
            "name": self.name,
            "message": self.message
        }
        return data 

    def create_message(self):
        return self.name + ":" + self.message

def save_json(dict: dict, filepath: str) -> None:
    with open(filepath, "a") as f:
        writer = ndjson.writer(f)
        writer.writerow(dict)
        # json.dump(dict, f)

def send_chat_message(number:int, name:str, message:str):
    chat_message1 = ClientChatMessage(number, name, message)
    save_json(chat_message1.tansfer_json(), FILEPATH)

def load_json(filepath: str):
    with open(filepath, "r") as f:
        d = json.load(f)
    return d
        

# ----- test case -----

def send_caht_message_test():
    name = input("名前を入力してください: ")
    message = "It's me "+name+"!"
    
def save_json_test(number: int, name:str, message:str):
    # name = input("名前を入力してください: ")
    # message = "It's me "+name+"!"
    filepath = "./json/save_test.ndjson"
    chat_message1 = ClientChatMessage(number,name, message)
    save_json(chat_message1.tansfer_json(), filepath )

def transfer_message_to_json_test(number:int,name:str, message:str) -> str:
    # name = input("名前を入力してください: ")
    # message = "It's me "+name+"!"
    chat_message1 = ClientChatMessage(number,name, message)
    print(chat_message1.create_message())
    print(chat_message1.tansfer_json())
    
def test_load_json():
    filepath = "./json/save_test.ndjson"
    d = load_json(filepath)
    print(d)

def test_add_save_json():
    filepath = "./json/save_test.ndjson"
    dict = {"name2": "name2 message!",
            "name3": "name3 message!",
            "name4": "name4 message!",
            "name5": "name5 message!",
            }
    save_json(dict, filepath)
    
    
if __name__ == "__main__":
    # name = input("名前を入力してください: ")
    # message = "It's me "+name+"!"
    # number = 0

    # transfer_message_to_json_test(number, name, message)
    # save_json_test(number,name, message)
    
    #test_load_json()
    test_add_save_json()

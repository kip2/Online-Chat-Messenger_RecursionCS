import os
from lib.udp_client import * 
from lib.json_tool import *

import lib

JSON_DIRECTORY_PATH = "json"
ROOM_LIST_PATH = "./json/room_list.json"

def get_room_list() -> dict:
    # todo: filepathが存在しているかを確認する
    # todo: ない場合は、room_listを要求するようにすること
    # todo: 要求したroom_listがない場合は、ルームの作成に入ること
    if os.path.exists(ROOM_LIST_PATH):
        d = load_json(ROOM_LIST_PATH)
        return d
    return None

def create_json_directory():
    """
        json受け渡しをするjsonフォルダを作成する
    """
    if not os.path.exists(JSON_DIRECTORY_PATH):
        os.makedirs(JSON_DIRECTORY_PATH)

def print_room_list(room_list):
    print("----------------------------------")
    print("----------room list---------------")
    print("-- 部屋名 ---------- 参加可能人数 -")
    print("----------------------------------")
    for k, v in room_list.items():
        print("|", end=" ")
        # print("部屋名:", k, " 参加可能人数:", v, end="")
        space = " " * (27 - len(k))
        print(k, space, v, end=" ")
        print("|")
    print("----------------------------------")
    print("----------room list---------------")
    print("----------------------------------")

def select_enter_room():
    pass

def chat_client():

    # room listの取得
    room_list = get_room_list() 

    # room listがない場合
    if room_list == None:
        # todo: ない場合の処理はまだ
        # todo: room作成の処理に写ってよいと思う
        pass

    print_room_list(room_list)

    select_enter_room()


if __name__ == "__main__":
    chat_client()
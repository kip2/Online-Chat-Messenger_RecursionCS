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

def create_json_directory() -> None:
    """
        json受け渡しをするjsonフォルダを作成する
    """
    if not os.path.exists(JSON_DIRECTORY_PATH):
        os.makedirs(JSON_DIRECTORY_PATH)

def print_room_list(room_list: dict) -> None:
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
    print()

def room_exists(room: str, room_list: dict) -> bool:
    """
        roomの一覧に部屋が存在するかを確認
    """
    for room_name in room_list.keys():
        if room == room_name: return True
    return False


def select_enter_room(room_list: dict) -> str:
    """
        入室する処理を行う
    """
    # エラーメッセージ
    err_message = "!!そのような名前の部屋はありません!!"
    # エラーメッセージ用フラグ
    err_flg = False

    while True:
        # roomの一覧を表示する
        print_room_list(room_list)
        if err_flg: print(err_message)

        room = input("入室する部屋を選んでください : ")
        if room_exists(room, room_list): break
        else: err_flg = True

    # 選択した部屋の名前
    return room

def enter_room(room: str):
    """ 
        入室処理を行う関数
    """ 
    pass

def request_room_message_log(room):
    pass

# todo
def request_room_list():
    pass


def chat_client():

    # room listの取得
    room_list = get_room_list() 

    # room listがない場合
    if room_list == None:
        # todo: ない場合の処理はまだ
        # todo: room作成の処理に写ってよいと思う
        request_room_list()
        pass

    # 入る部屋を選択する
    room = select_enter_room(room_list)

    # 部屋のログを取得する
    log = request_room_message_log(room)


if __name__ == "__main__":
    chat_client()
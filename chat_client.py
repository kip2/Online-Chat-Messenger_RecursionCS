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
        # 部屋の人数が規定人数であれば"full"と表示する
        if is_full_member(v): k += " full!"
        # 文字レイアウト整形用
        space = " " * (27 - len(k))
        print(k, space, v[0], end=" ")
        print("|")
    print("----------------------------------")
    print()

def is_full_member(members: tuple) -> bool:
    """
        人数が規定人数に達しているかを判定
    """
    if members[0] == members[1] :return True
    return False


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
    err_message = ""

    while True:
        # roomの一覧を表示する
        print_room_list(room_list)
        if err_message != "": print(err_message)

        room = input("入室する部屋を選んでください : ")

        # リストにない名前を選択した場合
        if not room_exists(room, room_list): 
            err_message = "   そのような部屋は存在していません   "
            continue
        
        # 選択した部屋の人数が最大の場合
        if is_full_member(room_list[room]):
            err_message = "   人数がいっぱいで入れません  "
            continue

        # そうでなければ入室OK
        break
    # 選択した部屋の名前を返す
    return room

def enter_room(room: str) -> bool:
    """ 
        入室処理を行う関数
    """ 
    # tcpclientを作成する

    # 入室する旨を知らせる
        # headerがいる
        # 入室処理は別のファイルで作成してなかった？
    
    # 入室NGの場合
    # 人数オーバー
    return False

    # 入室OKの場合
    return True
    
    pass

# todo
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

    # 入室処理をループする
    while True:
        # 入室できたらループを抜ける
        if enter_room(room): break
        # 入室失敗なら別の部屋を選択する
        else: room = select_enter_room(room_list)

    # 部屋のログを取得する
    log = request_room_message_log(room)

def test_print_room_list():
    # room listの取得
    room_list = get_room_list() 
    print_room_list(room_list)


if __name__ == "__main__":
    chat_client()
    # test_print_room_list()
from lib.udp_server import * 
from lib.json_tool import *
import os
import pathlib

# json save directory
JSON_DIRECTORY_PATH = "json"

# 保存パス
ROOM_LIST_FILEPATH = "./json/room_list.json"

# logファイルの保存パス
ROOM_LOG_PATH = "./json/room_log/"

# メッセージフォーマット用のspace
MESSAGE_SPACE = 3

chat_clients = []

class ChatClient:
    """
        field:
            name:       クライアントのユーザーネーム
            address:    クライアントのアドレス
            port:       クライアントのポート番号
    """
    def __init__(self, name :str, address: str, port: str):
        # validationは不要
        self.name: str = name
        self.address: str = address
        self.port: str = port
    
    def get_address(self):
        """
            addressをタプルに直して返す
            message送信用
        """
        return (self.address, self.port)

class ChatRoom():
    """
        field:
            name:       チャットルームの名前
            max_member:  チャットルームの最大参加人数

            room_log:    roomのメッセージlog格納配列。右の形式 -> (name, message)
            client_list: 入室しているクライアント情報
            ljust_max:   チャットメッセージの文字列整形管理用
    """
    # roomのメッセージログ
    room_log = []
    # client HashMap
    client_list = {}
    # チャットメッセージ文字列整形用
    ljust_max = 0
    
    def __init__(self, name: str, max_member: int):
        # todo: validationがいる
        self.name: str = name
        self.max_member: int = max_member
        self.create_log_file()

    # def __del__(self):
    #     """
    #         デストラクター
    #         pythonプログラム終了時に動作
    #     """
    #     print("destracter")
    #     super().__exit__()
        # self.sock.close()

    # # with文のため
    # def __enter__(self):
    #     return self
    
    # with文のため
    # def __exit__(self, *args):
        # super().__exit__()
        # self.sock.close()

    # def room_socket_create(self):
    #     """
    #         chatroomのサーバーを作成する
    #     """
    #     self.sock, self.address, self.port = startup_udp_server()

    def create_client_and_enter_chat_room(self, name: str, address: str, port: int):
        """
            クライエント作成と入室を同時にする
        """
        chat_client = ChatClient(name, address, port)
        self.enter_chat_room(chat_client)

    def has_chat_client(self, chat_client: ChatClient) -> bool:
        """
            このroomにクライアントが存在するか確認
        """
        if chat_client.name in self.client_list:
            return True
        return False

    def enter_chat_room(self, chat_client: ChatClient) -> bool:
        """
            roomに初めて入室したクライエントを登録する
        """
        if self.max_member <= len(self.client_list):
            return False
        if not self.has_chat_client(chat_client):
            # メッセージ整形用の数字を計算
            self.generate_message_format(chat_client.name)
            # クライアントを登録する
            self.client_list[chat_client.name] = chat_client
            return True
        return False
    
    def create_send_message(self, name: str, message: str) -> str:
        """
            整形したメッセージ文章を送信
        """
        space = (self.ljust_max - len(name)) * " "
        return name + space + ":" + " " + message

    def create_file_path(self):
        """
            roomのmessagelogのパスを返す
        """
        return ROOM_LOG_PATH + self.name + ".json"

    def create_log_file(self):
        """
            roomのlogファイルを作成する
        """
        filepath = self.create_file_path()
        if not os.path.exists(filepath):
            touch_file = pathlib.Path(filepath)
            touch_file.touch()

    def udp_message_broadcast(self, sock, name: str, message:str):
        """
            roomのclientへのブロードキャスト
        """
        message = self.create_send_message(name, message)
        for client in self.client_list.values():
            send_udp_message(sock, client.get_address(), message)
    
    def exit_client(self, chat_client: ChatClient):
        """
            chat roomからclientを退室させる処理
        """
        self.regenerate_message_format()
        del self.client_list[chat_client.name]

    def generate_message_format(self, client_name: str):
        """
            新しいクライアントがnewされた時に実行すること
            チャットメッセージの名前の最大文字数から、メッセージとの適切な感覚を調整
        """
        new_ljust_max = MESSAGE_SPACE + len(client_name)
        if new_ljust_max >= self.ljust_max: self.ljust_max = new_ljust_max

    def regenerate_message_format(self) -> int:
        """
            新しいクライアントがnewされた時に実行する
            チャットメッセージの名前の最大文字数から、メッセージとの適切な感覚を調整
        """
        max = 0
        for client_name in self.client_list:
            if len(client_name) >= max: max = len(client_name)
        self.ljust_max = max + MESSAGE_SPACE

class ChatRooms:
    # このクラス唯一のインスタンス 
    _instance = None

    # chatrooms配列。singletonにより、ただ一つ管理されることが保証
    chat_rooms = {}

    # __new__を書き換えてsingletonに
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ChatRooms, cls).__new__(cls)
            cls._instance.initialize()
        return cls._instance

    # 初期化処理
    def initialize(self):
        self.deserialize_json_data()
        pass

    def save_json_file(self):
        """
            room listをjsonデータに保存する
        """
        d = self.convert_json_data()
        save_json(d, ROOM_LIST_FILEPATH)

    def convert_json_data(self):
        """
            room_listをjsonデータで使用する形式に変換する
        """
        json_dict = {}
        for room_name, room in self.chat_rooms.items():
            json_dict[room_name] = room.max_member
        return json_dict
    
    def deserialize_json_data(self):
        """ 
            jsonファイルからroom listを読み込む
        """ 
        d = load_json(ROOM_LIST_FILEPATH)
        for room_name, max_member in d.items():
            self.append_room(ChatRoom(room_name, max_member))
        pass

    def has_chat_room(self, room_name:str) -> bool:
        """
            該当の名前のroomが存在するか確認する
        """
        if room_name in self.chat_rooms:
            return True
        return False

    def append_room(self, room: ChatRoom) -> bool:
        """
            chatroomを登録する
        """
        if room.name not in self.chat_rooms:
            self.chat_rooms[room.name] = room
            return True
        return False
        
    def remove_room(self, room: ChatRoom):
        """
            指定されたchatroomの登録を削除する
        """
        if room.name in self.chat_rooms:
            del self.chat_rooms[room.name]

    def get_room(self, room_name:str) -> ChatRoom:
        """
            roomの名前から、ルームを返す
            listになければNoneを返す
        """
        if room_name in self.chat_rooms:
            return self.chat_rooms[room_name]
        else: return None
    
    def get_room_list(self) -> list:
        """
            roomのリストを返す
        """
        room_list = []
        for k in self.chat_rooms.keys():
            room_list.append(k)
        return room_list

def create_json_directory():
    """
        json受け渡しをするjsonフォルダを作成する
    """
    if not os.path.exists(JSON_DIRECTORY_PATH):
        os.makedirs(JSON_DIRECTORY_PATH)

def chat_room_create(room_name: str, max_member: int):
    """
        chat_roomを作成し、辞書に登録する
    """
    chat_rooms = ChatRooms()
    chat_room = ChatRoom(room_name, max_member)

    # チャットルーム辞書にチャットルームを追加
    chat_rooms.append_room(chat_rooms)
    return chat_room


def send_error_message(sock, client_address:tuple, message:str):
    send_udp_message(sock, client_address, message)


# -------------------
# ---- test code ----
# -------------------

def test_chatrooms_append():
    room_list = ChatRooms()

    # singleton room append test
    room = ChatRoom("room1", 5)
    assert "room1" ,room.name
    room_list.append_room(room) 
    assert "room1", room_list.chat_rooms[0].name

def test_chatrroms_get():
    room_list = ChatRooms()

    # singleton room append test
    room = ChatRoom("room1", 5)
    assert room, room_list.chat_rooms["room1"]
    assert room, room_list.get_room("room1")

def test_char_room_create():
    room = chat_room_create("room1", 5)
    assert "room1" ,room.name

def test_singleton_class():
    # singleton test
    singleton1 = ChatRooms()
    singleton2 = ChatRooms()

    # 同じインスタンスなのでTrueになる
    assert True, (singleton1 is singleton2)

def test_chatrooms_append():
    room_list = ChatRooms()

    # singleton room append test
    room = ChatRoom("room1", 5)
    assert "room1" ,room.name
    room_list.append_room(room) 
    assert "room1", room_list.chat_rooms[0].name

def test_chatrooms_remove():
    
    room_list = ChatRooms()
    room1 = ChatRoom("room1", 5)
    room2 = ChatRoom("room2", 5)
    room3 = ChatRoom("room3", 5)
    room4 = ChatRoom("room4", 5)
    room5 = ChatRoom("room5", 5)
    room6 = ChatRoom("room6", 5)
    room7 = ChatRoom("room7", 5)
    
    room_list.append_room(room1) 
    room_list.append_room(room2) 
    room_list.append_room(room3) 
    room_list.append_room(room4) 
    room_list.append_room(room5) 
    room_list.append_room(room6) 
    room_list.append_room(room7) 

    print("現在のリスト")
    print(room_list.chat_rooms)
    print()


    room_list.remove_room(room1) 
    room_list.remove_room(room2) 
    room_list.remove_room(room3) 
    room_list.remove_room(room4) 
    room_list.remove_room(room5) 
    room_list.remove_room(room6) 
    room_list.remove_room(room7) 

    print("現在のリスト")
    print(room_list.chat_rooms)
    print()



def test_chat_room():

    room = ChatRoom("room1", 5)
    print("room:", room, "name:", room.name)
    
    cl1 = ChatClient("taro", "address", 9001)
    print("client:", cl1, "name:", cl1.name)

    # new clients
    cl2 = ChatClient("jiro", "address", 9002)
    print("client:", cl2, "name:", cl2.name)

    cl3 = ChatClient("saburo", "address", 9003)
    print("client:", cl3, "name:", cl3.name)

    cl4 = ChatClient("shiro", "address", 9004)
    print("client:", cl4, "name:", cl4.name)

    cl5 = ChatClient("goro", "address", 9005)
    print("client:", cl5, "name:", cl5.name)

    # enter room
    room.enter_chat_room(cl1)
    print(room.ljust_max)
    room.enter_chat_room(cl2)
    print(room.ljust_max)
    room.enter_chat_room(cl3)
    print(room.ljust_max)
    room.enter_chat_room(cl4)
    print(room.ljust_max)
    room.enter_chat_room(cl5)
    print(room.ljust_max)

    # debug print
    print("room name:", room.name, "room member:",[ x for x in room.client_list] )

    # client exit room
    room.exit_client(cl1)
    print("room name:", room.name, "room member:", [ x for x in room.client_list] )
    room.exit_client(cl2)
    print(room.ljust_max)
    print("room name:", room.name, "room member:", [ x for x in room.client_list] )
    room.exit_client(cl3)
    print(room.ljust_max)
    print("room name:", room.name, "room member:", [ x for x in room.client_list] )
    room.exit_client(cl4)
    print(room.ljust_max)
    print("room name:", room.name, "room member:", [ x for x in room.client_list] )
    room.exit_client(cl5)
    print(room.ljust_max)
    print("room name:", room.name, "room member:", [ x for x in room.client_list] )

def test_room_log_path():
    room1 = ChatRoom("room1", 5)
    print(room1.create_file_path())

def test_create_log_file():
    room1 = ChatRoom("room1", 5)
    room1.create_log_file()
    
if __name__ == "__main__":

    test_create_log_file()
    # test_room_log_path()
    # test_singleton_class()
    
    # test_chatrooms_remove()
    # test_char_room_create()
    # test_chatrooms_append()

    pass

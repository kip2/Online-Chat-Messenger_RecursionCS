import sys
from client import *
from server import *

# チャットルームの辞書配列
chat_rooms= {}

# チャットメッセージ文字列整形用
ljust_max = 0


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

class ChatRoom:
    """
        field:
            title:       チャットルームの名前
            max_member:  チャットルームの最大参加人数
            // todo
            // サーバークリエイト時にランダムな値を生成する
            address:     アドレス
            port:        ポート番号
    """
    # client HashMap
    client_list = {}
    # チャットメッセージ文字列整形用
    ljust_max = 0
    
    def __init__(self, title: str, max_member: int):
        # validationがいる
        self.title: str = title
        self.max_member: int = max_member
        #self.room_server_create()

    def create_client_and_enter_chat_room(self, name, address, port):
        """
            クライエント作成と入室を同時にする
        """
        chat_client = ChatClient(name, address, port)
        self.enter_chat_room(chat_client)

    def enter_chat_room(self, chat_client: ChatClient):
        """
            roomに入室したクライエントを登録する
        """
        self.client_list[chat_client.name] = chat_client

    def room_server_create():
        """
            chatroomのサーバーを作成する
        """
        pass

def chat_room_create(room_name: str, max_member: int):
    """
        chat_roomを作成し、辞書に登録する
    """
    chat_room = ChatRoom(room_name, max_member)

    # チャットルーム辞書にチャットルームを追加
    chat_rooms[room_name] = chat_room
    return chat_room

def create_new_chat_room():
    """
        新しいチャットルームを作成する関数
    """
    while True:
        room_name = input("Room Name? > ")
        if not room_name == ""  and not room_name.isspace(): break
        
    while True:
        max_member = input("maximum number? > ")
        if max_member.isdecimal(): break
    chat_room_create(room_name, max_member)
    return
    

if __name__ == "__main__":
    pass
def prologue():
    print("Welcome Online chat Messenger!")
    print("Make your chat room!")

    # 最初なので、ルームを作成
    chat_room = create_new_chat_room()
    return 

"""
    test cases
"""

def test():
    rooms = {"room1":5,
            "room2":3,
            "room3":6,
            }

# roomを一括で作成
    for key, value in rooms.items():
        chat_room_create(key, value)
    
    # ChatRoomの作成のテスト
    assert chat_rooms["room1"].title == "room1"
    assert chat_rooms["room1"].max_member == 5

    # ChatClientのテスト
    chat_client = ChatClient("adam", "0.0.0.0", "8080")
    chat_rooms["room1"].enter_chat_room(chat_client)
    assert chat_rooms["room1"].client_list["adam"] == chat_client

def test_new_chat_client():
    clients = []

    clients.append(ChatClient("taro1", "192.168.0.0", "12345"))
    clients.append(ChatClient("taro2", "192.168.0.1", "12346"))
    clients.append(ChatClient("taro3", "192.168.0.2", "12347"))
    clients.append(ChatClient("jugemujugemugokounosurikire", "192.168.0.2", "12347"))
    # test_print_chat_client(clients)
    
    return clients

def test_print_chat_client(clients: ChatClient):
    for c in clients:
        print(c.name)
        print(c.address)
        print(c.port)
    return 

def intaractive_create_chat_room():
    # title
    while True:
        title = input("Enter new chat room name!: ")
        # validation
        if (not title in chat_rooms): break
        print("It has already been registered.")
        
    # max_member
    while True:
        max_member = input("What is the maximum number of people in a chat room?: ")
        # validation
        if (max_member.isdigit()): break
        print("Please enter a number.")

    """
    test case
    """
    cr = chat_room_create(title, max_member)
    test_print_chat_room(cr)
    return 

def test_print_chat_room(chatroom: ChatRoom):
    """ 
        test用print出力
    """ 
    cr = chatroom 
    print(cr.title)
    print(cr.max_member)

def format_chat_message(clients: list[ChatClient]) -> int:
    """
        新しいクライアントがnewされた時に実行する
        チャットメッセージの名前の最大文字数から、メッセージとの適切な感覚を調整
    """
    space = 3
    max = 0
    for client in clients:
        if len(client.name) >= max: max = len(client.name)
    return max + space


def chat_message(name: str, message: str, name_ljust: int) -> str:
    """
        chat messageをprintする
    """
    print(name.ljust(name_ljust) + ":" + message)
    return 

def test_chat_message():
    clients = test_new_chat_client()
    ljust_max = format_chat_message(clients)
    chat_message(clients[0].name, "test message!", ljust_max)
    chat_message(clients[1].name, "Hello, World!", ljust_max)
    chat_message(clients[2].name, "Hello", ljust_max)
    chat_message(clients[3].name, "Hello", ljust_max)

if __name__ == "__main__":
    #prologue()

    #test()
    # test_new_chat_client()
    # intaractive_create_chat_room()
    # start_client()
    # start_server()

    # test_chat_message()
    
    
    pass
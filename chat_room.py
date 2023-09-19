from lib.udp_server import * 

# チャットルームの辞書配列
chat_rooms= {}

# メッセージフォーマット用のspace
MESSAGE_SPACE = 3

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
            socket:      通信用socket
            address:     アドレス
            port:        ポート番号

            client_list: 入室しているクライアント情報
            ljust_max:   チャットメッセージの文字列整形管理用
    """
    # client HashMap
    client_list = {}
    # チャットメッセージ文字列整形用
    ljust_max = 0
    
    def __init__(self, title: str, max_member: int):
        # validationがいる
        self.title: str = title
        self.max_member: int = max_member
        self.room_socket_create()

    def __del__(self):
        """
            デストラクター
            pythonプログラム終了時に動作
        """
        self.sock.close()

    def room_socket_create(self):
        """
            chatroomのサーバーを作成する
        """
        self.sock, self.address, self.port = startup_udp_server()

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
        self.generate_message_format(chat_client.name)
        self.client_list[chat_client.name] = chat_client
    
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
    chat_rooms = []

    # __new__を書き換えてsingletonに
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ChatRooms, cls).__new__(cls)
            cls._instance.initialize()
        return cls._instance

    # 初期化処理
    def initialize(self):
        pass

    def append_room(self, room: ChatRoom):
        """
            chatroomを登録する
        """
        self.chat_rooms.append(room)
        
    def remove_room(self, room: ChatRoom):
        """
            指定されたchatroomの登録を削除する
        """
        self.chat_rooms.remove(room)

def chat_room_create(room_name: str, max_member: int):
    """
        chat_roomを作成し、辞書に登録する
    """
    chat_room = ChatRoom(room_name, max_member)

    # チャットルーム辞書にチャットルームを追加
    chat_rooms[room_name] = chat_room
    return chat_room


# ---- test code ----

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
    assert "room1" ,room.title
    room_list.append_room(room) 
    assert "room1", room_list.chat_rooms[0].title

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
    print("room:", room, "name:", room.title)
    
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
    print("room name:", room.title, "room member:",[ x for x in room.client_list] )

    # client exit room
    room.exit_client(cl1)
    print("room name:", room.title, "room member:", [ x for x in room.client_list] )
    room.exit_client(cl2)
    print(room.ljust_max)
    print("room name:", room.title, "room member:", [ x for x in room.client_list] )
    room.exit_client(cl3)
    print(room.ljust_max)
    print("room name:", room.title, "room member:", [ x for x in room.client_list] )
    room.exit_client(cl4)
    print(room.ljust_max)
    print("room name:", room.title, "room member:", [ x for x in room.client_list] )
    room.exit_client(cl5)
    print(room.ljust_max)
    print("room name:", room.title, "room member:", [ x for x in room.client_list] )
    
if __name__ == "__main__":

    # test_singleton_class()
    
    # test_chatrooms_remove()

    pass

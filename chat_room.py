from lib.udp_server import * 

# チャットルームの辞書配列
chat_rooms= {}

# メッセージフォーマット用のspace
SPACE = 3

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

class ChatRooms:
    chat_rooms = []
    def __init__(self):
        pass

# todo: 次回、この辺りから
        


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
        new_ljust_max = SPACE + len(client_name)
        if new_ljust_max >= self.ljust_max: self.ljust_max = new_ljust_max
        # for client in clients:
        #     if len(client.name) >= max: max = len(client.name)
    def regenerate_message_format(self) -> int:
        """
            新しいクライアントがnewされた時に実行する
            チャットメッセージの名前の最大文字数から、メッセージとの適切な感覚を調整
        """
        max = 0
        for client_name in self.client_list:
            if len(client_name) >= max: max = len(client_name)
        self.ljust_max = max + SPACE

def chat_room_create(room_name: str, max_member: int):
    """
        chat_roomを作成し、辞書に登録する
    """
    chat_room = ChatRoom(room_name, max_member)

    # チャットルーム辞書にチャットルームを追加
    chat_rooms[room_name] = chat_room
    return chat_room


if __name__ == "__main__":
    # cr = create_new_chat_room()
    # print("cr:", cr, " cr.name:", cr.title, " cr.maximum:", cr.max_member)
    # cr = create_information_new_chat_room()
    # print(cr)

    cl1 = ChatClient("taro", "address", 9001)
    print("client:", cl1, "name:", cl1.name)

    room = ChatRoom("room1", 5)
    print("room:", room, "name:", room.title)
    
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
    

    pass
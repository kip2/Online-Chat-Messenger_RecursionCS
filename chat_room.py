from lib.udp_server import * 

# チャットルームの辞書配列
chat_rooms= {}

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

    def room_socket_create(self):
        """
            chatroomのサーバーを作成する
        """
        self.sock, self.address, self.port = startup_udp_server()
        pass

def chat_room_create(room_name: str, max_member: int):
    """
        chat_roomを作成し、辞書に登録する
    """
    chat_room = ChatRoom(room_name, max_member)

    # チャットルーム辞書にチャットルームを追加
    chat_rooms[room_name] = chat_room
    return chat_room

# def create_new_chat_room():
#     """
#         新しいチャットルームを作成する関数
#     """
#     while True:
#         room_name = input("Room Name? > ")
#         if not room_name == ""  and not room_name.isspace(): break
        
#     while True:
#         max_member = input("maximum number? > ")
#         if max_member.isdecimal(): break
#     chat_room = chat_room_create(room_name, max_member)
#     return chat_room

if __name__ == "__main__":
    # cr = create_new_chat_room()
    # print("cr:", cr, " cr.name:", cr.title, " cr.maximum:", cr.max_member)
    # cr = create_information_new_chat_room()
    # print(cr)
    pass
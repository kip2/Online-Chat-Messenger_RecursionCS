
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
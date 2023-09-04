import sys

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
        self.name = name
        self.address = address
        self.port = port

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
    client_list = {}
    
    def __init__(self, title: str, max_member: int):
        self.title = title
        self.max_member = max_member
        #self.room_server_create()

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
    
def prologue():
    print("Welcome Online chat Messenger!")
    print("Make your chat room!")

    # 最初なので、ルームを作成
    chat_room = create_new_chat_room()
    return 

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

if __name__ == "__main__":
    #prologue()

    test()



    
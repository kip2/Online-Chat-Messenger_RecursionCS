import sys

# チャットルームの辞書配列
chat_rooms_dict= {}

class ChatClient:
    """
        field:
            name:       クライアントのユーザーネーム
            address:    クライアントのアドレス
            port:       クライアントのポート番号
    """
    def __init__(self, name, address, port):
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
    def __init__(self, title, max_member):
        self.title = title
        self.max_member = max_member
        #self.room_server_create()

    def room_server_create():
        """
            chatroomのサーバーを作成する
        """
        pass

def chat_room_create(room_name, max_member):
    """
        chat_roomを作成し、辞書に登録する
    """
    chat_room = ChatRoom(room_name, max_member)

    # チャットルーム辞書にチャットルームを追加
    chat_rooms_dict[room_name] = chat_room
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

if __name__ == "__main__":
    prologue()
    print(chat_rooms_dict)

    
import sys
import ndjson
from  lib.tcp_server import *
from  lib.udp_server import *
from lib.chat_room import *

import lib

# network socket type
NETWORK_SOCKET_TYPE = lib._address_config.NETWORK_SOCKET_TYPE 
# server address
SERVER_ADDRESS = lib._address_config.SERVER_ADDRESS 
# server port
SERVER_PORT = lib._address_config.SERVER_PORT

# chat room list
chat_rooms = ChatRooms()

def header_parsing(header):
    """
        headerを解析する
    """
    client_request = int.from_bytes(header[:1], "big")
    message_length = int.from_bytes(header[1:3], "big")
    data_length = int.from_bytes(header[4:8], "big")
    return (client_request, message_length, data_length)

# def broadcast_client(sock, addr):
#     while True:
#         try:
#             data = sock.recv(4096)
#             if data == b"":
#                 break
#             print("$ say client:{}".format(addr))
#             # 受信データを全クライアントに送信
#             for client in clients:
#                 client[0].send(data)

#         except ConnectionResetError:
#             break
#         except OSError as e:
#             if e.errno == 57:
#                 break
#     # クライアントリストから削除
#     clients.remove((sock,addr))
#     print("- close client:{}".format(addr))

#     sock.shutdown(socket.SHUT_WR)
#     sock.close()

def test_room_create():
    cr = ChatRoom("room1", 1)
    chat_rooms.append_room(cr)
    cr = ChatRoom("room2", 2)
    chat_rooms.append_room(cr)
    cr = ChatRoom("room3", 3)
    chat_rooms.append_room(cr)
    cr = ChatRoom("room4", 4)
    chat_rooms.append_room(cr)
    cr = ChatRoom("room5", 5)
    chat_rooms.append_room(cr)
    return 

def chatroom_server():
    print("Starting up udp on {} port {}".format(SERVER_ADDRESS, SERVER_PORT))

    sock, addr, port = startup_udp_server(SERVER_ADDRESS, SERVER_PORT)
    print(f"socket = {sock}, address = {addr}, port = {port}")

    # roomの作成
    name = "room1"
    max_member = 5
    room = ChatRoom(name, max_member)
    chat_rooms.append_room(room)
    mock_rooms()
    l = chat_rooms.get_room_list()

    try:
        while True:
            try:
                data, client_address = sock.recvfrom(4096)
                print("connection from", client_address)

                # messageのデコード
                data = decode_message(data)

                a,p  = client_address

                # 入室処理のメッセージをparseする
                parsed_message = message_parsing(data)
                # todo: messageに:が入らないことはclient側で保証すること
                # もしparseしたメッセージが2つなら入室メッセージ
                if (len(parsed_message) == 2):
                    room_name, client_name = parsed_message
                    # roomの存在をチェック
                    if not chat_rooms.has_chat_room(room_name):
                        err_message = "そのようなroomは存在しません"
                        send_error_message(sock, client_address,err_message)
                        continue

                    # roomを取得する
                    room = chat_rooms.get_room(room_name)

                    # clientをインスタンス化
                    client = ChatClient(client_name, a, p)
                    
                    # すでに入室しているなら
                    if room.has_chat_client(client):
                        message = "すでに入室しています"
                        send_error_message(sock, client_address,err_message)
                        continue

                    # clientを入室させる
                    room.enter_chat_room(client)

                # もしparseしたメッセージが3つならチャットへのメッセージ
                elif(len(parsed_message) == 3):
                    # unpack message
                    room_name, client_name, message = parsed_message

                    # ルームが存在しない
                    if not chat_rooms.has_chat_room(room_name):
                        err_message = "そのようなroomは存在しません"
                        send_error_message(sock, client_address,err_message)
                        continue

                    # roomを取得する
                    room = chat_rooms.get_room(room_name)

                    client = ChatClient(client_name, a, p)

                    # clientがroomに存在すればbroadcast
                    if room.has_chat_client(client):
                        message = "test broadcast"
                        room.udp_message_broadcast(sock, client_name, message)
                    else:
                        # todo: testまだ
                        err_message = "入室していません"
                        send_error_message(sock, client_address,  err_message)
                        continue

            except Exception as e:
                print("Error: " + str(e))
                break
    except KeyboardInterrupt:
        pass
    finally:
        print("Closing current connection")
        server_exit(sock)

def server_exit(sock):
    sock.close()
    sys.exit(0)
    
def message_parsing(message):
    message = message.split(":")
    if (len(message) == 2):
        return (message[0], message[1])
    elif (len(message) == 3):
        return (message[0], message[1], message[2])

def mock_rooms():
    room = ChatRoom("mock_room1", 5)
    chat_rooms.append_room(room)
    room = ChatRoom("mock_room2", 5)
    chat_rooms.append_room(room)
    room = ChatRoom("mock_room3", 5)
    chat_rooms.append_room(room)
    room = ChatRoom("mock_room4", 5)
    chat_rooms.append_room(room)
    room = ChatRoom("mock_room5", 5)
    chat_rooms.append_room(room)


def mock_member(room: ChatRoom):
    room.enter_chat_room(ChatClient("mock太郎"+str(10000), '127.0.0.1', 10000))
    room.enter_chat_room(ChatClient("mock太郎"+str(10001), '127.0.0.1', 10001))
    room.enter_chat_room(ChatClient("mock太郎"+str(10002), '127.0.0.1', 10002))
    room.enter_chat_room(ChatClient("mock太郎"+str(10003), '127.0.0.1', 10003))
    room.enter_chat_room(ChatClient("mock太郎"+str(10004), '127.0.0.1', 10004))
    return 

def test_conver_json_data():
    mock_rooms()
    d = chat_rooms.convert_json_data()
    print(d)

    
def test_rooms_append_room():
    mock_rooms()

def test_has_chat_room():
    mock_rooms()
    print(chat_rooms.has_chat_room("mock_room1"))
    print(chat_rooms.has_chat_room("mock_room6"))
    
def test_message_parsing():
    message = "room1" + ":" + "mocck_client1"
    message = message_parsing(message)
    print(message)
    a, b = message
    print(a, b)
    
if __name__ == "__main__":

    # test_message_parsing()
    # test_has_chat_room()
    # test_rooms_append_room()
    # broadcast_chatroom()
    # chatroom_server()
    test_conver_json_data()

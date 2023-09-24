import socket
import os
import threading
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

# client list
clients = []
# todo: clientsの扱いをどうするか。キューで管理するのかどうか

# chat room list
chat_rooms = ChatRooms()

def create_room():
    client_socket = clients[0][0]

    # 部屋の名前と人数を聞く
    
    
    # 帰ってきた情報を受けて、roomを作成し、roomリストに追加する
        # roomリストに追加
        # 

    # そちらで更新するように、headerに情報を加えて渡す
        # header情報を変えるか？
        # client側のheader解析情報が入りそう

    client_socket.send(b"CREATE ROOM!\n")
    client_socket.send(b"NEXT MESSAGE!")

    # connection.close()
    pass

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

def send_room_list():
    clients[0][0].send(b"ROOM LIST!!!")
    """
        roomlistのJSONファイルのやりとりがいる
        JSONファイルやりとり用のソケット通信を開いて、そこで通信をしたい
        JSONファイルをやりとりするためのサーバーを立てて、そこでやりとりするように誘導する
        つまり、
        - serverでserverを立てる
        - clientでそこに接続する
            client側で、TCPであるかUDPであるかを識別するためのヘッダーbitがいる
    """
    
def send_log_file():
    clients[0][0].send(b"LOG FILE!!!")

def allow_enter():
    clients[0][0].send(b"ENTER ROOM!!!")

def receive_message():
    clients[0][0].send(b"RECEIVED MESSAGE!!!")

def send_client_exit_message():
    clients[0][0].send(b"exitOK")

# def send_exit_message():
#     clients[0][0].send(b"BYE!!!")
def send_exit_message():
    clients[0][0].send(b"BYE!!!")


# todo: まだ
def startup_chat_room(room_name: str, room_maximum_people: int):

    with ChatRoom(room_name, room_maximum_people) as room:
        sock, addr, port = room.unpack()
        while True:
            try:
                data, client_address = sock.recvfrom(8)
                print("connection from", client_address)
                # headerの読み取り
                client_request, message_length, data_length = header_parsing(data)
                print('Received header from client. Byte lengths: Client request {}, message length {}, Data Length {}'.format(client_request,message_length,data_length))

                # もし人数が一人もいないなら、部屋を削除する
                if room.is_empty():
                    break
                pass
            except Exception as e:
                break
            finally:
                if room.is_empty():
                    room.finalize()
                    break

    pass

def receive_udp_request_message():
    print("Starting up udp on {} port {}".format(SERVER_ADDRESS, SERVER_PORT))

    sock, addr, port = startup_udp_server(SERVER_ADDRESS, SERVER_PORT)
    print(f"socket = {sock}, address = {addr}, port = {port}")

    # room作成用メソッド
    test_room_create()

    
    try:
        while True:
            try:
                data, client_address = sock.recvfrom(4096)
                print("connection from", client_address)
                # client_request, message_length, data_length = header_parsing(data)
                # print('Received header from client. Byte lengths: Client request {}, message length {}, Data Length {}'.format(client_request,message_length,data_length))
                room_name = mes_decode(data)
                print(chat_rooms.get_room(room_name))
            except Exception as e:
                break
    finally:
        sock.close()


chat_clients = []
def chat_room():
    print("Starting up CHAT ROOM on {} port {}".format(SERVER_ADDRESS, SERVER_PORT))

    # 部屋の作成 
    # todo: 部屋の作成を別に切り出す必要がある
    room_name = "test_room"
    max_member = 5
    room = ChatRoom(room_name, max_member)

    with UDP_Server() as server:
        sock, addr, port = server.unpack()
        print(f"socket = {sock}, address = {addr}, port = {port}")

        while True:
            try:
                data, client_address = sock.recvfrom(4096)
                print("connection from", client_address)

                # headerの読み取り
                client_request, message_length, data_length = header_parsing(data)

                print('Received header from client. Byte lengths: Client request {}, message length {}, Data Length {}'.format(client_request,message_length,data_length))

                # todo: dataがまだheaderになっている
                # todo: chatroom用のheaderを受け取る
                # todo: 本来、入室した時点で作成し、それを使い回す必要がある
                # todo: 入室したクライアントが既存の誰かを把握する必要がある
                cl = ChatClient("testclient:"+str(client_address[1]), client_address[0], client_address[1])
                print("client_name:", cl.name)

                # なければクライアントに追加
                if client_address not in chat_clients:
                    chat_clients.append(client_address)

                # headerの種類によって動作を変える
                if client_request == lib._header.SEND_MESSAGE:
                    print("Received message!")
                    message = sock.recv(4096)
                    udp_message_broadcast(sock, message)
                elif client_request == lib._header.CLIENT_EXIT_MESSAGE:
                    client_room_exit(client_address)
                elif client_request == lib._header.EXIT_MESSAGE:
                    break

            except KeyboardInterrupt:
                # server側からは、Ctrl + C で終了
                print("Closing current connection")
                break
            except Exception as e:
                print("Error: " + str(e))
                break

def udp_message_broadcast(sock, message):
    """
        roomのclientへのブロードキャスト
    """
    for client_address in chat_clients:
        send_udp_message(sock, client_address, message)

# todo メインサーバからの退室処理が不完全
def client_exit_main_server(sock, addr):
    """
        clientをメインサーバから退室させる
    """
    clients.remove((sock,addr))
    print("- close client:{}".format(addr))
    print(sock)

#------------------------------------------------------------------------------------------------

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

def main_udp():
    print("Starting up udp on {} port {}".format(SERVER_ADDRESS, SERVER_PORT))

    sock, addr, port = startup_udp_server(SERVER_ADDRESS, SERVER_PORT)
    print(f"socket = {sock}, address = {addr}, port = {port}")

    # room作成用メソッド
    # test_room_create()
    
    # recv_size = 4096
    # thread = threading.Thread(target=receive_udp_request_message, args=(sock, recv_size))
    # thread.start()

    try:
        while True:
            try:
                data, client_address = sock.recvfrom(4096)
                print("connection from", client_address)

                client_request, message_length, data_length = header_parsing(data)

                print('Received header from client. Byte lengths: Client request {}, message length {}, Data Length {}'.format(client_request,message_length,data_length))

                # headerの種類によって動作を変える
                if client_request == lib._header.CREATE_ROOM:
                    sock.sendto(data, client_address)
                elif client_request == lib._header.REQUEST_ROOM_LIST:
                    sock.sendto(data, client_address)
                elif client_request == lib._header.REQUEST_LOG_FILE:
                    sock.sendto(data, client_address)
                elif client_request == lib._header.ENTER_ROOM:
                    sock.sendto(data, client_address)
                elif client_request == lib._header.SEND_MESSAGE:
                    sock.sendto(data, client_address)
                elif client_request == lib._header.CLIENT_EXIT_MESSAGE:
                    sock.sendto(data, client_address)
                elif client_request == lib._header.EXIT_MESSAGE:
                    sock.sendto(data, client_address)
                    break
            except Exception as e:
                print("Error: " + str(e))
                break
    except KeyboardInterrupt:
        pass
    finally:
        print("Closing current connection")
        sock.close()

# -------- test code ---------
def test_chat_room():

    with UDP_Server() as serv:
        sock = serv.sock

        data, client_address = sock.recvfrom(4096)
        data = b"Welcome to chatroom!"
        sock.sendto(data, client_address)
        data = b"Enter your message!"
        sock.sendto(data, client_address)
        print("End!")

def test_mes_udp():
    with UDP_Server() as serv:
        sock = serv.sock

        data, client_address = sock.recvfrom(4096)

# ---------------------------
def main_tcp():

    print("Starting up tcp on {} port {}".format(SERVER_ADDRESS, SERVER_PORT))

    sock, addr, port = startup_tcp_server(SERVER_ADDRESS, SERVER_PORT)
    print(f"socket = {sock}, address = {addr}, port = {port}")

    try:
        while True:
            try:
                connection, client_address = sock.accept()
                clients.append((connection, client_address))
                print("connection from", client_address)
                while True:
                    data = connection.recv(8)
                    # # headerからの抽出
                    # client_request = int.from_bytes(header[:1], "big")
                    # message_length = int.from_bytes(header[1:3], "big")
                    # data_length = int.from_bytes(header[4:8], "big")

                    # headerの読み取り(header4バイト)
                    # clientが何を求めているかを受け取る
                    client_request, message_length, data_length = header_parsing(data)

                    print('Received header from client. Byte lengths: Client request {}, message length {}, Data Length {}'.format(client_request,message_length,data_length))

                    # headerの種類によって動作を変える
                    if client_request == lib._header.CREATE_ROOM:
                        create_room()
                    elif client_request == lib._header.REQUEST_ROOM_LIST:
                        send_room_list()
                    elif client_request == lib._header.REQUEST_LOG_FILE:
                        send_log_file()
                    elif client_request == lib._header.ENTER_ROOM:
                        allow_enter()
                    elif client_request == lib._header.SEND_MESSAGE:
                        receive_message()
                    elif client_request == lib._header.CLIENT_EXIT_MESSAGE:
                        send_client_exit_message()
                    elif client_request == lib._header.EXIT_MESSAGE:
                        send_exit_message()
                        break
            except Exception as e:
                print("Error: " + str(e))
                break
    except KeyboardInterrupt:
        pass
    finally:
        print("Closing current connection")
        sock.close()

def broadcast_chatroom():
    print("Starting up udp on {} port {}".format(SERVER_ADDRESS, SERVER_PORT))

    sock, addr, port = startup_udp_server(SERVER_ADDRESS, SERVER_PORT)
    print(f"socket = {sock}, address = {addr}, port = {port}")

    # roomの作成
    name = "room1"
    max_member = 5
    room = ChatRoom(name, max_member)
    chat_rooms.append_room(room)

    try:
        while True:
            try:
                data, client_address = sock.recvfrom(4096)
                print("connection from", client_address)

                # messageのデコード
                data = decode_message(data)

                # client_request, message_length, data_length = header_parsing(data)

                # print('Received header from client. Byte lengths: Client request {}, message length {}, Data Length {}'.format(client_request,message_length,data_length))

                # mock_member(room)

                a,p  = client_address
                n = "test太郎" + str(p)

                # enterできないならそのメッセージを元のクライアントに返す
                if not room.enter_chat_room(ChatClient(n, a, p)):
                    err_message = "入室できませんでした"
                    send_udp_message(sock, client_address,  err_message)
                    continue
                
                room_name, client_name = message_parsing(data)

                if not chat_rooms.has_chat_room(room_name):
                    err_message = "そのようなroomは存在しません"
                    send_error_message(sock, client_address,err_message)
                    continue

                # mes = "test message @ " + str(p)
                # room.udp_message_broadcast(sock, n, mes)

                # # # headerの種類によって動作を変える
                # if client_request == lib._header.CREATE_ROOM:
                #     sock.sendto(data, client_address)
                # elif client_request == lib._header.REQUEST_ROOM_LIST:
                #     sock.sendto(data, client_address)
                # elif client_request == lib._header.REQUEST_LOG_FILE:
                #     sock.sendto(data, client_address)
                # elif client_request == lib._header.ENTER_ROOM:
                #     sock.sendto(data, client_address)
                # elif client_request == lib._header.SEND_MESSAGE:
                #     sock.sendto(data, client_address)
                # elif client_request == lib._header.CLIENT_EXIT_MESSAGE:
                #     sock.sendto(data, client_address)
                # elif client_request == lib._header.EXIT_MESSAGE:
                #     sock.sendto(data, client_address)
                #     break
            except Exception as e:
                print("Error: " + str(e))
                break
    except KeyboardInterrupt:
        pass
    finally:
        print("Closing current connection")
        sock.close()

def send_error_message(sock, client_address:tuple, message:str):
    message = encode_message(message)
    send_udp_message(sock, client_address, message)
    
def message_parsing(message):
    message = message.split(":")
    return (message[0], message[1])

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
    broadcast_chatroom()

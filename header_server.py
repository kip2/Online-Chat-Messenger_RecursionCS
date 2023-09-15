import socket
import os
from port_scan import *
import threading
import ndjson

# const request
# header用定数
CREATE_ROOM = 0
REQUEST_ROOM_LIST = 1
REQUEST_LOG_FILE = 2
ENTER_ROOM = 3
SEND_MESSAGE = 4
EXIT_MESSAGE = 5

# network socket type
NETWORK_SOCKET_TYPE = socket.AF_INET

# client list
clients = []

sock = socket.socket(NETWORK_SOCKET_TYPE, socket.SOCK_STREAM)
SERVER_ADDRESS = "127.0.0.1"
SERVER_PORT = 9001

# # UDP通信Descriptor用ファイル名のprefix
# UDP_FILE_DIRECTORY = "/udp/"

def startup_tcp_server(server_address:str = SERVER_ADDRESS, server_port:str = None) -> tuple:
    """
        TCPサーバーを立てる関数
        connect用のsocketと、(IP_address, PORT)のタプルを返す
    """

    # portが指定されていなければ自動で生成
    if server_port == None: 
        server_port = available_port(server_address)

    try:
        sock = socket.socket(NETWORK_SOCKET_TYPE, socket.SOCK_STREAM) 
        sock.bind((server_address, server_port))
        sock.listen(1)
        return (sock, server_address, server_port)
    except (socket.timeout, ConnectionRefusedError):
        return

def startup_udp_server(server_address:str = SERVER_ADDRESS, server_port:str = None) -> tuple:
    """
        UDPサーバーを立てる関数
        connect用のsocketと、(IP_address, PORT)のタプルを返す
    """

    # portが指定されていなければ自動で生成
    if server_port == None:
        server_port = available_port(server_address)

    try:
        sock = socket.socket(NETWORK_SOCKET_TYPE, socket.SOCK_DGRAM) 
        sock.bind((server_address, server_port))
        return (sock, server_address, server_port)
    except (socket.timeout, ConnectionRefusedError):
        return

# def startup_udp_room_server(room_name:str):
#     """
#         UDPによるRoomサーバーを立てる関数
#         connect用socketと、(IP_address, PORT)のタプルを返す
#     """

#     sock = socket.socket(NETWORK_SOCKET_TYPE, socket.SOCK_DGRAM)
#     server_address = create_udp_descriptor_name(room_name)
#     # try:
#     #     os.unlink(server_address)
#     # except FileNotFoundError:
#     #     pass
#     sock.bind(server_address)
#     return (sock, server_address) 

# def create_udp_descriptor_name(room_name:str) -> str:
#     """
#         udp通信待ち受け用descriptorの名前を作る
#     """
#     return UDP_FILE_DIRECTORY + "udp_"+room_name+"_file"

def create_room():
    clients[0][0].send(b"CREATE ROOM!")

def broadcast_client(sock, addr):
    # todo : まだ　clientへのbroadcat関数
    while True:
        try:
            data = sock.recv(4096)
            if data == b"":
                break
            print("$ say client:{}".format(addr))
            # 受信データを全クライアントに送信
            for client in clients:
                client[0].send(data)

        except ConnectionResetError:
            break
        except OSError as e:
            if e.errno == 57:
                break
    # クライアントリストから削除
    clients.remove((sock,addr))
    print("- close client:{}".format(addr))

    sock.shutdown(socket.SHUT_WR)
    sock.close()

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

def send_exit_message():
    clients[0][0].send(b"BYE!!!")

def start_server():

    print("Starting up on {} port {}".format(SERVER_ADDRESS, SERVER_PORT))

    sock.bind((SERVER_ADDRESS, SERVER_PORT))
    sock.listen(5)

    try:
        while True:
            try:
                connection, client_address = sock.accept()
                clients.append((connection, client_address))
                print("connection from", client_address)
                # headerの読み取り
                # header4バイト
                # clientが何を求めているかを受け取る
                header = connection.recv(8)
                # headerからの抽出
                client_request = int.from_bytes(header[:1], "big")
                message_length = int.from_bytes(header[1:3], "big")
                data_length = int.from_bytes(header[4:8], "big")

                print('Received header from client. Byte lengths: Client request {}, message length {}, Data Length {}'.format(client_request,message_length,data_length))

                # headerの種類によって動作を変える
                if client_request == CREATE_ROOM:
                    create_room()
                elif client_request == REQUEST_ROOM_LIST:
                    send_room_list()
                elif client_request == REQUEST_LOG_FILE:
                    send_log_file()
                elif client_request == ENTER_ROOM:
                    allow_enter()
                elif client_request == SEND_MESSAGE:
                    receive_message()
                elif client_request == EXIT_MESSAGE:
                    send_exit_message()
            except Exception as e:
                print("Error: " + str(e))
                break
            # todo 勝手にfinallyに入ってconnectを抜けている
            # finally:
            #     print("Closing current connection")
            #     connection.close()
                # break
    finally:
        print("Closing current connection")
        connection.close()

if __name__ == "__main__":
    # start_server()
    # sock, address, port = startup_tcp_server()
    sock, address, port = startup_udp_server()
    print(sock, address, port)
    sock.close()
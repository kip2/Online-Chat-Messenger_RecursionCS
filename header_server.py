import socket
import os
from port_scan import *
import threading
import ndjson

# 定数読み込み用
import _header
import _address_config

# network socket type
NETWORK_SOCKET_TYPE = _address_config.NETWORK_SOCKET_TYPE 

# server address
SERVER_ADDRESS = _address_config.SERVER_ADDRESS 
# server port
SERVER_PORT = _address_config.SERVER_PORT

# client list
clients = []


def startup_tcp_server(server_address:str = SERVER_ADDRESS, server_port:int = None) -> tuple:
    """
        TCPサーバーを立てる関数
        connect用のsocketと、(IP_address, PORT)のタプルを返す
    """
    # portが指定されていなければ自動で生成
    if server_port == None: 
        server_port = available_tcp_port(server_address)

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
        server_port = available_udp_port(server_address)

    try:
        sock = socket.socket(NETWORK_SOCKET_TYPE, socket.SOCK_DGRAM) 
        sock.bind((server_address, server_port))
        return (sock, server_address, server_port)
    except (socket.timeout, ConnectionRefusedError):
        return

def create_room():
    clients[0][0].send(b"CREATE ROOM!\n")
    clients[0][0].send(b"NEXT MESSAGE!")
    # connection.close()
    pass
    # todo clientsの数字指定をもうちょっとわかりやすくしたい

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

def send_client_exit_message():
    clients[0][0].send(b"BYE client!!!")

def send_exit_message():
    clients[0][0].send(b"BYE!!!")

def main_tcp():

    print("Starting up tcp on {} port {}".format(SERVER_ADDRESS, SERVER_PORT))

    sock, addr, port = startup_tcp_server(SERVER_ADDRESS, SERVER_PORT)
    print(f"socket = {sock}, address = {addr}, port = {port}")

    try:
        while True:
            try:
                print("ここから!")
                connection, client_address = sock.accept()
                clients.append((connection, client_address))
                print("connection from", client_address)
                # headerの読み取り
                # header4バイト
                # clientが何を求めているかを受け取る
                print("leached!")
                header = connection.recv(8)
                # headerからの抽出
                client_request = int.from_bytes(header[:1], "big")
                message_length = int.from_bytes(header[1:3], "big")
                data_length = int.from_bytes(header[4:8], "big")

                print('Received header from client. Byte lengths: Client request {}, message length {}, Data Length {}'.format(client_request,message_length,data_length))

                # headerの種類によって動作を変える
                if client_request == _header.CREATE_ROOM:
                    create_room()
                elif client_request == _header.REQUEST_ROOM_LIST:
                    send_room_list()
                elif client_request == _header.REQUEST_LOG_FILE:
                    send_log_file()
                elif client_request == _header.ENTER_ROOM:
                    allow_enter()
                elif client_request == _header.SEND_MESSAGE:
                    receive_message()
                elif client_request == _header.CLIENT_EXIT_MESSAGE:
                    send_client_exit_message()
                elif client_request == _header.EXIT_MESSAGE:
                    send_exit_message()
                    break
            except Exception as e:
                print("Error: " + str(e))
                break
            # finally:
            #     connection.close()
    finally:
        print("Closing current connection")
        sock.close()

def main_udp():

    print("Starting up udp on {} port {}".format(SERVER_ADDRESS, SERVER_PORT))

    sock, addr, port = startup_udp_server(SERVER_ADDRESS, SERVER_PORT)
    print(f"socket = {sock}, address = {addr}, port = {port}")

    try:
        while True:
            try:
                data, client_address = sock.recvfrom(4096)
                print("connection from", client_address)
                # headerの読み取り
                # header4バイト
                # clientが何を求めているかを受け取る
                header = data
                # headerからの抽出
                client_request = int.from_bytes(header[:1], "big")
                message_length = int.from_bytes(header[1:3], "big")
                data_length = int.from_bytes(header[4:8], "big")

                print('Received header from client. Byte lengths: Client request {}, message length {}, Data Length {}'.format(client_request,message_length,data_length))

                # headerの種類によって動作を変える
                if client_request == _header.CREATE_ROOM:
                    # create_room()
                    sock.sendto(data, client_address)
                elif client_request == _header.REQUEST_ROOM_LIST:
                    send_room_list()
                elif client_request == _header.REQUEST_LOG_FILE:
                    send_log_file()
                elif client_request == _header.ENTER_ROOM:
                    allow_enter()
                elif client_request == _header.SEND_MESSAGE:
                    sock.sendto(data, client_address)
                    # receive_message()
                elif client_request == _header.CLIENT_EXIT_MESSAGE:
                    send_client_exit_message()
                elif client_request == _header.EXIT_MESSAGE:
                    sock.sendto(data, client_address)
                    # send_exit_message()
                    break
            except Exception as e:
                print("Error: " + str(e))
                break
    finally:
        print("Closing current connection")
        sock.close()

if __name__ == "__main__":

    main_tcp()
    
    # main_udp()
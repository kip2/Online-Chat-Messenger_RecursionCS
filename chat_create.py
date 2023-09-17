import socket
import sys
import threading
from port_scan import *
from _header import *

# 定数読み込み用
import _header
import _address_config

# network socket type
NETWORK_SOCKET_TYPE = _address_config.NETWORK_SOCKET_TYPE

# server address & port
SERVER_ADDRESS = _address_config.SERVER_ADDRESS 
SERVER_PORT = _address_config.SERVER_PORT

# client address & port
CLIENT_ADDRESS = _address_config.CLIENT_ADDRESS


# def create_exit_header():
#     return _header.EXIT_MESSAGE.to_bytes(1,"big") + int(0).to_bytes(3,"big") + int(0).to_bytes(4,"big")

def send_tcp_message(sock, header_message):
    """
        TCPクライアントからメッセージを送信する
    """
    header = create_header(header_message, 0, 0)
    sock.send(header)

def send_udp_message(sock, SERVER_ADDRESS, SERVER_PORT, header_message):
    """
        UDPクライアントからメッセージを送信する
    """
    header = create_header(header_message, 0, 0)
    sock.sendto(header, (SERVER_ADDRESS, SERVER_PORT))

def startup_udp_client(client_address:str = CLIENT_ADDRESS ,client_port:str = None) -> tuple:
    """
        UDPクライエントを起動する関数
        connect用のsocketと、(IP_address, PORT)のタプルを返す
    """
    # portが指定されていなければ自動で生成
    if client_port == None:
        client_port = available_udp_port(client_address)

    try:
        sock = socket.socket(NETWORK_SOCKET_TYPE, socket.SOCK_DGRAM) 
        sock.bind((client_address, client_port))
        return (sock, client_address, client_port)
    except (socket.timeout, ConnectionRefusedError):
        return

# データ受信関数
def recv_data(sock, recv_size):
    try:
        while True:
            try:
                data = sock.recv(recv_size)
                if data == b"":
                    break
                print(data.decode("utf-8"))
            except ConnectionResetError:
                break
            except OSError as e:
                if e.errno == 9:
                    break
            except Exception as e:
                print("Error: ", + str(e))
                break
    finally:
        print("shutdown helper.")
        sock.close()

def startup_tcp_client(server_address:str, server_port: int) -> tuple:
    """
        TCPクライエントを起動する関数
        connect用のsocketと、(IP_address, PORT)のタプルを返す
        server側のアドレスを使う点に注意する
    """
    try:
        sock = socket.socket(NETWORK_SOCKET_TYPE, socket.SOCK_STREAM) 
        sock.connect((server_address, server_port))
        return (sock, server_address, server_port)
    except (socket.timeout, ConnectionRefusedError):
        return
    except socket.error as e:
        print(e)
        return 

def main_tcp():
    sock, address, port= startup_tcp_client(SERVER_ADDRESS, SERVER_PORT)

    recv_size = 1024
    # データ受信をサブスレッドで実行
    thread = threading.Thread(target=recv_data, args=(sock, recv_size,))
    thread.start()

    # header送信テスト中
    send_tcp_message(sock, _header.CREATE_ROOM)

    # データ入力ループ
    try:
        while True:
            data = input("> ")
            if data == "exit":
                # sock.send(data.encode("utf-8"))
                # header = create_header(EXIT_MESSAGE, 0, 0)
                # sock.send(header)
                send_tcp_message(sock, _header.EXIT_MESSAGE)
                break
            else:
                try:
                    send_tcp_message(sock, _header.SEND_MESSAGE)
                    # sock.send(data.encode("utf-8"))
                except ConnectionResetError:
                    break
                except Exception as e:
                    print("Error: ", + str(e))
                    break
    finally:
        print("shutdown main")
        sock.shutdown(socket.SHUT_RD)
        sock.close()
    

def main_udp():
    sock, address, port = startup_udp_client(CLIENT_ADDRESS)

    recv_size = 1024
    # データ受信をサブスレッドで実行
    thread = threading.Thread(target=recv_data, args=(sock, recv_size, ))
    thread.start()

    # header送信テスト中
    send_udp_message(sock, SERVER_ADDRESS, SERVER_PORT, _header.CREATE_ROOM)

    # データ入力ループ
    try:
        while True:
            data = input("> ")
            if data == "exit":
                send_udp_message(sock, SERVER_ADDRESS, SERVER_PORT, _header.EXIT_MESSAGE)
                break
            else:
                try:
                    print("leadched!")
                    send_udp_message(sock, SERVER_ADDRESS, SERVER_PORT, _header.SEND_MESSAGE)
                except ConnectionResetError:
                    break
                except Exception as e:
                    print("Error: ", + str(e))
                    break
    finally:
        print("shutdown main")
        sock.close()
    

if __name__ == "__main__":
    # main_tcp()
    main_udp()

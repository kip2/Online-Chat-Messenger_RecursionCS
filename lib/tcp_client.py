import socket
from lib._header import *
from lib.port_scan import *

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

def send_tcp_message(sock, header_message):
    """
        TCPクライアントからメッセージを送信する
    """
    header = create_header(header_message, 0, 0)
    sock.send(header)
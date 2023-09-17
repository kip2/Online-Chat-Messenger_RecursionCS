import socket
from lib._header import *
from lib.port_scan import *

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

def send_udp_message(sock, SERVER_ADDRESS, SERVER_PORT, header_message):
    """
        UDPクライアントからメッセージを送信する
    """
    header = create_header(header_message, 0, 0)
    sock.sendto(header, (SERVER_ADDRESS, SERVER_PORT))

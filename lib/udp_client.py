import socket
from lib._header import *
from lib.port_scan import *

class UDP_Client:
    def __init__(self):
        self.sock, self.addr, self.port = startup_udp_client()

    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        self.sock.close()

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

def send_udp_header(sock, SERVER_ADDRESS, SERVER_PORT, header_message):
    """
        UDPクライアントからheaderを送信する
    """
    header = request_header(header_message, 0, 0)
    sock.sendto(header, (SERVER_ADDRESS, SERVER_PORT))

def send_udp_message(sock, SERVER_ADDRESS, SERVER_PORT, message):
    """
        UDPクライアントからheaderを送信する
    """
    message = encode_message(message)
    sock.sendto(message, (SERVER_ADDRESS, SERVER_PORT))

def encode_message(message: str):
    """
        utf-8 の 
        str -> byte へのエンコード
    """
    return message.encode(CHARA_CODE)

def test_udp_class():
    sock, addr, port = startup_udp_client()
    print(f"socket = {sock}, address = {addr}, port = {port}")
    sock.close()
    with UDP_Client() as s:
        print("別のテスト")
        print(s)

if __name__ == "__main__":
    test_udp_class()
import socket
from lib._header import *
from lib.port_scan import *

class TCP_Client:
    def __init__(self, server_address, server_port):
        self.server_address = server_address
        self.server_port = server_port
        self.sock, self.addr, self.port = startup_tcp_client(self.server_address, self.server_port)

    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        """
            python終了時にsocketをcloseする
        """
        self.sock.close()

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

def send_tcp_header(sock, header_message):
    """
        TCPクライアントからheaderを送信する
    """
    header = request_header(header_message, 0, 0)
    sock.send(header)

def send_tcp_message(sock, message):
    """
        TCPクライアントからメッセージを送信する
    """
    message = encode_message(message)
    sock.send(message)

def encode_message(message: str):
    """
        utf-8 の 
        str -> byte へのエンコード
    """
    return message.encode("utf-8")

def test_tcp_class():
    # sock, addr, port = startup_tcp_client(SERVER_ADDRESS, SERVER_PORT)
    # print(f"socket = {sock}, address = {addr}, port = {port}")
    # sock.close()
    with TCP_Client(SERVER_ADDRESS, SERVER_PORT) as t:
        print("TCPのテスト")
        print(t)
    

if __name__ == "__main__":
    test_tcp_class()
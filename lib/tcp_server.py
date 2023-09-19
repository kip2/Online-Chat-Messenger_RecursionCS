import socket
from lib.port_scan import *
from lib._address_config import *
from lib._header import *


class TCP_Server:
    def __init__(self):
        self.sock, self.addr, self.port = startup_tcp_server()

    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        self.sock.close()

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

def send_server_message(connection, message):
    """
        connectionに、messageをutf-8にencodeして送るだけの関数
    """
    connection.send(message.encode(CHARA_CODE))

# ----- test case -----
def test_tcp_class():
    sock, addr, port = startup_tcp_server()
    print(f"socket = {sock}, address = {addr}, port = {port}")
    sock.close()
    with TCP_Server() as t:
        print("TCPのテスト")
        print(t)
    

if __name__ == "__main__":
    test_tcp_class()
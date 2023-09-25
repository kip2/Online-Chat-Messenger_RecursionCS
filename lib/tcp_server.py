import sys
import socket
from lib.port_scan import *
from lib._address_config import *
from lib._header import *


class TCP_Server:
    def __init__(self, port):
        self.sock, self.addr, self.port = startup_tcp_server(server_port=port)

    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        self.sock.close()

def startup_tcp_server(server_address:str = SERVER_ADDRESS, server_port:int = None, listen=5) -> tuple:
    """
        TCPサーバーを立てる関数
        connect用のsocketと、(IP_address, PORT)のタプルを返す
    """
    # # portが指定されていなければ自動で生成
    # if server_port == None: 
    #     server_port = available_tcp_port(server_address)

    try:
        sock = socket.socket(NETWORK_SOCKET_TYPE, socket.SOCK_STREAM) 
        sock.bind((server_address, server_port))
        sock.listen(listen)
        return (sock, server_address, server_port)
    except (socket.timeout, ConnectionRefusedError):
        return

def send_server_message(connection, message):
    """
        connectionに、messageをutf-8にencodeして送るだけの関数
    """
    connection.send(message.encode(CHARA_CODE))

def server_exit(sock):
    """
        serverのソケット終了処理
    """
    sock.close()
    sys.exit(0)

# ----- test case -----
def test_tcp_class():
    sock, addr, port = startup_tcp_server()
    print(f"socket = {sock}, address = {addr}, port = {port}")
    sock.close()
    with TCP_Server(CHAT_SERVER_PORT) as t:
        print("TCPのテスト")
        print(t)
    

def test_startup_tcp_server():
    socket1, addr1, port1 = startup_tcp_server()
    socket2, addr2, port2 = startup_tcp_server()
    socket3, addr3, port3 = startup_tcp_server()
    socket4, addr4, port4 = startup_tcp_server()
    socket5, addr5, port5 = startup_tcp_server()

if __name__ == "__main__":
    # test_tcp_class()
    test_startup_tcp_server()
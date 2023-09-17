import socket
from lib.port_scan import *
from lib._address_config import *

class UDP_Server:
    def __enter__(self):
        self.sock, self.addr, self.port = startup_udp_server()
        return (self.sock, self.addr, self.port) 
    
    def __exit__(self, *args):
        self.sock.close()


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

def test_udp_class():
    sock, addr, port = startup_udp_server()
    print(f"socket = {sock}, address = {addr}, port = {port}")
    sock.close()
    with UDP_Server() as s:
        print("別のテスト")
        print(s)
    
if __name__ == "__main__":
    test_udp_class()
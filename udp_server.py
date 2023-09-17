import _address_config
from port_scan import *

class UDP_Server:
    def __enter__(self):
        self.sock, self.addr, self.port = startup_udp_server()
        return (self.sock, self.addr, self.port) 
    
    def __exit__(self, *args):
        self.sock.close()


def startup_udp_server(server_address:str = _address_config.SERVER_ADDRESS, server_port:str = None) -> tuple:
    """
        UDPサーバーを立てる関数
        connect用のsocketと、(IP_address, PORT)のタプルを返す
    """
    # portが指定されていなければ自動で生成
    if server_port == None:
        server_port = available_udp_port(server_address)

    try:
        sock = socket.socket(_address_config.NETWORK_SOCKET_TYPE, socket.SOCK_DGRAM) 
        sock.bind((server_address, server_port))
        return (sock, server_address, server_port)
    except (socket.timeout, ConnectionRefusedError):
        return
from port_scan import *

# 定数読み込み用
import _address_config

class TCP_Server:
    def __enter__(self):
        self.sock, self.addr, self.port = startup_tcp_server()
        return (self.sock, self.addr, self.port) 
    
    def __exit__(self, *args):
        self.sock.close()

def startup_tcp_server(server_address:str = _address_config.SERVER_ADDRESS, server_port:int = None) -> tuple:
    """
        TCPサーバーを立てる関数
        connect用のsocketと、(IP_address, PORT)のタプルを返す
    """
    # portが指定されていなければ自動で生成
    if server_port == None: 
        server_port = available_tcp_port(server_address)

    try:
        sock = socket.socket(_address_config.NETWORK_SOCKET_TYPE, socket.SOCK_STREAM) 
        sock.bind((server_address, server_port))
        sock.listen(1)
        return (sock, server_address, server_port)
    except (socket.timeout, ConnectionRefusedError):
        return
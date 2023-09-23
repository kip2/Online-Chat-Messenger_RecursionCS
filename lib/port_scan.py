import socket
from lib._address_config import *

# 使用する予定のport番号の範囲
PORT_RANEG_MIN = 9001
PORT_RANEG_MAX = 10000

SERVER_HOST = SERVER_ADDRESS
CLIENT_HOST = CLIENT_ADDRESS

# 注意：openなら使用しているので、closeのportを使用する
def is_tcp_port_open(host:str, port: int) -> bool:
    """
        tcpのportがopenであるかどうかをbooleanで返す関数
    """
    try:
        # ソケットを作成し、指定したポートに接続を試みる
        with socket.socket(NETWORK_SOCKET_TYPE, socket.SOCK_STREAM) as sock:
            # 接続タイムアウトの設定
            sock.settimeout(1)  
            sock.connect((host, port))
        return True  
    except (socket.timeout, ConnectionRefusedError):
        # timeoutしているので、portが空いている
        return False

def is_udp_port_open(host:str, port: int) -> bool:
    """
        udpのportがopenであるかどうかをbooleanで返す関数
    """
    try:
        # bindできればportが空いている
        with socket.socket(NETWORK_SOCKET_TYPE, socket.SOCK_DGRAM) as sock:
            sock.bind((host, port))
        return True  
    # portが空いてない
    except OSError:
        return False  

# def available_tcp_port(host:str=SERVER_HOST,  range_min=PORT_RANEG_MIN, range_max=PORT_RANEG_MAX) -> int:
#     """
#         portのrangeの範囲から、使えるtcpのport番号を返す
#     """
#     for i in range(range_min, range_max):
#         if is_tcp_port_open(host, i) == False:
#             return i
#     return None

def available_udp_port(host:str=CLIENT_HOST,  range_min=PORT_RANEG_MIN, range_max=PORT_RANEG_MAX) -> int:
    """
        portのrangeの範囲から、使えるudpのport番号を返す
    """
    for i in range(range_min, range_max):
        if is_udp_port_open(host, i) == True:
            return i
    return None

if __name__ == "__main__":
    # ポートをチェックしたいホストとポートを指定
    host = "127.0.0.1"
    # port = 9001


    # print(is_udp_port_open(CLIENT_HOST, 9001))
    port = available_tcp_port()
    port = available_udp_port()
    print(port)
    # port = available_port()
    # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    #     sock.bind((host, port))
    #     sock.listen()
        
    #     connection, client_address = sock.accept()



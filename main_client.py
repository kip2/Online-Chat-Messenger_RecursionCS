import socket
import sys
import threading
from lib.port_scan import *
from lib.udp_client import *
from lib.tcp_client import *

# 定数用
from lib._address_config import *
from lib._header import *


# データ受信関数
def recv_data(sock, recv_size):
    
    """
        データ受信用のthread
    """
    try:
        while True:
            try:
                data = sock.recv(recv_size)
                if data == b"":
                    break
                print(data.decode("utf-8"))
            except ConnectionResetError:
                break
            except OSError as e:
                if e.errno == 9:
                    break
            except Exception as e:
                print("Error: ", + str(e))
                break
    finally:
        print("shutdown helper.")
        sock.close()


def main_tcp():
    """
        tcp通信のmain関数
    """
    sock, address, port= startup_tcp_client(SERVER_ADDRESS, SERVER_PORT)

    recv_size = 1024
    # データ受信をサブスレッドで実行
    thread = threading.Thread(target=recv_data, args=(sock, recv_size,))
    thread.start()

    # header送信テスト中
    send_tcp_message(sock, CREATE_ROOM)

    # データ入力ループ
    try:
        while True:
            data = input("> ")
            if data == "exit":
                send_tcp_message(sock, EXIT_MESSAGE)
                break
            else:
                try:
                    send_tcp_message(sock, SEND_MESSAGE)
                    # sock.send(data.encode("utf-8"))
                except ConnectionResetError:
                    break
                except Exception as e:
                    print("Error: ", + str(e))
                    break
    except Exception as e:
        print("Error: ", str(e))
    finally:
        print("shutdown main")
        sock.shutdown(socket.SHUT_RD)
        sock.close()
    

def main_udp():
    """
        udp通信のmain関数
    """
    sock, address, port = startup_udp_client(CLIENT_ADDRESS)

    recv_size = 1024
    # データ受信をサブスレッドで実行
    thread = threading.Thread(target=recv_data, args=(sock, recv_size, ))
    thread.start()

    # header送信テスト中
    send_udp_message(sock, SERVER_ADDRESS, SERVER_PORT, CREATE_ROOM)

    # データ入力ループ
    try:
        while True:
            data = input("> ")
            if data == "exit":
                send_udp_message(sock, SERVER_ADDRESS, SERVER_PORT, EXIT_MESSAGE)
                break
            else:
                try:
                    print("leadched!")
                    send_udp_message(sock, SERVER_ADDRESS, SERVER_PORT, SEND_MESSAGE)
                except ConnectionResetError:
                    break
                except Exception as e:
                    print("Error: ", + str(e))
                    break
    finally:
        print("shutdown main")
        sock.close()
    

if __name__ == "__main__":
    # main_tcp()
    main_udp()

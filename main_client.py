import sys
import threading
from lib.port_scan import *
from lib.udp_client import *
from lib.tcp_client import *
from lib.client_method import *

# 定数用
from lib._address_config import *
from lib._header import *

RECV_SIZE = 4096

def printd(byte_data):
    """
        byteデータをdecodeしてprintする関数
    """
    print(byte_data.decode(CHARA_CODE))

def mes_decode(byte_data):
    """
        受信したメッセージ(byte)をデコードする
    """
    return byte_data.decode(CHARA_CODE)

def flush_display(log):
    print("=====================")
    print("----- log ------")
    print()
    print(log)
    print("---------------------")
    print("Enter your message ")

    
def recv_data(sock, recv_size):
    """
        データ受信用のthread
    """
    log = ""
    try:
        while True:
            try:
                data = sock.recv(recv_size)
                if data == b"":
                    break
                # printd(data)
                log += mes_decode(data) + "\n"
                flush_display(log)
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


def chat_client():
    sock, address, port = startup_udp_client(CLIENT_ADDRESS)
    # データ受信をサブスレッドで実行
    thread = threading.Thread(target=recv_data, args=(sock, RECV_SIZE, ))
    thread.start()
    
    # 入室処理用ループ
    while True:
        data = input("入室する部屋を選んでください")
        if data == "exit":
            client_exit(sock)
        else:
            try:
                send_enter_room_message(sock, SERVER_ADDRESS, SERVER_PORT,"room1")
                break
            except ConnectionResetError:
                client_exit(sock)
            except Exception as e:
                print("Error: ", + str(e))
                client_exit(sock)
                break

    # 入室後メッセージ入力ループ
    try:
        while True:
            data = input()
            if data == "exit":
                send_udp_header(sock, SERVER_ADDRESS, SERVER_PORT, CLIENT_EXIT_MESSAGE)
                break
            if data == "server exit":
                send_udp_header(sock, SERVER_ADDRESS, SERVER_PORT, EXIT_MESSAGE)
                break
            else:
                try:
                    send_chat_message(sock, SERVER_ADDRESS, SERVER_PORT, "room1", data )
                except ConnectionResetError:
                    break
                except Exception as e:
                    print("Error: ", + str(e))
                    break
    finally:
        print("shutdown main")
        client_exit(sock)

def client_exit(sock):
    """
        clientのsocketを閉じる処理
    """
    sock.close()
    sys.exit(0)

NAME = "client1"
def create_chat_message_prefix(room_name, message):
    """
        chatメッセージ送信用のプレフィックス
    """
    return room_name + ":" + NAME + ":" + message

def send_chat_message(sock, server_address, server_port, room_name, message):
    """
        chatメッセージを送信
    """
    message = create_chat_message_prefix(room_name, message)
    send_udp_message(sock, server_address, server_port, message)
    return

def create_enter_room_prefix(room_name):
    """
        入室用メッセージのプレフィックスを作成する
    """
    return room_name + ":" + NAME

def send_enter_room_message(sock, server_address, server_port, room_name):
    """
        入室メッセージを送信する
    """
    message = create_enter_room_prefix(room_name)
    send_udp_message(sock, server_address, server_port, message)
    return
    


if __name__ == "__main__":
    chat_client()
    # main_tcp()
    # main_udp()
    # test_chat_room()

    # cipher_suite = Fernet(SECRET_KEY)
    # test_multi_thread_tcp_client()
    
    # cr = create_information_new_chat_room()
    # print(cr)
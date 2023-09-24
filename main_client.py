import socket
import sys
import threading
from lib.port_scan import *
from lib.udp_client import *
from lib.tcp_client import *
from lib.client_method import *

# 定数用
from lib._address_config import *
from lib._header import *

RECV_SIZE = 1024

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
                printd(data)
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

def test_chat_room():
    with UDP_Client() as clt:
        sock = clt.sock
        thread = threading.Thread(target=recv_data, args=(sock, RECV_SIZE,))
        thread.start()
        
        # header送信テスト中
        # send_udp_header(sock, SERVER_ADDRESS, SERVER_PORT, CREATE_ROOM)

        # データ入力ループ
        while True:
            data = input("> ")
            if data == "exit":
                send_udp_header(sock, SERVER_ADDRESS, SERVER_PORT, CLIENT_EXIT_MESSAGE)
                break
            if data == "se":
                send_udp_header(sock, SERVER_ADDRESS, SERVER_PORT, EXIT_MESSAGE)
                break
            else:
                try:
                    # header送信
                    # send_udp_header(sock, SERVER_ADDRESS, SERVER_PORT, SEND_MESSAGE)
                    # messageの送信
                    message = data
                    send_udp_message(sock, SERVER_ADDRESS, SERVER_PORT, message)

                except ConnectionResetError:
                    break
                except Exception as e:
                    print("Error: ", + str(e))
                    break

def main_tcp():
    """
        tcp通信のmain関数
    """
    sock, address, port= startup_tcp_client(SERVER_ADDRESS, SERVER_PORT)
    print(sock, address, port)

    # データ受信をサブスレッドで実行
    thread = threading.Thread(target=recv_data, args=(sock, RECV_SIZE,))
    thread.start()

    # header送信テスト中
    send_tcp_header(sock, CREATE_ROOM)

    # データ入力ループ
    try:
        while True:
            data = input("> ")
            if data == "exit":
                send_tcp_header(sock, EXIT_MESSAGE)
                break
            else:
                try:
                    send_tcp_header(sock, SEND_MESSAGE)
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

def test_multi_thread_tcp_client():
    thread1 = threading.Thread(target=main_tcp)
    thread1.start()
    thread2 = threading.Thread(target=main_tcp)
    thread2.start()
    thread3 = threading.Thread(target=main_tcp)
    thread3.start()
    thread4 = threading.Thread(target=main_tcp)
    thread4.start()
    thread5 = threading.Thread(target=main_tcp)
    thread5.start()
    

def main_udp():
    """
        udp通信のmain関数
    """
    sock, address, port = startup_udp_client(CLIENT_ADDRESS)

    # データ受信をサブスレッドで実行
    thread = threading.Thread(target=recv_data, args=(sock, RECV_SIZE, ))
    thread.start()

    # header送信テスト中
    send_udp_header(sock, SERVER_ADDRESS, SERVER_PORT, CREATE_ROOM)

    # データ入力ループ
    try:
        while True:
            data = input("> ")
            if data == "exit":
                send_udp_header(sock, SERVER_ADDRESS, SERVER_PORT, CLIENT_EXIT_MESSAGE)
                break
            if data == "server exit":
                send_udp_header(sock, SERVER_ADDRESS, SERVER_PORT, EXIT_MESSAGE)
                break
            else:
                try:
                    send_udp_header(sock, SERVER_ADDRESS, SERVER_PORT, SEND_MESSAGE)
                except ConnectionResetError:
                    break
                except Exception as e:
                    print("Error: ", + str(e))
                    break
    finally:
        print("shutdown main")
        sock.close()

def chat_client():
    
    sock, address, port = startup_udp_client(CLIENT_ADDRESS)
    # データ受信をサブスレッドで実行
    thread = threading.Thread(target=recv_data, args=(sock, RECV_SIZE, ))
    thread.start()
    
    # 起動時にヘッダを送信して、それに従って入室させればよろしい

    # データ入力ループ
    try:
        while True:
            data = input("> ")
            if data == "exit":
                send_udp_header(sock, SERVER_ADDRESS, SERVER_PORT, CLIENT_EXIT_MESSAGE)
                break
            if data == "server exit":
                send_udp_header(sock, SERVER_ADDRESS, SERVER_PORT, EXIT_MESSAGE)
                break
            else:
                try:
                    send_udp_header(sock, SERVER_ADDRESS, SERVER_PORT, SEND_MESSAGE)
                except ConnectionResetError:
                    break
                except Exception as e:
                    print("Error: ", + str(e))
                    break
    finally:
        print("shutdown main")
        sock.close()


if __name__ == "__main__":
    chat_client()
    # main_tcp()
    # main_udp()
    # test_chat_room()

    # cipher_suite = Fernet(SECRET_KEY)
    # test_multi_thread_tcp_client()
    
    # cr = create_information_new_chat_room()
    # print(cr)
# const request header
CREATE_ROOM = 1
REQUEST_ROOM_LIST = 2
REQUEST_LOG_FILE = 3
ENTER_ROOM = 4
SEND_MESSAGE = 5
CLIENT_EXIT_MESSAGE = 6
EXIT_MESSAGE = 0

# 文字コード
CHARA_CODE = "UTF-8"


def request_header(client_request, message_length,data_length):
    """
        送信用のheaderを作成する関数
    """
    # todo: やりとりの様式が決まっていないので、仮で実装している
    return client_request.to_bytes(1, "big") + message_length.to_bytes(3,"big") + data_length.to_bytes(4, "big")



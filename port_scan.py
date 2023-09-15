import socket

# 使用する予定のport番号の範囲
PORT_RANEG_MIN = 9001
PORT_RANEG_MAX = 10000

HOST = "127.0.0.1"

# 注意：openなら使用しているので、closeのportを使用する
def is_port_open(host:str, port: int) -> bool:
    """
        portがopenであるかどうかをbooleanで返す関数
    """
    try:
        # ソケットを作成し、指定したポートに接続を試みる
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)  # 接続タイムアウトを設定（秒）
            sock.connect((host, port))
        return True  # ポートが開いている場合
    except (socket.timeout, ConnectionRefusedError):
        return False  # ポートが開いていない場合

def available_port(host: str = HOST, range_min=PORT_RANEG_MIN, range_max=PORT_RANEG_MAX) -> int:
    """
        portのrangeの範囲から、使えるport番号を返す
    """
    for i in range(range_min, range_max):
        if is_port_open(host, i) == False:
            return i
    return None

if __name__ == "__main__":
    # ポートをチェックしたいホストとポートを指定
    # host = 'example.com'
    # port = 80
    host = "127.0.0.1"
    port = 9001

    print(available_port())

    # for i in range(9001, 10000):
    #     print("test", i)
    #     if is_port_open(host, i):
    #         print(f"Port {i} is OK!")
    #         break

    # if is_port_open(host, port):
    #     print(f"Port {port} on {host} is open.")
    # else:
    #     print(f"Port {port} on {host} is closed.")

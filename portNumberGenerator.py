import random

port_number_arr = []

def create_port_number() :
    """
        port番号ランダム生成機
    """
    # 以下の範囲で番号を生成する
    # 1024~65535
    r = random.randint(1024, 65535)
    return r

if __name__ == "__main__":
    print(create_port_number())

    
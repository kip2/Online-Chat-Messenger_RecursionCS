import random

# main関数の方で、管理し直す
port_number_arr = []

def create_port_number() :
    """
        port番号ランダム生成機

        以下の範囲で番号を生成する
        1024~65535
    """
    #rangeMin = 1024
    #rangeMax = 65535
    rangeMin = 1024
    rangeMax = 1150 

    r = random.randint(rangeMin, rangeMax)

    while (r in port_number_arr):
        # todo 回数制限しないと無限ループに陥るバグあり
        r = random.randint(rangeMin, rangeMax)
        #print("被った！", end="")

    port_number_arr.append(r)
    return r

if __name__ == "__main__":
    """
        test case: 被った時にちゃんとループし直しているか
    """
    for i in range(100):
        print(create_port_number())
    print(port_number_arr)

    
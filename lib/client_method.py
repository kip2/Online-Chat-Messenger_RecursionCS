
def create_information_new_chat_room():
    """
        新しいチャットルームを作成する関数
        clientから送信するメッセージ
    """
    while True:
        room_name = input("Room Name? > ")
        if not room_name == ""  and not room_name.isspace(): break
        
    while True:
        max_member = input("maximum number? > ")
        if max_member.isdecimal(): break
    return (room_name, max_member)
    

if __name__ == "__main__":
    # cr = create_new_chat_room()
    # print("cr:", cr, " cr.name:", cr.title, " cr.maximum:", cr.max_member)
    cr = create_information_new_chat_room()
    print(cr)
    pass
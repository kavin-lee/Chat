"""
chat room client
env:python3.6
socket fork 练习
"""

from socket import *
import os, sys


# 服务器地址
ADDR = ('176.234.8.11', 9000)


def login(s):
    while True:
        name = input("姓名:")
        msg = 'L ' + name
        s.sendto(msg.encode(), ADDR)
        # 等待回应
        data, addr = s.recvfrom(1024)
        if data.decode() == 'OK':
            print("您已进入聊天室")
            return name
        else:
            print(data.decode())


def send_msg(s, name):
    """
        发送消息
    :param s:
    :param name:
    :return:
    """
    while True:
        try:
            text = input("发言:")
        except KeyboardInterrupt:
            text = "quit"
        if text == "quit" or text == "q":
            msg = "Q " + name
            s.sendto(msg.encode(), ADDR)
            sys.exit("退出聊天室")
        msg = "C %s %s" % (name, text)
        s.sendto(msg.encode(), ADDR)


def recv_msg(s):
    """
        接收消息
    :param s:
    :return:
    """
    while True:
        data, addr = s.recvfrom(2048)
        # 服务端发送exit表示让客户端退出
        if data.decode() == "EXIT":
            sys.exit(0)
        print('\r'+data.decode()+"\n发言:",end=" ")


# 创建网络连接
def main():
    s = socket(AF_INET, SOCK_DGRAM)
    name = login(s)
    pid = os.fork()
    if pid < 0:
        sys.exit("Error!")
    elif pid == 0:
        send_msg(s, name)
    else:
        recv_msg(s)




if __name__ == '__main__':
    main()

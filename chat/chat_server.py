"""
chat room sever
env:python3.6
socket fork 练习
"""

from socket import *
import os, sys

# 服务器地址
ADDR = ('0.0.0.0', 9000)
# 存储用户信息
dict_user = {}


def do_request(s):
    """
        接受客户端请求,并处理客户端请求
    :param s:
    :return:
    """
    while True:
        data, addr = s.recvfrom(1024)
        info = data.decode().split(" ")
        # 区分请求类型
        if info[0] == "L":
            do_login(s, info[1], addr)
        elif info[0] == "C":
            msg = " ".join(info[2:])
            do_chat(s, info[1], msg)
        elif info[0] == "Q":
            if info[1] not in dict_user:
                s.sendto(b'EXIT',addr)
                continue
            do_logout(s, info[1])


def do_logout(s, name):
    """
        退出聊天室
    :param s:
    :param msg:
    :return:
    """
    msg = "%s退出了聊天室" % name
    try:
        del dict_user[name]
    except Exception:
        pass
    else:
        for i in dict_user:
            if i != name:
                s.sendto(msg.encode(), dict_user[i])
            else:
                s.sendto(b'EXIT', dict_user[i])


def do_login(s, name, addr):
    """
        判断是否要客户进入聊天室
    :param s:
    :param name:
    :param addr:
    :return:
    """
    if name in dict_user or "管理" in name:
        s.sendto("该用户已存在".encode(), addr)
        return

    s.sendto(b'OK', addr)

    # 通知其他人
    info = '欢迎%s进入聊天室' % name
    for i in dict_user:
        s.sendto(info.encode(), dict_user[i])
    # 加入用户
    dict_user[name] = addr


def do_chat(s, name, msg):
    """
        聊天
    :param s:
    :param name: 收到的姓名
    :param msg: 转发的信息
    :return:
    """
    msg = "%s : %s" % (name, msg)
    for i in dict_user:
        if i != name:
            s.sendto(msg.encode(), dict_user[i])


# 创建网络连接
def main():
    # 套接字UDP网络
    s = socket(AF_INET, SOCK_DGRAM)
    s.bind(ADDR)

    pid = os.fork()
    if pid < 0:
        return
        # 发送管理员消息
    elif pid == 0:
        while True:
            msg=input("超管提醒:")
            msg="C 超管提醒 "+msg
            s.sendto(msg.encode(),ADDR)
    else:
        # 请求处理
        do_request(s)  # 处理客户端请求


if __name__ == '__main__':
    main()

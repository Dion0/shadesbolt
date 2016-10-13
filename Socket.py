import socket
from Config import HOST, PORT, PASS, NICK

def openSocket(channel, host = HOST, port = PORT, pwd = PASS, nick = NICK):
    s = socket.socket()
    s.connect((host, port))
    s.send("PASS {}\r\n".format(pwd).encode("utf-8"))
    s.send("NICK {}\r\n".format(nick).encode("utf-8"))
    s.send("JOIN #{}\r\n".format(channel).encode("utf-8"))
    return s

from Read import getUser, getMessage
from Socket import openSocket, sendMessage
from Initialize import joinRoom
from Markov import *
from TwitchUtil import *
from datetime import datetime
import time
import sys

MSG_TO_GEN = 50
CHECK_ONLINE_SLEEP = 9000
FILE_NAME = "out.txt"
F_LOG_NAME = "chatlog.txt"
last_online = False

def main_loop():
    f_log = open(F_LOG_NAME, 'a', encoding = 'utf-8')
    non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
    s = openSocket()
    joinRoom(s)
    readbuffer = ""
    running = True
    getChatters()
    chain = read_chain()
    msg_counter = 0
    ticks = 0


    while running:
        readbuffer = readbuffer + s.recv(1024).decode("utf-8")
        temp = readbuffer.split("\n")
        readbuffer = temp.pop()
        for line in temp:
            #really need to change that
            if "PING" in line:
                s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
                break
            user = getUser(line)
            message = getMessage(line)
            msg_lower = message.lower()
            if ("meaning" in msg_lower or "purpose" in msg_lower):
                sendMessage(s, "No matter whAt I do, I'm always THIS, always THIS BODY THIS MIND THIS WORLD. NO WAY OUT%")
            chain.process_sentence(message)
            f_log.write((user + ':' + message + '\n').translate(non_bmp_map))
            
            msg_counter += 1
            if (msg_counter % 20 == 0):
                print(msg_counter)
            if msg_counter % MSG_TO_GEN == 0:
                to_send = chain.gen_sentence()
                out_f = open(FILE_NAME, 'a', encoding = "utf-8")
                out_f.write((to_send + "\n").translate(non_bmp_map))
                out_f.close()
                sendMessage(s, to_send)
                write_chain(chain)

        if ticks == CHECK_ONLINE_SLEEP:
            ticks = 0
            if (not checkLive(last_online)):
                sendMessage(s, "time to sleep ( -ᴗ-)")
                print("time to sleep")
                running = False
                break
        ticks += 1
        time.sleep(0.1)
    f_log.close()
    write_chain(chain)

while True:
    if checkLive(last_online):
        main_loop()
    print(str(datetime.now().time()) + ": still not online :\\")
    time.sleep(900)



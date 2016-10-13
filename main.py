from Bot import *
from StrUtil import *
import threading, time, CommandQueue, Whisperer


if __name__ == "__main__":
    msg_mutex = threading.RLock()
    bots = []
    chn_names = []
    com_q = CommandQueue.CommandQueue()
    running = True
    inp = ''

    with open('channels.txt', 'r') as ch_file:
        str = ch_file.read()
        lines = str.split('\n')
        for line in lines:
            if len(line) == 0:
                continue
            if not line in chn_names:
                chn_names.append(line)
                tmp_bot = Bot(msg_mutex, com_q, line)
                tmp_bot.start()
                bots.append(tmp_bot)

    wisp = Whisperer.Whisperer(msg_mutex, com_q)
    wisp.start()

    while running:
        inp = input()
        if inp.startswith('add '):
            inp = inp[4:]
            print(inp)
            arg = inp.split(' ')
            if len(arg) == 1:
                arg.append('12')
            tmp_bot = Bot(msg_mutex, com_q, arg[0], int(arg[1]))
            tmp_bot.start()
            bots.append(tmp_bot)
        elif inp.startswith('break'):
            running = False
            print('breaking')
            for bot in bots:
                bot.stop()
            wisp.stop()
        elif isValidCommand(inp):
            print('valid')
            com_q.put(inp)
        else:
            print('invalid')

    for bot in bots:
        bot.join()
    wisp.join()

    print('dun')


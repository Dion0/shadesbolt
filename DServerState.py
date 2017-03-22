import Markov
from discord import Message as dMessage

CFG_PREFIX = "discord_"
CFG_POSTFIX = ".cfg"

DEF_msg_to_reply = 69
DEF_whitelist_mode = False
DEF_chn_whitelist = []


class DState:
    def __init__(self, serv_id = "", chn_list = [], cont_len = 50):
        self.id = serv_id
        self.save_name = Markov.SAVE_PREFIX + serv_id
        self.ch = Markov.read_chain(self.save_name)
        self.context = [Markov.DEF_STR] * (cont_len + 1)
        self.cont_len = cont_len
        self.cont_cnt = 0

        self.msg_to_reply = 0
        self.msg_counter = 0
        self.chn_whitelist = {i:False for i in chn_list}
        self.whitelist_mode = False

        self.load_cfg()

    def save_ch(self):
        Markov.write_chain(self.ch, self.save_name)

    """

    CFG FILE FORMAT:
    number of messages to trigger response
    bool - is it a whitelist-mode server?
    names of whitelisted channels separated by spaces

    """

    def load_cfg(self):
        filename = CFG_PREFIX + self.id + CFG_POSTFIX
        try:
            cfg_file = open(filename, 'r')
            self.msg_to_reply = int(cfg_file.readline())
            print(self.msg_to_reply)
            self.whitelist_mode = int(cfg_file.readline()) == 1
            print(self.whitelist_mode)
            tmp = cfg_file.readline().split(' ')
            for i in tmp:
                self.chn_whitelist[i] = True
            print(self.chn_whitelist)
            cfg_file.close()
        except:
            print('loading default dstate for ' + self.id + ' and creating a cfg file')
            self.msg_to_reply = DEF_msg_to_reply
            print(self.msg_to_reply)
            self.whitelist_mode = DEF_whitelist_mode
            print(self.whitelist_mode)
            self.chn_whitelist = DEF_chn_whitelist
            print(self.chn_whitelist)
            self.save_cfg()


    def save_cfg(self):
        filename = CFG_PREFIX + self.id + CFG_POSTFIX
        cfg_file = open(filename, 'w')
        cfg_file.write(str(self.msg_to_reply) + '\n')
        cfg_file.write(str(int(self.whitelist_mode))
                       + '\n')
        tmp_list = [xkey for xkey, xval in self.chn_whitelist.items() if xval]
        cfg_file.write(" ".join(tmp_list).strip())
        print('saved config for ' + self.id)

    def reverse_mode(self):
        self.whitelist_mode = not self.whitelist_mode
        print(self.chn_whitelist)
        self.chn_whitelist = not self.chn_whitelist
        print(self.chn_whitelist)
        self.save_cfg()

    def process_msg(self, msg):
        assert isinstance(msg, dMessage)



if __name__ == '__main__':
    ds = DState('1')
    ds.load_cfg()
    print('dun')
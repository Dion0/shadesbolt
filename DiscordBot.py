import discord, asyncio, random
from Config import DISCORD_TOKEN
import StrUtil
from Markov import *
import logging

YOURFACE_CHANCE = 0.2

logging.basicConfig(level=logging.INFO)

DISCORD_CHAIN_FILE = 'chain_data_discord_fubz'
MSG_TO_GEN = 19
counter = 0

rude_responses = ['how about i slap your shit', 'up yours QuestionMark', 'http://puu.sh/rA91W/79f04a5452.png',
                  '( ° ͜ʖ͡°)╭∩╮', "it's time to stop", 'this human is look very stupid  ༼◥▶ل͜◀◤༽ ', 'dot dot dot']

PEPE = """

 ▬▬▬▬▬▬▬▬▬▬ஜ۩۞۩ஜ▬▬▬▬▬▬▬▬▬▬▬▬
  ⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
  ⬛🐸🐸🐸⬛🐸🐸⬛🐸🐸🐸⬛🐸🐸⬛⬛
  ⬛🐸⬛🐸⬛🐸⬛⬛🐸⬛🐸⬛🐸⬛⬛⬛
  ⬛🐸🐸🐸⬛🐸🐸⬛🐸🐸🐸⬛🐸🐸⬛⬛
  ⬛🐸⬛⬛⬛🐸⬛⬛🐸⬛⬛⬛🐸⬛⬛⬛
  ⬛🐸⬛⬛⬛🐸🐸⬛🐸⬛⬛⬛🐸🐸⬛⬛
  ⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
 ▬▬▬▬▬▬▬▬▬▬ஜ۩۞۩ஜ▬▬▬▬▬▬▬▬▬▬▬▬
"""

client = discord.Client()
ch = read_chain(DISCORD_CHAIN_FILE)

@asyncio.coroutine
def bg_task():
    yield from client.wait_until_login()


@client.event
@asyncio.coroutine
def on_message(message):
    global counter
    global MSG_TO_GEN
    author = message.author
    if author == client.user:
        return

    msg_lower = message.content.lower()
    #supreme
    if random.random() < 0.0001:
        yield from client.send_message(message.channel, PEPE)

    if message.content.startswith('.test') and author.name == 'dion':
        yield from client.send_message(message.channel, 'beep boop')
    if message.content.startswith('.save') and author.name == 'dion':
        print()
        write_chain(ch, DISCORD_CHAIN_FILE)
    if message.content.startswith('boltoid is'):
        msg_str = message.content[10:]
        if len(msg_str):
            if random.random() < YOURFACE_CHANCE:
                yield from client.send_message(message.channel, 'your face is' + msg_str)
    if 'uh oh' == msg_lower or 'uhoh' == msg_lower or 'uh-oh' == msg_lower:
        if (author.name == 'Mortzcent (Apl.De.Ap)') and random.random() < 0.3:
            yield from client.send_message(message.channel, 'fuk u apl')
        else:
            yield from client.send_message(message.channel, 'spaghetti-os')
        return
    if 'oh uh' == msg_lower or 'ohuh' == msg_lower or 'oh-uh' == msg_lower:
        yield from client.send_message(message.channel, rude_responses[random.randint(0, len(rude_responses) - 1)])
        return
    if 'thea-who?' == msg_lower:
        yield from client.send_message(message.channel, "theano")
        return
    if msg_lower.startswith('.set') and author.name == 'dion':
        cmd = msg_lower.split(' ')
        if cmd[1] == 'counter' and len(cmd) == 3:
            counter = int(cmd[2])
            print('set counter to ' + str(counter))
        elif cmd[1] == 'msg_to_gen' and len(cmd) == 3:
            MSG_TO_GEN = int(cmd[2])
            print('set msg_to_gen to ' + str(MSG_TO_GEN))


    print(str(author) + ":" + message.content)
    msg_c = message.channel
    if isinstance(msg_c, discord.Channel):
        print(msg_c.name)
        print(msg_c.server)
        print(msg_c.position)
    else:
        for r in msg_c.recipients:
            print(r)
        return


    if  message.content.startswith('.'):
        return
    msg, valid = StrUtil.sanitizeMessage(message.content, False)
    if (valid and len(msg.split(' ')) > 1):
        counter += 1
        print(counter)
        ch.process_sentence(msg)
        if (counter >= MSG_TO_GEN):
            MSG_TO_GEN = 19
            if random.random() < 0.2:
                MSG_TO_GEN = 10 + random.randint(1, 20)
            counter = 0
            to_send = ch.gen_sentence()
            yield from client.send_message(message.channel, to_send, tts=True)
            #print('sent: ' + to_send + '| to ' + message.channel)
            write_chain(ch, DISCORD_CHAIN_FILE)




@client.event
@asyncio.coroutine
def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')



if __name__ == '__main__':
    client.loop.create_task(bg_task())
    client.run(DISCORD_TOKEN)

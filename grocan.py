#!/usr/local/bin/python3

from random import randint, choice
import discord
import json
import os
from gtts import gTTS

countMsg = 0
nextMsg = 0

with open('config/grocan.json') as json_file:
    config = json.load(json_file)
    channelID = config['config']['channelID']
    msgInterval = config['config']['msg']

client = discord.Client()

sndLst = os.listdir("snd")
imgLst = os.listdir("img")


def getMsgResp():
    global countMsg, nextMsg, msgInterval, config
    countMsg += 1
    if countMsg >= nextMsg:
        nextMsg = randint(msgInterval[0],msgInterval[1])
        print("new interval:", nextMsg)
        countMsg = 0
        return choice(config['quotes'])
    else:
        return None

def addMessage(msg):
    global config
    config['quotes'].append(msg)
    print("add message:", msg)
    with open('grocan.json', 'w+') as outfile:
        json.dump(config['quotes'], outfile)


@client.event
async def on_ready():
    print(client.user.name,"has connected to Discord!")

@client.event
async def on_member_join(member):
    global config
    await member.create_dm()
    await member.dm_channel.send(
        str(member.name) + ' est twe gwo'
    )

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    global channelID, config, sndLst, imgLst
    channel = client.get_channel(int(channelID))
    if message.content[:4] == '&add' and str(message.channel.id) == channelID:
        addMessage(message.content[5:])
        await channel.send("OK, adding "+str(message.content[5:]))

    elif message.content[:4] == '&qte' and str(message.channel.id) == channelID:
        await channel.send(choice(config['quotes']))

    elif message.content[:4] == '&sel' and str(message.channel.id) == channelID:
        await channel.send(':salt: :salt:  '+choice(config['saltQuotes'])+'  :salt: :salt:')

    elif message.content[:6] == '&ewall' and str(message.channel.id) == channelID:
        try:
            size = message.content[7:]
            pos = size.find('x')
            w = int(size[0:pos])
            h = int(size[pos+1:])
            if w > 20 or h > 20:
                await channel.send('Two Gwo')
            else:
                for i in range(w):
                    msgStr = ''
                    for j in range(h):
                        msgStr += choice(config['emotes'])+' '
                    await channel.send(msgStr)
        except:
            pass

    elif message.content[:4] == '&img' and str(message.channel.id) == channelID:
        await channel.send(file=discord.File('img/'+choice(imgLst)))

    elif message.content[:5] == '&vqte':
        tts = gTTS(choice(config['quotes']), lang='fr')
        tts.save('tts.mp3')

        if len(client.voice_clients) > 0:
            voice = client.voice_clients[0]
            if voice.channel != message.author.voice.channel:
                await voice.move_to(message.author.voice.channel)
        else:
            voice = await message.author.voice.channel.connect()
        voice.play(discord.FFmpegPCMAudio('tts.mp3'))

    elif message.content[:5] == '&vsnd':
        if len(client.voice_clients) > 0:
            voice = client.voice_clients[0]
            if voice.channel != message.author.voice.channel:
                await voice.move_to(message.author.voice.channel)
        else:
            voice = await message.author.voice.channel.connect()
        voice.play(discord.FFmpegPCMAudio('snd/'+choice(sndLst)))
        
    elif message.content[:5] == '&help':
        await channel.send("``` &add expression -> to add an expression \n &qte -> to get a random quote  \n &vqte -> to get a random quote played \n &vsnd -> to get a random sound played  \n &img -> to get a random image  \n &ewall HxW -> to get a wall of random emotes```")

    else:
        resp = getMsgResp()
        if resp != None:
            await channel.send(resp)

client.run(config['config']['token'])
from asyncio import locks
from re import purge
import discord
from discord.ext.commands import Bot
from discord.enums import Status
from discord.ext import commands, tasks
from discord.utils import get
from discord_components import DiscordComponents, ComponentsBot, Button, SelectOption, Select
from random import randint, random
from time import sleep
import aiohttp
import datetime
import random
import json
import requests
import base64
import re
import os
import sys
import urllib.parse
import urllib.request as u
from cryptography.fernet import Fernet
import asyncio
import numpy as np
import cv2 as cv
from io import BytesIO
import time
from itertools import cycle
import xml.etree.ElementTree as et
import rule34

BOT_TOKEN = ""

ltime = time.asctime(time.localtime())
r = rule34.Rule34
def xmlparse(str):
	root = et.parse(u.urlopen(str))
	for i in root.iter('post'):
		fileurl = i.attrib['file_url']
		return fileurl
def xmlcount(str):
	root = et.parse(u.urlopen(str))
	for i in root.iter('posts'):
		count = i.attrib['count']
		return count
def pidfix(str):
	ye = int(xmlcount(r.urlGen(tags=str,limit=1)))
	ye = ye - 1
	return ye
def rdl(str,int):
	print(f'[INFO {ltime}]: integer provided: {int}')

	if int > 2000:
		int = 2000
	if int == 0:
		int == 0
		print(f'[INFO {ltime}]: entero es 0, complaciente para el error de desbordamiento compensado. ')	
	elif int != 0:	
		int = random.randint(1,int)
	print(f'[INFO {ltime}]: integer after randomizing: {int}')
	xurl = r.urlGen(tags=str,limit=1,PID=int)
	print(xurl)
	wr = xmlparse(xurl)
	
	if 'webm' in wr:
		if 'sound' not in str:
			if 'webm' not in str:
				print(f'[INFO {ltime}]:Obtuvimos un .webm, el usuario no especificó el sonido. recurrente. etiquetas de usuario: {str}')
				wr = rdl(str,pidfix(str))
		else:
			pass
	elif 'webm' not in wr:
		print(f'[INFO {ltime}]: No es un webm, no te recuses.')
	return wr
    
status = cycle(
    ['Wtf?','Made by ! slvqm#1869', 'Omg soy un bot', 'Furrys 3000', 'When haces un momazo'])
    
mainshop = [{"name":"Watch","price":100,"description":"Time"},
            {"name":"Laptop","price":1000,"description":"Work"},
            {"name":"PC","price":10000,"description":"Gaming"},
            {"name":"Ferrari","price":99999,"description":"Sports Car"}]

            
def get_prefix(client, message):
    with open('prefixes.json', 'r') as file:
        prefixes = json.load(file)

    if str(message.guild.id) in prefixes:
        return prefixes[str(message.guild.id)]
    else:
        prefixes[str(message.guild.id)] = "d-"
        with open('prefixes.json', 'w') as file:
            json.dump(prefixes, file, indent=2)
        return
        
client = commands.Bot(command_prefix= get_prefix,  owner_id=956924198473859092)
DiscordComponents(client)
client.remove_command('help')

@client.event
async def on_ready():
    change_status.start()
    print('Bot is ready')

@tasks.loop(seconds=60)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))
    

@client.command()
async def vtc(ctx,*,message):
   emb=discord.Embed(title="Votacion", description=f"{message}")
   msg=await ctx.channel.send(embed=emb)
   await ctx.message.delete()
   await msg.add_reaction("👍")
   await msg.add_reaction("👎")

@client.command(helpinfo='ping owo')
async def ping(ctx):
    await ctx.send("🏓 Pong: **{}ms**".format(round(client.latency * 1000, 2)))

@client.command()
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member, *, reason=None):
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="Muted")

    if not mutedRole:
        mutedRole = await guild.create_role(name="Muted")

        for channel in guild.channels:
            await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)

    await member.add_roles(mutedRole, reason=reason)
    await ctx.send(f"Muteado por {member.mention} {reason}")
    await member.send(f"Fuiste muteado de {guild.name} por {reason}")


@client.command()
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: discord.Member):
    mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

    await member.remove_roles(mutedRole)
    await ctx.send(f"Unmuted {member.mention}")
    await member.send(f"Fuiste desmuteado de {ctx.guild.name})")

@client.command()
async def echo(ctx, *args):
    await ctx.send('{} : {}'.format(len(args), ', '.join(args)))

@client.command()
@commands.is_owner()
async def terminar(ctx):
    await ctx.send("Terminando...")
    await client.logout()

@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def purge(ctx, limit: int):
        await ctx.channel.purge(limit=limit)
        await ctx.message.delete()
        await ctx.send('Purge by {}'.format(ctx.author.mention))
        time.sleep(4)
        await ctx.message.delete()

@client.command(helpinfo='Shows MC account info, skin and username history', aliases=['skin', 'mc'])
async def minecraft(ctx, username='Shrek'):
    uuid = requests.get('https://api.mojang.com/users/profiles/minecraft/{}'
                        .format(username)).json()['id']

    url = json.loads(base64.b64decode(requests.get(
        'https://sessionserver.mojang.com/session/minecraft/profile/{}'
        .format(uuid)).json()['properties'][0]['value'])
                     .decode('utf-8'))['textures']['SKIN']['url']
    
    names = requests.get('https://api.mojang.com/user/profiles/{}/names'
                        .format(uuid)).json()
    history = "**Name History:**\n"
    for name in reversed(names):
        history += name['name']+"\n"

    await ctx.send('**Username: `{}`**\n**Skin: {}**\n**UUID: {}**'.format(username, url, uuid))
    await ctx.send(history)

@client.command()
async def emojify(ctx,*, text):
    emojis =[]
    for s in text:
        if s.isdecimal():
            num2emo = {'0':'zero','1':'one','2':'two',
            '3':'three','4':'four','5':'five',
            '6':'six','7':'seven','8':'eight','9':'nine'}
            emojis.append(f':{num2emo.get(s)}:')
        elif s.isalpha():
            emojis.append(f':regional_indicator_{s}:')
        else:
            emojis.append(s)
    await ctx.send(''.join(emojis))

@client.command(helpinfo='', aliases=['server', 'num', 'count'])
async def servers(ctx):
    servers = client.guilds
    servers.sort(key=lambda x: x.member_count, reverse=True)
    await ctx.send('***Top servers by Prxv Bot:***')
    for x in servers[:5]:
        await ctx.send('**{}**, **{}** Miembros, {} region, Owned by <@{}>, Createdo por {}\n{}'.format(x.name, x.member_count, x.region, x.owner_id, x.created_at, x.icon_url_as(format='png',size=32)))
    y = 0
    for x in client.guilds:
        y += x.member_count
    await ctx.send('**Numero total de users:** ***{}***!\n**Numero total de servers:** ***{}***!'.format(y, len(client.guilds)))

@client.command(helpinfo='Searches the web (or images if typed first)', aliases=['search'])
async def google(ctx, *, searchquery: str):
    '''
    Should be a group in the future
    Googles searchquery, or images if you specified that
    '''
    searchquerylower = searchquery.lower()
    if searchquerylower.startswith('images '):
        await ctx.send('<https://www.google.com/search?tbm=isch&q={}>'
                       .format(urllib.parse.quote_plus(searchquery[7:])))
    else:
        await ctx.send('<https://www.google.com/search?q={}>'
                       .format(urllib.parse.quote_plus(searchquery)))

@client.command(helpinfo='Let me Google that for you')
async def lmgtfy(ctx, *, searchquery: str):
    '''
    Sarcastic site for helping googling
    '''
    await ctx.send('<https://lmgtfy.com/?iie=1&q={}>'
                   .format(urllib.parse.quote_plus(searchquery)))
        
@client.command()
async def encrypt(ctx):
    user = ctx.author
    await user.send("Introduce el mensaje.")
    response = await client.wait_for('message') # , check=message_check(channel=ctx.author.dm_channel))
    message = response.content
    encoded = message.encode()
    key = Fernet.generate_key()
    f = Fernet(key)
    encrypted = f.encrypt(encoded)
    await ctx.author.send("La key de encriptacion es:")
    await ctx.author.send(encrypted.decode())
    await ctx.author.send("La key para decriptar es:")
    await ctx.author.send(key.decode())


@client.command()
async def decrypt(ctx):
    user = ctx.author
    await user.send("Porfavor, introduce el mensaje encriptado.")
    response = await client.wait_for('message')
    encrypted = response.content.encode()
    await user.send("Introduce la key:")
    response = await client.wait_for('message') 
    key = response.content.encode()
    f = Fernet(key)
    decrypted = f.decrypt(encrypted)
    decoded = decrypted.decode()
    await user.send(decoded)
    print(decoded)

#----------------------------------------------------------------------------------


player1 = ""
player2 = ""
turn = ""
gameOver = True

board = []

winningConditions = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]

@client.command()
async def tictactoe(ctx, p1: discord.Member, p2: discord.Member):
    global count
    global player1
    global player2
    global turn
    global gameOver

    if gameOver:
        global board
        board = [":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:"]
        turn = ""
        gameOver = False
        count = 0

        player1 = p1
        player2 = p2

        # print the board
        line = ""
        for x in range(len(board)):
            if x == 2 or x == 5 or x == 8:
                line += " " + board[x]
                await ctx.send(line)
                line = ""
            else:
                line += " " + board[x]

        # determine who goes first
        num = random.randint(1, 2)
        if num == 1:
            turn = player1
            await ctx.send("It is <@" + str(player1.id) + ">'s turn.")
        elif num == 2:
            turn = player2
            await ctx.send("It is <@" + str(player2.id) + ">'s turn.")
    else:
        await ctx.send("un juego ya está en progreso! Termínalo antes de empezar uno nuevo.")

@client.command()
async def place(ctx, pos: int):
    global turn
    global player1
    global player2
    global board
    global count
    global gameOver

    if not gameOver:
        mark = ""
        if turn == ctx.author:
            if turn == player1:
                mark = ":regional_indicator_x:"
            elif turn == player2:
                mark = ":o2:"
            if 0 < pos < 10 and board[pos - 1] == ":white_large_square:" :
                board[pos - 1] = mark
                count += 1

                # print the board
                line = ""
                for x in range(len(board)):
                    if x == 2 or x == 5 or x == 8:
                        line += " " + board[x]
                        await ctx.send(line)
                        line = ""
                    else:
                        line += " " + board[x]

                checkWinner(winningConditions, mark)
                print(count)
                if gameOver == True:
                    await ctx.send(mark + " wins!")
                elif count >= 9:
                    gameOver = True
                    await ctx.send("It's a tie!")

                # switch turns
                if turn == player1:
                    turn = player2
                elif turn == player2:
                    turn = player1
            else:
                await ctx.send("Asegúrese de elegir un número entero entre 1 y 9 (ambos inclusive) y un mosaico sin marcar.")
        else:
            await ctx.send("no es tu turno.")
    else:
        await ctx.send("porfavor inicia usando p-tictactoe.")


def checkWinner(winningConditions, mark):
    global gameOver
    for condition in winningConditions:
        if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
            gameOver = True

@tictactoe.error
async def tictactoe_error(ctx, error):
    print(error)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Mencione 2 jugadores para este comando.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Por favor asegúrate de mencionar / hacer ping a los jugadores (ie. <@688534433879556134>).")


@client.command(aliases=["ltc"]) 
async def latency(ctx):
	if int(round(client.latency * 1000)) <= 50:
		color=0x000000
	elif int(round(client.latency * 1000)) <= 100:
		color=0x00FF00
	elif int(round(client.latency * 1000)) <= 300:
		color=0x00FFFF
	else:
		color=0xFF0000
	if ctx.message.content.lower().startswith(f"{client.command_prefix}latency"):
		title="Latency"
	elif ctx.message.content.lower().startswith(f"{client.command_prefix}ping"):
		title="Ping"
	else:
		title="Latency"
	hehe = discord.Embed(title=title,description=f"Latency : {str(round(client.latency * 1000))}ms", color=color)
	await ctx.send(embed=hehe)
    
snipe_message_author = {}
snipe_message_content = {}

@client.event
async def on_message_delete(message):
     snipe_message_author[message.channel.id] = message.author
     snipe_message_content[message.channel.id] = message.content
     await sleep(60)
     del snipe_message_author[message.channel.id]
     del snipe_message_content[message.channel.id]

@client.command(name = 'snipe')
async def snipe(ctx):
    channel = ctx.channel
    try: 
        em = discord.Embed(name = f"Last deleted message in #{channel.name}", description = snipe_message_content[channel.id])
        em.set_footer(text = f"This message was sent by {snipe_message_author[channel.id]}")
        await ctx.send(embed = em)
    except KeyError: 
        await ctx.send(f"There are no recently deleted messages in #{channel.name}")
        
#------------------------------------------------

@client.command(pass_context=True)
async def bal(ctx):
    await open_account(ctx.author)

    user = ctx.author

    users = await get_bank_data()

    wallet_amt = users[str(user.id)]["wallet"]

    bank_amt = users[str(user.id)]["bank"]

    embed = discord.Embed(title=f"{ctx.author.name}'s balance", color=0xFF69B4)

    embed.add_field(name= "Wallet Balance", value= wallet_amt,inline = False)
    embed.add_field(name= "Bank Balance", value= bank_amt,inline = False)

    await ctx.send(embed = embed)

    
@client.command(pass_context=True)
async def beg(ctx):
    await open_account(ctx.author)

    user = ctx.author

    users = await get_bank_data()

    


    earnings = random.randrange(101)

    await ctx.send(f"**Toma {earnings} coins para vos**")

    users[str(user.id)]["wallet"] += earnings

    with open("mainbank.json", "w") as f:
        json.dump(users,f)

@client.command(pass_context=True)
@commands.cooldown(rate=1, per=120)
async def hack(ctx):
    await open_account(ctx.author)

    user = ctx.author

    users = await get_bank_data()

    


    earnings = random.randrange(101)

    await ctx.send(f"**Haz robado {earnings} coins!!**")

    users[str(user.id)]["wallet"] += earnings

    with open("mainbank.json", "w") as f:
        json.dump(users,f)
        
@client.command(pass_context=True)
async def withdraw(ctx,amount = None):
    await open_account(ctx.author)
    if amount == None:
        await ctx.send("**Porfavor ingrese la cantidad de dinero**")
        return

    bal = await update_bank(ctx.author)

    amount = int(amount)

    if amount>bal[1]:
        await ctx.send("**No tienes esa cantidad de dinero!!**")
        return
    if amount<0:
        await ctx.send("**La cantidad debe ser positiva**")
        return

    await update_bank(ctx.author,amount)
    await update_bank(ctx.author,-1*amount,"bank")

    await ctx.send(f"**tu retiraste {amount} coins!**")

@client.command(pass_context=True)
async def dep(ctx,amount = None):
    await open_account(ctx.author)
    if amount == None:
        await ctx.send("**Porfavor ingrese la cantidad de dinero**")
        return

    bal = await update_bank(ctx.author)

    amount = int(amount)

    if amount>bal[0]:
        await ctx.send("**No tienes esa cantidad de dinero!!!**")
        return
    if amount<0:
        await ctx.send("**La cantidad debe ser positiva**")
        return

    await update_bank(ctx.author,-1*amount)
    await update_bank(ctx.author,amount,"bank")

    await ctx.send(f"**Tu depositaste {amount} coins!**")


@client.command(pass_context=True)
async def pay(ctx,member: discord.Member, amount = None):
    await open_account(ctx.author)
    await open_account(member)
    if amount == None:
        await ctx.send("**Porfavor ingresa la cantidad**")
        return

    bal = await update_bank(ctx.author)

    if amount == "all":
        amount = bal[0]




    amount = int(amount)

    if amount>bal[1]:
        await ctx.send("**No tienes esa cantidad de dinero!**")
        return
    if amount<0:
        await ctx.send("**La cantidad debe ser positiva**")
        return

    await update_bank(ctx.author,-1*amount,"bank")
    await update_bank(member,amount,"bank")

    await ctx.send(f"**tu pagaste {amount} coins!**")

@client.command(pass_context=True)
async def rob(ctx,member: discord.Member):
    await open_account(ctx.author)
    await open_account(member)
   
    bal = await update_bank(member)

    

    if bal[0]<100:
        await ctx.send("Que no vale la pena")
        return

    earnings = random.randrange(0, bal[0])
  

    await update_bank(ctx.author,earnings)
    await update_bank(member,-1*earnings)

    await ctx.send(f"usted robó y consiguió {earnings} coins!")


@client.command(pass_context=True)
async def slots(ctx, amount = None):
    await open_account(ctx.author)
    if amount == None:
        await ctx.send("Por favor ingrese la cantidad")
        return

    bal = await update_bank(ctx.author)

    amount = int(amount)

    if amount>bal[0]:
        await ctx.send("¡No tienes tanto dinero!!")
        return
    if amount<0:
        await ctx.send("La cantidad debe ser positiva")
        return

    final = []
    for i in range(3):
        a = random.choice([":poop:", ":smile:", ":cherry_blossom:"])

        final.append(a)

    await ctx.send(str(final))

    if final[0] == final[1] or final[0] == final[2] or final[2] == final[1]:
         await update_bank(ctx.author,2*amount)
         await ctx.send("**tu ganaste!**")

    else:
        await update_bank(ctx.author,-1*amount)
        await ctx.send("**tu perdiste!**")


async def open_account(user):

    users = await get_bank_data()
    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = 0
        users[str(user.id)]["bank"] = 0

    with open("mainbank.json", "w") as f:
        json.dump(users,f)
    return True


async def get_bank_data():
    with open("mainbank.json", "r") as f:
        users = json.load(f)

    return users



async def update_bank(user, change=0,mode = 'wallet'):

    users = await get_bank_data()

    users[str(user.id)][mode] += change

    with open("mainbank.json", "w") as f:
        json.dump(users,f)

    bal = users[str(user.id)]["wallet"],users[str(user.id)]["bank"]


    return bal


    await ctx.send(f"Te he concedido tu petición, {author}", embed=embed)
 
@client.command()
async def shop(ctx):
    em = discord.Embed(title = "Shop")

    for item in mainshop:
        name = item["name"]
        price = item["price"]
        desc = item["description"]
        em.add_field(name = name, value = f"${price} | {desc}")

    await ctx.send(embed = em)

@client.command()
async def buy(ctx,item,amount = 1):
    await open_account(ctx.author)

    res = await buy_this(ctx.author,item,amount)

    if not res[0]:
        if res[1]==1:
            await ctx.send("Ese objeto no está ahi!")
            return
        if res[1]==2:
            await ctx.send(f"No tienes suficiente dinero en tu billetera para comprar {amount} {item}")
            return


    await ctx.send(f"acabas de comprar {amount} {item}")

@client.command()
async def bag(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()

    try:
        bag = users[str(user.id)]["bag"]
    except:
        bag = []


    em = discord.Embed(title = "Bag")
    for item in bag:
        name = item["item"]
        amount = item["amount"]

        em.add_field(name = name, value = amount)    

    await ctx.send(embed = em)


async def buy_this(user,item_name,amount):
    item_name = item_name.lower()
    name_ = None
    for item in mainshop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            price = item["price"]
            break

    if name_ == None:
        return [False,1]

    cost = price*amount

    users = await get_bank_data()

    bal = await update_bank(user)

    if bal[0]<cost:
        return [False,2]


    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            if n == item_name:
                old_amt = thing["amount"]
                new_amt = old_amt + amount
                users[str(user.id)]["bag"][index]["amount"] = new_amt
                t = 1
                break
            index+=1 
        if t == None:
            obj = {"item":item_name , "amount" : amount}
            users[str(user.id)]["bag"].append(obj)
    except:
        obj = {"item":item_name , "amount" : amount}
        users[str(user.id)]["bag"] = [obj]        

    with open("mainbank.json","w") as f:
        json.dump(users,f)

    await update_bank(user,cost*-1,"wallet")

    return [True,"Worked"]
    

@client.command()
async def sell(ctx,item,amount = 1):
    await open_account(ctx.author)

    res = await sell_this(ctx.author,item,amount)

    if not res[0]:
        if res[1]==1:
            await ctx.send("That Object isn't there!")
            return
        if res[1]==2:
            await ctx.send(f"no tienes {amount} {item} en tu mochila.")
            return
        if res[1]==3:
            await ctx.send(f"no tienes {item} en tu mochila.")
            return

    await ctx.send(f"acabas de vender {amount} {item}.")

async def sell_this(user,item_name,amount,price = None):
    item_name = item_name.lower()
    name_ = None
    for item in mainshop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            if price==None:
                price = 0.7* item["price"]
            break

    if name_ == None:
        return [False,1]

    cost = price*amount

    users = await get_bank_data()

    bal = await update_bank(user)


    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            if n == item_name:
                old_amt = thing["amount"]
                new_amt = old_amt - amount
                if new_amt < 0:
                    return [False,2]
                users[str(user.id)]["bag"][index]["amount"] = new_amt
                t = 1
                break
            index+=1 
        if t == None:
            return [False,3]
    except:
        return [False,3]    

    with open("mainbank.json","w") as f:
        json.dump(users,f)

    await update_bank(user,cost,"wallet")

    return [True,"Worked"]


@client.command(aliases = ["lb"])
async def leaderboard(ctx,x = 1):
    users = await get_bank_data()
    leader_board = {}
    total = []
    for user in users:
        name = int(user)
        total_amount = users[user]["wallet"] + users[user]["bank"]
        leader_board[total_amount] = name
        total.append(total_amount)

    total = sorted(total,reverse=True)    

    em = discord.Embed(title = f"Top {x} gente mas rica" , description = "Testo se decide sobre la base del dinero bruto en el banco y la billetera",color = discord.Color(0xfa43ee))
    index = 1
    for amt in total:
        id_ = leader_board[amt]
        member = client.get_user(id_)
        name = member.name
        em.add_field(name = f"{index}. {name}" , value = f"{amt}",  inline = False)
        if index == x:
            break
        else:
            index += 1

    await ctx.send(embed = em)


async def open_account(user):

    users = await get_bank_data()

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = 0
        users[str(user.id)]["bank"] = 0

    with open('mainbank.json','w') as f:
        json.dump(users,f)

    return True


async def get_bank_data():
    with open('mainbank.json','r') as f:
        users = json.load(f)

    return users


async def update_bank(user,change=0,mode = 'wallet'):
    users = await get_bank_data()

    users[str(user.id)][mode] += change

    with open('mainbank.json','w') as f:
        json.dump(users,f)
    bal = users[str(user.id)]['wallet'],users[str(user.id)]['bank']
    return bal
    
@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def changeprefix(ctx, prefix):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = prefix

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

    await ctx.send(f'Prefix changed to: {prefix}')
    name=f'{prefix}BotBot'
 
@client.event
async def on_member_join(member):
    with open('users.json', 'r') as f:
        users = json.load(f)

    await update_data(users, member)

    with open('users.json', 'w') as f:
        json.dump(users, f)


@client.event
async def on_message(message):
    if message.author.bot == False:
        with open('users.json', 'r') as f:
            users = json.load(f)

        await update_data(users, message.author)
        await add_experience(users, message.author, 5)
        await level_up(users, message.author, message)

        with open('users.json', 'w') as f:
            json.dump(users, f)

    await client.process_commands(message)


async def update_data(users, user):
    if not f'{user.id}' in users:
        users[f'{user.id}'] = {}
        users[f'{user.id}']['experience'] = 0
        users[f'{user.id}']['level'] = 1


async def add_experience(users, user, exp):
    users[f'{user.id}']['experience'] += exp


async def level_up(users, user, message):
    with open('levels.json', 'r') as g:
        levels = json.load(g)
    experience = users[f'{user.id}']['experience']
    lvl_start = users[f'{user.id}']['level']
    lvl_end = int(experience ** (1 / 4))
    if lvl_start < lvl_end:
        await message.channel.send(f'{user.mention} Subes de nivel! {lvl_end}')
        users[f'{user.id}']['level'] = lvl_end

@client.command()
async def level(ctx, member: discord.Member = None):
    if not member:
        id = ctx.message.author.id
        with open('users.json', 'r') as f:
            users = json.load(f)
        lvl = users[str(id)]['level']
        await ctx.send(f'Eres nivel {lvl}!')
    else:
        id = member.id
        with open('users.json', 'r') as f:
            users = json.load(f)
        lvl = users[str(id)]['level']
        await ctx.send(f'{member} Tu nivel es {lvl}!')

@client.command()
async def avatar(ctx, *,  avamember : discord.Member=None):
    userAvatarUrl = avamember.avatar_url
    await ctx.send(userAvatarUrl)


@client.command()
async def createemoji(ctx, url: str, *, name):
	guild = ctx.guild
	if ctx.author.guild_permissions.manage_emojis:
		async with aiohttp.ClientSession() as ses:
			async with ses.get(url) as r:
				
				try:
					img_or_gif = BytesIO(await r.read())
					b_value = img_or_gif.getvalue()
					if r.status in range(200, 299):
						emoji = await guild.create_custom_emoji(image=b_value, name=name)
						await ctx.send(f'Emoji creado con éxito: <:{name}:{emoji.id}>')
						await ses.close()
					else:
						await ctx.send(f'Error al realizar la solicitud | {r.status} respuesta.')
						await ses.close()
						
				except discord.HTTPException:
					await ctx.send('File size is too big!')

@client.command()
async def deleteemoji(ctx, emoji: discord.Emoji):
	guild = ctx.guild
	if ctx.author.guild_permissions.manage_emojis:
		await ctx.send(f'Eliminado con éxito (o no): {emoji}')
		await emoji.delete()

@commands.command()
async def on_message(self, message: discord.Message):      
    if message.author.bot:
        return
        
    else:
        if message.channel == message.author.dm_channel:
            time_difference = (datetime.utcnow() - self.last_timeStamp).total_seconds()

            if time_difference < 5:
                    return await message.channel.send("You are on cooldown!")
                
            self.channel_id = 972736122876727347
            self.modmail_channel = self.bot.get_channel(self.channel_id)
            embed = discord.Embed(
                title = f"Modmail From `{message.author}`", 
                description = f"{message.content}", 
                color = random
            )
            if message.attachments:
                embed.set_image(url=message.attachments[0].url)
            embed.set_footer(text=f'ID: {message.author.id}')

            await self.modmail_channel.send(embed=embed)
            await message.channel.send('Tu mensaje ha sido enviado!', delete_after = 7)

@client.command()
async def hello(ctx):
    await ctx.send("hello", components = [
        [Button(label="Hi", style="3", emoji = "🥴", custom_id="button1"), Button(label="Bye", style="4", emoji = "😔", custom_id="button2")]
        ])
    interaction = await client.wait_for("button_click", check = lambda i: i.custom_id == "button1")
    await interaction.send(content = "Button clicked!", ephemeral=False)      

#------------------

@client.command(name="whois")
async def whois(ctx,user:discord.Member=None):

    if user==None:
        user=ctx.author

    rlist = []
    for role in user.roles:
      if role.name != "@everyone":
        rlist.append(role.mention)

    b = ", ".join(rlist)


    embed = discord.Embed(colour=user.color,timestamp=ctx.message.created_at)

    embed.set_author(name=f"User Info - {user}"),
    embed.set_thumbnail(url=user.avatar_url),
    embed.set_footer(text=f'Solicitado por - {ctx.author}',
  icon_url=ctx.author.avatar_url)

    embed.add_field(name='ID:',value=user.id,inline=False)
    embed.add_field(name='Name:',value=user.display_name,inline=False)

    embed.add_field(name='Creado en:',value=user.created_at,inline=False)
    embed.add_field(name='Se unió a:',value=user.joined_at,inline=False)

  
 
    embed.add_field(name='Bot?',value=user.bot,inline=False)

    embed.add_field(name=f'Roles:({len(rlist)})',value=''.join([b]),inline=False)
    embed.add_field(name='Top Rol:',value=user.top_role.mention,inline=False)

    await ctx.send(embed=embed)
    
@client.command()
async def pato(ctx):
    embed = discord.Embed(title="Quack!", description=" ", color=0x176cd5)
    embed.set_image(url="https://random-d.uk/api/randomimg?t=1652145993164")
    await ctx.send(embed=embed)

@client.command()
async def porn(ctx,*arg):
	answer = ''
	arg = str(arg)
	arg = arg.replace(',','')
	arg = arg.replace('(','')
	arg = arg.replace(')','')
	arg = arg.replace("'",'')
	print(f'[DEBUG {ltime}]: arg is now {arg}')
	waitone = await ctx.send("***:desktop: ¡Estamos votando Rule34! por favor espere unos segundos.***")
	newint = pidfix(arg)
	if newint > 2000:
		newint = 2000
		answer = rdl(arg,random.randint(1,newint))
	if newint > 1:

		answer = rdl(arg,random.randint(1,newint))
	elif newint < 1:
		if newint == 0:
			answer = rdl(arg,0)
		elif newint != 0:
			answer = rdl(arg,1)
   
	if 'webm' in answer:
		await waitone.delete
		await ctx.send(answer)
	elif 'webm' not in answer:
		embed = discord.Embed(title=f'Rule34: {arg}',color=ctx.author.color)
		embed.set_author(name=f'{ctx.author.display_name}',icon_url=f'{ctx.author.avatar_url}')
		embed.set_thumbnail(url='https://rule34.paheal.net/themes/rule34v2/rule34_logo_top.png')
		embed.set_image(url=f'{answer}')
		embed.set_footer(text=" ",icon_url='https://cdn.discordapp.com/avatars/268211297332625428/e5e43e26d4749c96b48a9465ff564ed2.png?size=128')
		waitone.delete
		await ctx.send(embed = embed)


@client.event
async def on_raw_reaction_add(payload):

    if payload.member.bot:
        pass

    else:
        with open('reactrole.json') as react_file:
            data = json.load(react_file)
            for x in data:
                if x['message_id'] == payload.message_id:
                                                          
                    if x['emoji'] == payload.emoji.name:
                        role = discord.utils.get(client.get_guild(
                            payload.guild_id).roles, id=x['role_id'])

                    await payload.member.add_roles(role)


@client.event
async def on_raw_reaction_remove(payload):

    with open('reactrole.json') as react_file:
        data = json.load(react_file)
        for x in data:

            if x['message_id'] == payload.message_id:
                if x['emoji'] == payload.emoji.name:
                    role = discord.utils.get(client.get_guild(
                        payload.guild_id).roles, id=x['role_id'])

                
                await client.get_guild(payload.guild_id).get_member(payload.user_id).remove_roles(role)
                    
@client.command()
@commands.has_permissions(administrator=True, manage_roles=True)
async def reactrole(ctx, emoji, role: discord.Role, *, message):

    emb = discord.Embed(description=message)
    msg = await ctx.channel.send(embed=emb)
    await msg.add_reaction(emoji)

    with open('reactrole.json') as json_file:
        data = json.load(json_file)

        new_react_role = {'role_name': role.name, 
        'role_id': role.id,
        'emoji': emoji,
        'message_id': msg.id}

        data.append(new_react_role)

    with open('reactrole.json', 'w') as f:
        json.dump(data, f, indent=4)
        
@client.command()
async def menu(ctx):
    page1 = discord.Embed (
        title = 'Diversion 1/3',
        description = f'**vtc** | Realiza una votacion con este comando \n**avatar** | etiqueta a un usuario para ver su avatar \n **google** | Busca algo por google \n **lmgtfy** | Busca una sarcastica respuesta\n **emojify** | Transforma de texto a emojis \n **pato** | Haz aparecer un pato \n **minecraft** | Busca informacion sobre la cuenta de alguien premiun \n **porn** | Selecciona una categoria con este comando y te dare un resultado | \n **snipe** | Ve si algun mensaje fue borrado \n **whois** | Obten inforamcion de un usuario etiquetandolo \n **tictactoe** | Etiquetate a vos y a la persona con la que quieras jugar \n **place** | con este comando selecciona un emoji, de 1 a 9 para marcarlo y espera tu turno. \n  afk | Pon un estado de afk \n **punch** | Golpea a alguien con este comando etiquetadolo \n **shot** | Golpea a la persona que etiquetaste con esto \n **kiss** | Besa a quien hayas etiquetado ',
        colour = discord.Colour.red()
    )
    page2 = discord.Embed (
        title = 'Moderacion 2/3',
        description = '**mute** | Mutea a un usuario \n **unmute** | Desmutea al usuario \n **ban** | Banea a un usuario con este comando \n **reactrole**  | Funcion de autoroles <emoji>  <role> <textto> \n **createemoji** | Crea un emoji de esta manera createemoji <link de la imagen> <nombre> ',
        colour = discord.Colour.red()
    )
    page3 = discord.Embed (
        title = 'Economia 3/3',
        description = '**bal** | Ve el balance de cuenta \n **beg** | Recibe coins \n **bag** | Ve los items que tienes en tu mochila \n **buy** | Compra algun objeto que estan en "shop" \n **shop** | Ve la tienda \n **dep** | Deposita en tu cuenta y evita ser robado \n **sell** | Vende lo que compraste \n **hack** | Hackea y gana dinero \n **slots** Selecciona el dinero que quieras jugar y veamos que te toca. \n **pay** | Transfierele dinero a otro usuario. \n **withdraw** | Saca dinero de tu banco',
        colour = discord.Colour.red()

    )
    
    pages = [page1, page2, page3]

    message = await ctx.send(embed = page1)
    await message.add_reaction('⏮')
    await message.add_reaction('◀')
    await message.add_reaction('▶')
    await message.add_reaction('⏭')

    def check(reaction, user):
        return user == ctx.author

    i = 0
    reaction = None

    while True:
        if str(reaction) == '⏮':
            i = 0
            await message.edit(embed = pages[i])
        elif str(reaction) == '◀':
            if i > 0:
                i -= 1
                await message.edit(embed = pages[i])
        elif str(reaction) == '▶':
            if i < 2:
                i += 1
                await message.edit(embed = pages[i])
        elif str(reaction) == '⏭':
            i = 2
            await message.edit(embed = pages[i])
        
        try:
            reaction, user = await client.wait_for('reaction_add', timeout = 30.0, check = check)
            await message.remove_reaction(reaction, user)
        except:
            break

    await message.clear_reactions()

@client.command()
async def afk(ctx, mins):
    current_nick = ctx.author.nick
    await ctx.send(f"{ctx.author.mention} esta afk por {mins} minutos")
    await ctx.author.edit(nick=f"{ctx.author.name} [AFK]")

    counter = 0
    while counter <= int(mins):
        counter += 1
        await asyncio.sleep(60)

        if counter == int(mins):
            await ctx.author.edit(nick=current_nick)
            await ctx.send(f"{ctx.author.mention} no esta afk")
            break    

@client.command()
async def ship(ctx, user_1 : discord.Member, user_2 : discord.Member):
    await ctx.send(f"{user_1.mention} y {user_2.mention} hacen linda pareja ")


punch_gifs =['https://i.pinimg.com/originals/2b/5d/7b/2b5d7bb1dd4a8e64869c33499c409582.gif',
 'https://i.pinimg.com/originals/24/53/85/2453852df2d5f4644f8c7d9a8c1d1ff6.gif',
 'https://i.pinimg.com/originals/01/7a/21/017a21aedc18c37b96995acfbe5ebcda.gif',
 ]

punch_names = ['Te golpeo',
 'Golpeo a',
 'Le dio una paliza a',
 'Cago a piñas a',
 ]

@client.command()
async def punch(ctx, member : discord.Member):
    embed = discord.Embed(
          color=(discord.Colour.random()), 
          description = f"{ctx.author.mention} {(random.choice(punch_names))} {member})"
          
    )
    embed.set_image(url=(random.choice(punch_gifs)))
    
    await ctx.send(embed=embed)

shot_gifs =['Te golpeo',
'https://i.pinimg.com/originals/0d/ff/63/0dff63ddb1c91f4657a07372bf761e5d.gif',
'https://i.pinimg.com/originals/85/01/18/8501189152473f6bd7a6767d84159bd1.gif',
'https://i.pinimg.com/originals/6c/1c/bd/6c1cbd064bed81b88a1739e23f9b65d8.gif',
'https://i.pinimg.com/originals/a0/07/8b/a0078b401e72994d052af23c7f795f6b.gif',
]
shot_names =['Cago a tiros a',
'Disparo a',
'Le a disparado a',
]

@client.command()
async def shot(ctx, member : discord.Member):
    embed = discord.Embed(
          color=(discord.Colour.random()), 
          description = f"{ctx.author.mention} {(random.choice(shot_names))} {member})"
          
    )
    embed.set_image(url=(random.choice(shot_gifs)))
    
    await ctx.send(embed=embed)

kiss_gifs =['https://i.pinimg.com/originals/b2/0f/e0/b20fe027ba2f488d72d890ddc2b927ab.gif',
'https://i.pinimg.com/originals/07/5e/9d/075e9d0a559e7d85f5bb0da7ccad7d11.gif',
'https://i.pinimg.com/originals/2d/e7/6f/2de76fef28cf0eb8c2ea48bd36efba1d.gif',
]
kiss_names =['le dio un beso a',
'beso a',
]

@client.command()
async def kiss(ctx, member : discord.Member):
    embed = discord.Embed(
          color=(discord.Colour.random()), 
          description = f"{ctx.author.mention} {(random.choice(kiss_names))} {member})"
          
    )
    embed.set_image(url=(random.choice(kiss_gifs)))
    
    await ctx.send(embed=embed)  
	
client.run(BOT_TOKEN)

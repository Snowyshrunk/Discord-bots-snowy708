#!/usr/bin/python3
import discord
import datetime
import logging
import os
import sys
import paramiko
from random import randint, choice
from discord.ext import commands
from typing import Optional, Tuple
import openai
import emoji
from discord import option
import random
import time
from pathlib import Path
from datetime import datetime, timedelta
from discord.ext import commands, tasks
from discord.ui import Select, View
import json
import pytz

def blacklist():
    async def predicate(ctx: discord.ApplicationContext):
        file1= Path(__file__).parent / 'blacklist.txt'
        print("Blacklist loc:", file1)
        with open(file1, 'r') as f:
            print("Opened blacklist.")
            for line in f.readlines():
                line = line.strip()
                print("Read line: %r" % line)
                if line == str(ctx.user.id):
                    print("Line is equal to %s." % ctx.user.id)
                    print("Raising Permissions Error")
                    raise commands.MissingPermissions(["blacklist"])
        print("All checks seem fine for %s, returning True." % ctx.user.id)
        return True  # weren't in the file
    
    return commands.check(predicate)
def whitelist():
    async def predicate(ctx: discord.ApplicationContext):
        file1= Path(__file__).parent / 'whitelist.txt'
        print("whitelist loc:", file1)
        with open(file1, 'r') as f:
            print("Opened whitelist.")
            for line in f.readlines():
                line = line.strip()
                print("Read line: %r" % line)
                if line == str(ctx.user.id):
                    print("Line is equal to %s." % ctx.user.id)
                        
                    return True
        print("Raising Permissions Error")
        raise commands.MissingPermissions(['not white listed'])
    return commands.check(predicate)


def owner_or_admin():
    async def predicate(ctx: commands.Context):
        if ctx.author.guild_permissions.administrator or await ctx.bot.is_owner(ctx.author):
            return True
        raise commands.MissingPermissions(["administrator"])

    return commands.check(predicate)

intents = discord.Intents.default()
intents.message_content = (True)

bot = commands.Bot(commands.when_mentioned_or("s!"), intents=intents)

@bot.event
async def on_application_command_error(ctx: discord.ApplicationContext, error: Exception):
    loggchannel = int('REPLACE WITH CHANNEL ID')
    channel = bot.get_channel(loggchannel)
    if isinstance(error, commands.MissingPermissions):
        await channel.send(f'{bot.user} missing permissions error')
    await channel.send(f"{bot.user} experienced an error plz fix me")
    await channel.send(f"``` {str(error)} ```")
    raise error 

@bot.event
async def on_ready():
    #await bot.change_presence(status=discord.Status.online , activity=discord.Game("YOU"))
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Snowy mountains"))
    print(f"We have logged in as {bot.user}")
    print("in", len(bot.guilds), "guilds")
    print("guild names:", ", ".join((x.name for x in bot.guilds)))
    loggchannel = int('REPLACE WITH CHANNEL ID')
    channel = bot.get_channel(loggchannel)
    await channel.send(f'{bot.user} is now back online') 

@tasks.loop(seconds = 100)
async def myLoop():
    file2= Path(__file__).parent / 'assignment.json'
    print('loopstarted')
    curenttime=round(int(time.time()))
    print(curenttime)
    num = curenttime
    small = round((int(num) / 100))
    big = (small * 100)
    ct = big
    t = int(ct + 100) #+ 120 bigger num
    tt = int(ct) #-120 the smaller num
    file= Path(__file__).parent / 'assinment.txt'
    with open(file, 'r') as f:
        print("Begin iteration")
        for line in f.readlines():
            userid, user, due, name, who, info, guild_id, channel_id = line.split('%')
            num=due
            small = round((int(num) / 100))
            du = (small * 100)
            print(du)
            print(time.time())
            w1 = int(du) - 604800
            d3 = int(du) - 259200
            d1 = int(du) - 86400
            h3 = int(du) - 4200
            h1 = int(du) - 3600
            due2 = ('<t:'+str(due)+':R>')
            f = open(file2, "r")
            json_read = f.read() # read json back to var
            ids_read = json.loads(json_read) # convert json to dict
            f.close()
            print(str(json_read))
            read = str(json_read)
            print('guild id =', guild_id)
            #print(read.keys())
            server_id = str(guild_id)
            print(guild_id)
            print('awating ready')
            await bot.wait_until_ready()
            print('ready')
            logcheck = 0
            if server_id in read:
                print('guild id found')
                data = json.load(open(file2))
                channel_id2 = data[guild_id]
                channel = bot.get_channel(int(channel_id2))
                print('channel found from guild id')       
            else:
                channel = bot.get_channel(int(channel_id))
                print('server not set up')

            if channel is None:
                print('channel not found')
                print('server not set up')
                botlog = int('REPLACE WITH CHANNEL ID')
                channel = bot.get_channel(botlog)
                if channel is None:
                    channel = bot.fetch_channel(int('REPLACE WITH CHANNEL ID'))
                logcheck = logcheck + 1
                print('sent to log')

            if du in range(tt, t):
                print('event1')
                embed = discord.Embed(
                title='Assignment Reminder',
                description=name+'\n Info:'+info,
                color=discord.Colour.purple(), # not to future self change coulder to change coler bar on embed
                )
                embed.add_field(name="Who", value=who)
                embed.add_field(name="Time Due", value=due2, inline=True)
                embed.set_author(name=user, icon_url="https://cdn.discordapp.com/avatars/1161697414013534378/bd878019678d909440dfa117aa89a813.png?size=2048")
                await channel.send(who)
                await channel.send("Assignment due NOW", embed=embed)#check beofre send out
                if 0 < logcheck:
                    embed = discord.Embed(
                    title='Channel not found',
                    description=name+'Bot was unable to find a channel to send the reminder to\n *(defalting to this channel untill fixed)*'+info,
                    color=discord.Colour.purple(),)
                    embed.add_field(name="Original Channel", value='original channel was unable to be found this could have been caused by the channel being deleted or the Bot is unable to view the channel')
                    embed.add_field(name="Server not set up", value='The server has not been set up to send reminders to a defalt channel\nrun the command /choose_channel in the channel you want to use as the defalt channel to set this up')
                    embed.set_author(name=bot.user, icon_url="https://cdn.discordapp.com/avatars/1161697414013534378/bd878019678d909440dfa117aa89a813.png?size=2048")
                    print('log')
                    await channel.send(embed=embed)
                else:
                    print('no log')

            elif w1 in range(tt, t):
                print('event2')
                embed = discord.Embed(
                title='Assignment Reminder',
                description=name+'\n Info:'+info,
                color=discord.Colour.purple(), # not to future self change coulder to change coler bar on embed
                )
                embed.add_field(name="Who", value=who)
                embed.add_field(name="Time Due", value=due2, inline=True)
                embed.set_author(name=user, icon_url="https://cdn.discordapp.com/avatars/1161697414013534378/bd878019678d909440dfa117aa89a813.png?size=2048")
                await channel.send(who)
                await channel.send("Assignment due in 1 week", embed=embed)#check beofre send out
                if 0 < logcheck:
                    embed = discord.Embed(
                    title='Channel not found',
                    description=name+'Bot was unable to find a channel to send the reminder to\n *(defalting to this channel untill fixed)*'+info,
                    color=discord.Colour.purple(),)
                    embed.add_field(name="Original Channel", value='original channel was unable to be found this could have been caused by the channel being deleted or the Bot is unable to view the channel')
                    embed.add_field(name="Server not set up", value='The server has not been set up to send reminders to a defalt channel\nrun the command /choose_channel in the channel you want to use as the defalt channel to set this up')
                    embed.set_author(name=bot.user, icon_url="https://cdn.discordapp.com/avatars/1161697414013534378/bd878019678d909440dfa117aa89a813.png?size=2048")
                    embedcheck = embed=embed
                    print('log')
                    await channel.send(embed=embed)
                else:
                    print('no log')

            elif d3 in range(tt, t):
                print('event3')
                embed = discord.Embed(
                title='Assignment Reminder',
                description=name+'\n Info:'+info,
                color=discord.Colour.purple(), # not to future self change coulder to change coler bar on embed
                )
                embed.add_field(name="Who", value=who)
                embed.add_field(name="Time Due", value=due2, inline=True)
                embed.set_author(name=user, icon_url="https://cdn.discordapp.com/avatars/1161697414013534378/bd878019678d909440dfa117aa89a813.png?size=2048")
                await channel.send(who)
                await channel.send("Assignment due in 3 days", embed=embed)#check beofre send out
                if 0 < logcheck:
                    embed = discord.Embed(
                    title='Channel not found',
                    description=name+'Bot was unable to find a channel to send the reminder to\n *(defalting to this channel untill fixed)*'+info,
                    color=discord.Colour.purple(),)
                    embed.add_field(name="Original Channel", value='original channel was unable to be found this could have been caused by the channel being deleted or the Bot is unable to view the channel')
                    embed.add_field(name="Server not set up", value='The server has not been set up to send reminders to a defalt channel\nrun the command /choose_channel in the channel you want to use as the defalt channel to set this up')
                    embed.set_author(name=bot.user, icon_url="https://cdn.discordapp.com/avatars/1161697414013534378/bd878019678d909440dfa117aa89a813.png?size=2048")
                    embedcheck = embed=embed
                    print('log')
                    await channel.send(embed=embed)
            
            elif d1 in range(tt, t):
                print('event4')
                embed = discord.Embed(
                title='Assignment Reminder',
                description=name+'\n Info:'+info,
                color=discord.Colour.purple(), # not to future self change coulder to change coler bar on embed
                )
                embed.add_field(name="Who", value=who)
                embed.add_field(name="Time Due", value=due2, inline=True)
                embed.set_author(name=user, icon_url="https://cdn.discordapp.com/avatars/1161697414013534378/bd878019678d909440dfa117aa89a813.png?size=2048")
                await channel.send(who)
                await channel.send("Assignment due in 1 day", embed=embed)#check beofre send out
                if 0 < logcheck:
                    embed = discord.Embed(
                    title='Channel not found',
                    description=name+'Bot was unable to find a channel to send the reminder to\n *(defalting to this channel untill fixed)*'+info,
                    color=discord.Colour.purple(),)
                    embed.add_field(name="Original Channel", value='original channel was unable to be found this could have been caused by the channel being deleted or the Bot is unable to view the channel')
                    embed.add_field(name="Server not set up", value='The server has not been set up to send reminders to a defalt channel\nrun the command /choose_channel in the channel you want to use as the defalt channel to set this up')
                    embed.set_author(name=bot.user, icon_url="https://cdn.discordapp.com/avatars/1161697414013534378/bd878019678d909440dfa117aa89a813.png?size=2048")
                    embedcheck = embed=embed
                    print('log')
                    await channel.send(embed=embed)

            elif h3 in range(tt, t):
                print('event5')
                embed = discord.Embed(
                title='Assignment Reminder',
                description=name+'\n Info:'+info,
                color=discord.Colour.purple(), # not to future self change coulder to change coler bar on embed
                )
                embed.add_field(name="Who", value=who)
                embed.add_field(name="Time Due", value=due2, inline=True)
                embed.set_author(name=user, icon_url="https://cdn.discordapp.com/avatars/1161697414013534378/bd878019678d909440dfa117aa89a813.png?size=2048")
                await channel.send(who)
                await channel.send("Assignment due in 3 hours", embed=embed)#check beofre send out
                if 0 < logcheck:
                    embed = discord.Embed(
                    title='Channel not found',
                    description=name+'Bot was unable to find a channel to send the reminder to\n *(defalting to this channel untill fixed)*'+info,
                    color=discord.Colour.purple(),)
                    embed.add_field(name="Original Channel", value='original channel was unable to be found this could have been caused by the channel being deleted or the Bot is unable to view the channel')
                    embed.add_field(name="Server not set up", value='The server has not been set up to send reminders to a defalt channel\nrun the command /choose_channel in the channel you want to use as the defalt channel to set this up')
                    embed.set_author(name=bot.user, icon_url="https://cdn.discordapp.com/avatars/1161697414013534378/bd878019678d909440dfa117aa89a813.png?size=2048")
                    embedcheck = embed=embed
                    print('log')
                    await channel.send(embed=embed)

            elif h1 in range(tt, t):
                print('event2')
                embed = discord.Embed(
                title='Assignment Reminder',
                description=name+'\n Info:'+info,
                color=discord.Colour.purple(), # not to future self change coulder to change coler bar on embed
                )
                embed.add_field(name="Who", value=who)
                embed.add_field(name="Time Due", value=due2, inline=True)
                embed.set_author(name=user, icon_url="https://cdn.discordapp.com/avatars/1161697414013534378/bd878019678d909440dfa117aa89a813.png?size=2048")
                await channel.send(who)
                await channel.send("Assignment due in 1 hours", embed=embed)#check beofre send out
                if 0 < logcheck:
                    embed = discord.Embed(
                    title='Channel not found',
                    description=name+'Bot was unable to find a channel to send the reminder to\n *(defalting to this channel untill fixed)*'+info,
                    color=discord.Colour.purple(),)
                    embed.add_field(name="Original Channel", value='original channel was unable to be found this could have been caused by the channel being deleted or the Bot is unable to view the channel')
                    embed.add_field(name="Server not set up", value='The server has not been set up to send reminders to a defalt channel\nrun the command /choose_channel in the channel you want to use as the defalt channel to set this up')
                    embed.set_author(name=bot.user, icon_url="https://cdn.discordapp.com/avatars/1161697414013534378/bd878019678d909440dfa117aa89a813.png?size=2048")
                    embedcheck = embed=embed
                    print('log')
                    await channel.send(embed=embed)

            else:
                print('no event')    
        print("End iteration")

@bot.slash_command()
@option('assignment name', description='enter the name of the assignment')
@option('time')
@option('users', description='@ anyone you want to be pinged (incuding yourself)')
@option('extra info', description =' add any extra details here')
async def assignments_add(ctx: discord.ApplicationContext, name: str, unix_time: int, who: str, info: str):
    if unix_time < int(time.time()): 
        print('inthepast')
        await ctx.respond('you cant set an assingment in the past, only because i cant time travel yet (: ')
        return
    elif unix_time > 1735693261:
        print('2farinfuture')
        await ctx.respond('you cant set an assingment that for in the future sory try making one before 2025 ;) ')
        return
    else:    
        #a = datetime(year, month, day, hour, 0, 0)
        #duea = a.timestamp()
        due = round(unix_time)
        due2 = ('<t:'+str(due)+':R>')
        user= (str(ctx.user))
        userid= str(ctx.author.id)
        channel_id = str(ctx.channel.id)
        guild_id = str(ctx.guild.id)
        print(due)
        file= Path(__file__).parent / 'assinment.txt'
        print('opend file')
        with open(file, 'a') as f:
            f.write(userid)
            f.write('%')
            f.write(user)
            f.write('%')
            f.write(str(due))
            f.write('%')
            f.write(name)
            f.write('%')
            f.write(who)
            f.write('%')
            f.write(info)
            f.write('%')
            f.write(guild_id)
            f.write('%')
            f.write(channel_id+'\n')
            
        print('made it to the end')
        embed = discord.Embed(
                title=name,
                description='Extra info:\n'+info,
                color=discord.Colour.purple(), # not to future self change coulder to change coler bar on embed
                )
        embed.add_field(name="Tagged people", value=who)# who
        embed.add_field(name="Due", value=due2, inline=True)# time
        embed.set_author(name=user, icon_url="https://cdn.discordapp.com/avatars/1041320378137587762/7556cd5daf8ea8fe4597219ffdd9c678?size=1024")
        await ctx.respond('This is your new assignment', embed=embed)  

@bot.slash_command()
@blacklist()
async def assignments_help(ctx):
    embed = discord.Embed(
                title='Assignment Help',
                description='assignment commands:',
                color=discord.Colour.purple(), # not to future self change coulder to change coler bar on embed
                )
    embed.add_field(name="**/assignment_add**", value='this command is for adding assignments you need to fill out all of the options for the command as shown in the **image below** ')# who
    embed.add_field(name="**/assignment_list**", value="lists all of **your** current assignments and due dates")# time
    embed.set_author(name=bot.user, icon_url="https://cdn.discordapp.com/avatars/1041320378137587762/7556cd5daf8ea8fe4597219ffdd9c678?size=1024")
    embed.set_image(url='https://cdn.discordapp.com/attachments/1071573668615966811/1161676518058111128/image.png?ex=65392a90&is=6526b590&hm=1c19272b10c705ba8915de71315daa8599e9c0603b14a24da1d40c1c1116a8c6&')
    embed.add_field(name='__**Unix Time**__', value= 'Unix Time is used for multiple reasons the main one being time zones\n Tool for converting to Unix time ')
    embed.add_field(name= '__**Unix time converter**__', value='[Link](https://www.unixtimestamp.com/)',inline=True)
    embed.add_field(name='__Further Help__', value='for Further help contact my creator in their [Dev server](https://discord.gg/N2dHysf2aQ)')
    await ctx.respond(embed=embed)#check beofre send out

@bot.slash_command()
@blacklist()
async def assignments_list(ctx):
    print('assignemnt_list srarted')
    file= Path(__file__).parent / 'assinment.txt'
    with open(file, 'r') as f:
        print("Begin reading")
        print('author:', ctx.author.id)
        list = ''
        for line in f.readlines():
            userid, user, due, name, who, info, guild_id, channel_id = line.split('%')
            check= time.time()
            print('check')
            if check < int(due):
                print(ctx.author.id)
                print(userid)              
                #if str(ctx.author.id) == str(userid):
                if int(ctx.author.id) == int(userid):
                    due2 = ('<t:'+str(due)+':R>')
                    list= str(list + name +'\n Due: '+  due2 +'\n')
                    print('user has acssess to '+name)

        if list == '':
            list = 'you have no active assignments \nuse /assignment_add to create one'
        embed = discord.Embed(
            title='Your Assignments',
            description=list,
            color=discord.Colour.purple(),) # not to future self change coulder to change coler bar on embed
        embed.set_author(name=user, icon_url="https://cdn.discordapp.com/avatars/1161697414013534378/bd878019678d909440dfa117aa89a813.png?size=2048")
        await ctx.respond(embed=embed)

@bot.slash_command()
@blacklist()
async def currentdate(ctx):
    t= str(round(time.time()))
    d = datetime.now()
    d= d.strftime ('%Y-%m-%d %X')
    k = str('the current unix time the server uses is shown below \n   current time = <t:' + t + ':f> \n   current time in unix = '+t)
    await ctx.respond(k)
 
        
@bot.listen("on_message")
async def on_message(message: discord.Message):

    if message.author.id == bot.user.id:
        return
    
    if message.content.startswith('!ping'):
        await message.reply('Pong!')

    if message.content.startswith('lines'):
        await message.reply('i am made up of 614 lines of code 0_0\n can you find all 14 of my hidden responses/reactions?')

    if message.content.startswith('code'):
        await message.reply('i am made up of 614 lines of code 0_0\n can you find all 14 of my hidden responses/reactions?')

    if message.content.startswith('kill'):
        await message.reply('NO killing is bad D:')

    if message.content.startswith('!channel id'):
        await message.reply(f'the channel id is {message.channel.id}')

    if message.content.startswith('snow'):
        await message.reply(':cloud_snow: :cloud_snow: :cloud_snow: :cloud_snow: :cloud_snow: :cloud_snow: :cloud_snow: :cloud_snow:')
        
    if message.content.startswith('secrete'):
        await message.reply('shhhhhhhhhh!! this response is secrete')
        
    if message.content.startswith('mee6'):
        await message.reply('im way better then mee6 (; )')

    if message.content.startswith('kys'):
         await message.reply('NO')
        
    if message.content.startswith('dog'):
        await message.reply('dogs are nice but i like cats better')
        
    if message.content.startswith('cat'):
        await message.reply('I love cats!!!!!!!! :cat:')

    if message.content.startswith('gun'):
        await message.reply('a:catgun:1104398632947548221')

    if message.content.startswith('heart'):
        await message.reply('<a:blobheart:1104398606842208327>') #num 10
        
    if message.content.startswith('space'):
        await message.reply('space is great... \nI wish i could live in space :rocket: ')
        
    if message.content.startswith('cheese'):
        await message.reply('i like cheese.\n i want to live on the moon cause its made of cheese')
        channel = bot.get_channel(int(message.channel.id))
        m = await bot.wait_for('message', timeout=360)
        print (m)
        if 'no' in m.content.lower() or 'not' in m.content.lower():
            await channel.send ('do not ruin this for me :angry:')

    if 'snow'in message.content.lower() or 'purple'in message.content.lower():
        await message.add_reaction("✅")

    if 'purple'in message.content.lower():
        await message.add_reaction("🟣")
    

@bot.slash_command()
@blacklist()
async def ping(ctx):
    await ctx.respond(f"Pong! `{bot.latency * 1_000:.0f}ms`") 

@bot.slash_command()
@owner_or_admin()
@blacklist()
async def choose_channel(ctx):
    selected_channel_id = ctx.channel.id
    file1= Path(__file__).parent / 'assignment.json'
    f = open(file1, "r")
    json_read = f.read() # read json back to var
    ids_read = json.loads(json_read) # convert json to dict
    f.close()
    id1 = str(ctx.guild.id)

    ids_read[id1] = selected_channel_id

    json2 = json.dumps(ids_read)
    f = open(file1, "w")
    f.write(json2)
    f.close()  
    channel_name = bot.get_channel(selected_channel_id)
    embed = discord.Embed(
            title='Server setup',
            color=discord.Colour.purple(),)
    embed.set_author(name=bot.user, icon_url="https://cdn.discordapp.com/avatars/1161697414013534378/bd878019678d909440dfa117aa89a813.png?size=2048")
    embed.add_field(name=channel_name, value="This channel has been set as the defalt channel for reminders in this server")
    embed.add_field(name='*Changing channel*', value='*To change the chosen channel run this command in the the new channel you want to be the defalt channel for reminders*')
    print('guild_id:',ctx.guild.id,'\nchannel selected:',ctx.channel.id)
    await ctx.respond(embed=embed) 


token = ("BOT_TOKEN")
myLoop.start()
bot.load_extension('jishaku')
bot.run(token)
import discord
import datetime
from random import randint, choice
from discord.ext import commands
from typing import Optional, Tuple
from discord import option
from pathlib import Path
from datetime import datetime, timedelta
from discord.ext import commands, tasks

intents = discord.Intents.default()
intents.message_content = (
    True  # < This may give you `read-only` warning, just ignore it.
)

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
    await bot.change_presence(status=discord.Status.online , activity=discord.Game("Becoming Self Aware"))
    print(f"We have logged in as {bot.user}")
    print("in", len(bot.guilds), "guilds")
    print("guild names:", ", ".join((x.name for x in bot.guilds)))
    loggchannel = int('REPLACE WITH CHANNEL ID')
    channel = bot.get_channel(loggchannel)
    await channel.send(f'{bot.user} is now back online')
    
@bot.slash_command()
async def hello(ctx):
    await ctx.respond("hi 0/")

#old bot/ non restricted
@bot.slash_command()
async def ping(ctx):
    await ctx.respond(f"Pong! `{bot.latency * 1_000:.0f}ms`")
                      
@bot.slash_command()
async def dyslexia(ctx):
    await ctx.respond("*dyslexia is a condition of neurodevelopmental origin that mainly affects the ease with which a person reads, writes, and spells, typically recognized as a specific learning disorder*")

@bot.slash_command()
async def autism(ctx):
    await ctx.respond("*autism is a neurodevelopmental condition that can cause difficulties with social interaction and communication and by restricted or repetitive patterns of thought and behaviour*")

@bot.slash_command()
async def dyspraxia(ctx):
    await ctx.respond("*dyspraxia is a difficulty in performing coordinated movements, often associated with a neurodevelopmental condition*")

@bot.slash_command()
async def adhd(ctx):
    await ctx.respond("*attention deficit hyperactivity disorder, is a condition in which someone, especially a child, is often in a state of activity or excitement and unable to direct their attention towards what they are doing: People with ADHD have difficulty sitting still and concentrating*")

@bot.slash_command()
async def dyscalculia(ctx):
    await ctx.respond("*dyscalculia is a difficulty in performing arithmetical calculations*")

@bot.slash_command()
async def dysgraphia(ctx):
    await ctx.respond("*dysgraphia is an inability to write coherently, as a symptom of a neurological condition or as an aspect of a learning disability.*")

@bot.slash_command()
async def xmas(ctx):
    CHRISTMAS = datetime.datetime(year=2023, month=12, day=25)
    await ctx.respond("i can't wait because " + discord.utils.format_dt(CHRISTMAS, 'R') + "its christmas :D")

@bot.slash_command()
@option("timezone", description="Enter the time zone", choices =["GMT", "MST"])
async def xmas_option(ctx: discord.ApplicationContext,timezone: str,):
    if timezone == "GMT":
        await ctx.respond("i cant wait because <t:1703462400:R> its CHRISTMAS :D :christmas_tree:")
    elif timezone == "MST":
        await ctx.respond("i cant wait because <t:1703487600:R> its CHRISTMAS :D :christmas_tree:")

@bot.slash_command()
async def about_me(ctx):
    await ctx.respond("Hi :), my name is Snowflake im a simple bot. If theres a problem with me contact my creator snowy708 in my development server https://discord.gg/K9TVeCBPuM.")

@bot.slash_command()
async def gay(ctx):
    await ctx.respond("A person who has sexual attraction to members of the same gender or sex")

@bot.slash_command()
async def lesbian(ctx):
    await ctx.respond("A female or non-binary who has sexual attractions to members of the same gender or sex") 

@bot.slash_command()
async def pansexual(ctx):
    await ctx.respond("A person who can feel an attraction to anyone, including individuals who do not identify as a specific gender.")

@bot.slash_command()
async def asexual(ctx):
    await ctx.respond("A person that feels little or no sexual attraction.")

@bot.slash_command()
async def bisexual(ctx):
    await ctx.respond("A person sexually attracted to people of more than one sex and/or gender.")

@bot.slash_command()
async def cisgender(ctx):
    await ctx.respond("A person whose gender expression/identity is the same as at birth.")  

@bot.slash_command()
async def transgender(ctx):
    await ctx.respond("A person whose gender expression or identity is not the same as their sex assigned at birth.")


@bot.slash_command()
async def nonbinary(ctx):
    await ctx.respond("non-binary is relating to a gender identity that does not conform to traditional binary beliefs about gender (male/female)")


@bot.slash_command()
async def polyamorous(ctx):
    await ctx.respond("characterized by or involved in the practice of engaging in multiple romantic (and typically sexual) relationships, with the consent of all the people involved")

token = ("BOT_TOKEN")

bot.load_extension('jishaku')
bot.run(token)
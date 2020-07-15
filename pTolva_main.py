import discord
from discord.ext import commands
import asyncio
import random
import praw  # Reddit stuff

# Read discord token from token.txt
def read_token():
    with open("token.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()

token = read_token()

# Client = discord.Client() #old version? couldn't use commands
client = commands.Bot(command_prefix = '/') # I must be doing something wrong because I can't get my @client.command to work.

# Read reddit ID and Secret
def readClientID():
    with open("redditClientID.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()

def readClientSecret():
    with open("redditClientSecret.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()

redditClientID = readClientID()
redditClientSecret = readClientSecret()

# All the reddit ID's needed
reddit = praw.Reddit(client_id=redditClientID,
                     client_secret=redditClientSecret,
                     user_agent='pTolva')

def onlinep12a(guild):
        online = 0
        idle = 0
        offline = 0

        for m in guild.members:
            if str(m.status) == "online":
                online += 1
            if str(m.status) == "offline":
                offline += 1
            else:
                idle += 1
        
        return online, idle, offline

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    print(f"{message.guild}: {message.channel}: {message.author}: {message.content}")
    testServer = client.get_guild(638458389667643414)
    mellanhanget = client.get_guild(416321312886358036)
    guilds = [testServer, mellanhanget]
    emojis = ['👋', '🤚', '🖐', '✋', '🖖', '👌', '🤏', '✌️', '🤞', '🤟', '🤘', '🤙', '👈', '👉', '👆', '🖕', '👇', '☝️', '👍', '👎', '✊', '👊', '🤛', '🤜', '👏', '🙌', '👐', '🤲', '🤝', '🙏', '✍️', '💅', '🤳', '💪', '🦾', '🦵', '🦿', '🦶', '👂', '🦻', '👃', '🧠', '🦷', '🦴', '👀', '👁', '👅', '👄', '💋', '🩸']
    msgContent_list = []

    # If the bot is the writer, don't do anything
    if message.author == client.user:
        return

    # Check server and change GuildID depending on server
    if message.guild in guilds:
        if message.guild == testServer:
            guildID = testServer

        elif message.guild == mellanhanget:
            guildID = mellanhanget

        # Count the members 
        if "members p12a?" in message.content.lower():
            await message.channel.send(f"```{guildID.member_count} members```")

        # Count online, idle, etc.
        elif "online p12a?" == message.content.lower():
            online, idle, offline = onlinep12a(guildID)

            await message.channel.send(f"```Online: {online} \nIdle/busy/dnd: {idle} \nOffline: {offline}```")

    if message.content.startswith('pTolva'):
        await message.channel.send('Hi, I am p12a! My available commands are: ')
        await message.channel.send('members p12a?, online p12a?, copy, paste, /cats and ')
        await message.channel.send('roll d n, where n is the highest number on the dice')

    elif message.content.startswith('cookie'):
        await message.channel.send(':cookie:')

    elif "color" in message.content.lower():
        await message.channel.send('Colour*')

    elif "armor" in message.content.lower():
        await message.channel.send('Armour*')

    elif "69" in message.content.lower():
        await message.channel.send('hehe nice')

    elif "fucking p12a" in message.content.lower():
        await message.channel.send('logging out :upside_down:')
        await client.close()

    # Writes the line above the message 'copy' to copied.txt
    elif message.content.startswith('copy'):
        msg_list = await message.channel.history(limit=2).flatten()
        for msg in msg_list:
            msgContent_list += [msg.content]
        with open("copied.txt", "w") as f:
            f.write(msgContent_list[1])
        print(msgContent_list)

    # Pastes the line in copied.txt to the channel where paste is written
    elif message.content.startswith('paste'):
        with open("copied.txt", "r") as f:
            f_contents = f.read()
        await message.channel.send(f_contents)
        print(f_contents)

    # roll a dice
    elif message.content.startswith('roll d '):
        messageSplit = message.content.split(" ")
        diceHigh = int(messageSplit[2])
        # Turns out randrange isn't  rolling the highest number, so have to plus one
        n = random.randrange(1, diceHigh+1)
        await message.channel.send(n)

    # Add reaction
    for emoji in emojis:
        if emoji in message.content.lower():
            await message.add_reaction(emoji)
    
    # on message makes it so that commands can't work unless I have this code
    await client.process_commands(message)

@client.command()
async def cats(ctx):
    cats_submissions = reddit.subreddit('cats').hot()
    post_to_pick = random.randint(1, 10)
    for i in range(0, post_to_pick):
        submission = next(x for x in cats_submissions if not x.stickied)
    await ctx.send(submission.url)

client.run(token)
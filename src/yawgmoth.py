# ---------------------------
# Imports
# ---------------------------
from __future__ import print_function
from future import standard_library
standard_library.install_aliases()
import discord
import sys
import subprocess
import asyncio
import commands

# ---------------------------
# Startup Server / Channel
# ---------------------------
DESTServ = "/r/CompetitiveEDH"
DESTChan = "urborg"
TokenLocation = "/home/ec2-user/token.txt"

# ---------------------------
# Initialization
# ---------------------------
yawgmoth = discord.Client()

# ---------------------------
# Event: Ready
# ---------------------------
@yawgmoth.event
@asyncio.coroutine
def on_ready():

    riseServer = ""
    riseChannel= ""

    print("Destination server for rising: " + DESTServ)
    serverlist = list(yawgmoth.servers)
    for server in serverlist:
        print("Checking if {} is our destination".format(server))
        if server.name.lower() == DESTServ.lower():
            riseServer = server
            print("Rise server located")
    
    if not riseServer:
        print("No server found with name " + DESTServ)
    else:
        print("Destination channel for rising: " + DESTChan)
        channellist = list(riseServer.channels)
        for channel in channellist:
            print("Checking if {} is our destination".format(channel))
            if channel.name.lower() == DESTChan.lower():
                riseChannel = channel
                print("Rise channel located")
    
    print('User:' + '\t\t' + yawgmoth.user.name)
    print('ID:' + '\t\t' + yawgmoth.user.id)
    
    if riseServer:
        print('Server:' + '\t\t' + riseServer.name + ", " + riseServer.id)
        if riseChannel:
            print('Channel:' + '\t' + riseChannel.name)
            yield from yawgmoth.send_message(riseChannel, 'I rise...')

# ---------------------------
# Event: Message
# ---------------------------
@yawgmoth.event
@asyncio.coroutine
def on_message(message):
    response = ''
    response = commands.cmd_fetch(message)
    if message.content.startswith('!details'):
        response += commands.cmd_details(message)
    if message.content.startswith('!rulings'):
        response += commands.cmd_rulings(message)
    if message.content.startswith('!standardban'):
        response += commands.cmd_standardban(message)
    if message.content.startswith('!modernban'):
        response += commands.cmd_modernban(message)
    if message.content.startswith('!legacyban'):
        response += commands.cmd_legacyban(message)
    if message.content.startswith('!vintageban'):
        response += commands.cmd_vintageban(message)
    if message.content.startswith('!edhban'):
        response += commands.cmd_edhban(message)
    if message.content.startswith('!obey'):
        response += commands.cmd_obey(message)
    if message.content.startswith('!moon'):
        response += commands.cmd_moon(message)
    if message.content.startswith('!sun'):
        response += ':sun_with_face:'
    if message.content.startswith('!git'):
        response += commands.cmd_git(message)
    if message.content.startswith('!version'):
        response += commands.cmd_version(message)
    if message.content.startswith('!blush'):
        response += ':yawgblush:'
    if message.content.startswith('!sheep'):
        response += ':sheep:'
    if message.content.startswith('!mute'):
        response += commands.cmd_mute(message)
    if message.content.startswith('!admin'):
        response += commands.cmd_addadmin(message)
    if message.content.startswith('!clearmute'):
        response += commands.cmd_clearmute(message)
    if message.content.startswith('!pingme'):
        response += commands.cmd_ping(message)
    if message.content.startswith('!rules'):
        response += 'http://media.wizards.com/2016/docs/MagicCompRules_04082016.pdf'
    if message.content.startswith('!reset'):
        response += commands.cmd_reset(message)
    if message.content.startswith('!shutdown'):
        response += commands.cmd_shutdown(message)
    if message.content.startswith('!image'):
        response += commands.cmd_image(message)
    if message.content.startswith('!price'):
        response += commands.cmd_price(message)

    if message.author.name not in commands.muted_users:
        if response:
            yield from yawgmoth.send_message(message.channel, response)



# ---------------------------
# Login
# ---------------------------
#yawgmoth.login(sys.argv[1], sys.argv[2])


# ---------------------------
# Startup
# ---------------------------
with open (TokenLocation, "r") as myfile:
    token=myfile.read()
yawgmoth.run(token)

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
import personalvars

# ---------------------------
# Personal Variables
# ---------------------------
TokenLocation = personalvars.token_location()
DESTServ = personalvars.rise_server()
DESTChan = personalvars.rise_channel()
riseMSG = personalvars.rise_message()

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
        modsetup = commands.setup_mods(riseServer)
        print("Setting up yawgmods...\n{}".format(modsetup))
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
            yield from yawgmoth.send_message(riseChannel, riseMSG)

# ---------------------------
# Event: Message
# ---------------------------
@yawgmoth.event
@asyncio.coroutine
def on_message(message):
    response = ''
    if message.author not in commands.ignored_users:
        response = commands.cmd_fetch(message)
        
        ##############
        # Card Specs #
        ##############
        if message.content.startswith('!details'):
            response += commands.cmd_details(message)
        if message.content.startswith('!rulings'):
            response += commands.cmd_rulings(message)
        if message.content.startswith('!image'):
            response += commands.cmd_image(message)
        if message.content.startswith('!price'):
            response += commands.cmd_price(message)
                
        ############
        # Banlists #
        ############
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
        
        ############
        # Misc MTG #
        ############
        if message.content.startswith('!rules'):
            response += 'http://media.wizards.com/2016/docs/MagicCompRules_04082016.pdf'
        
        ############
        # Bot Info #
        ############
        if message.content.startswith('!git'):
            response += commands.cmd_git(message)
        if message.content.startswith('!version'):
            response += commands.cmd_version(message)
        
        ##############
        # Just 4 Fun #
        ##############
        if message.content.startswith('!obey'):
            response += commands.cmd_obey(message)
        if message.content.startswith('!moon'):
            response += commands.cmd_moon(message)
        if message.content.startswith('!sun'):
            response += ':sun_with_face:'
        if message.content.startswith('!blush'):
            response += ':yawgblush:'
        if message.content.startswith('!sheep'):
            response += ':sheep:'
        if message.content.startswith('!pingme'):
            response += commands.cmd_ping(message)
        if message.content.startswith('!shitposter'):
            response += commands.cmd_shitposter(yawgmoth, message)
        if message.content.startswith('!cockatrice'):
            response += commands.cmd_cockatrice(yawgmoth, message)
            
        ################
        # Mod Commands #
        ################
        if message.content.startswith('!ignore'):
            response += commands.cmd_ignore(message)
        if message.content.startswith('!yawgmod'):
            response += commands.cmd_yawgmod(message)
        if message.content.startswith('!clearignore'):
            response += commands.cmd_clearignore(message)
            
        ##################
        # Admin Commands #
        ##################
        if message.content.startswith('!reset'):
            response += commands.cmd_reset(message)
        if message.content.startswith('!reboot') or message.content.startswith('!nogitreset'):
            response += commands.cmd_reboot(message)
        if message.content.startswith('!shutdown'):
            response += commands.cmd_shutdown(message)

        ####################
        # Admin Just 4 Fun #
        ####################
        if message.content.startswith('!gametime'):
            gn = commands.cmd_gametime(message)
            if gn:
                yield from yawgmoth.change_presence(game=discord.Game(name=gn))

        if response:
            yield from yawgmoth.send_message(message.channel, response)

# ---------------------------
# Startup
# ---------------------------
with open (TokenLocation, "r") as myfile:
    token=myfile.read()
yawgmoth.run(token)

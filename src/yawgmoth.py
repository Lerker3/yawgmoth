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
MUTE_MESSAGE_TEXT = personalvars.mute_cmd_msg()

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
        if message.author in commands.muted_users:
            yield from yawgmoth.delete_message(message)
        else:
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
            if message.content.startswith('!temp'):
                response += commands.cmd_temp(message)

                
            #####################
            # Role Change Block #
            #####################
            if message.content.startswith('!cockatrice') or message.content.startswith('!shitposter') or message.content.startswith('!foodforthonk'):
                todo = ['n/a', 'How did you even get to this place in the code?']
                if message.content.startswith('!cockatrice'):
                    todo = commands.cmd_rolech(message, 'Cockatrice')
                if message.content.startswith('!shitposter'):
                    todo = commands.cmd_rolech(message, 'Shitposter')
                if message.content.startswith('!foodforthonk'):
                    todo = commands.cmd_rolech(message, 'Member')
                if todo[0] == 'n/a':
                    response += todo[1]
                if todo[0] == 'Add':
                    yield from yawgmoth.add_roles(todo[1], todo[2])
                    response += todo[3]
                if todo[0] == 'Remove':
                    yield from yawgmoth.remove_roles(todo[1], todo[2])
                    response += todo[3]            
                
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
            if message.content.startswith('!mute'):
                mute_resp = commands.cmd_mute(message)
                if mute_resp[0]:
                    response += mute_resp[1] + mute_resp[2]
                    #yield from yawgmoth.send_message(mute_resp[1], MUTE_MESSAGE_TEXT)
                else:
                    response += mute_resp[1]
                

            ####################
            # Admin Just 4 Fun #
            ####################
            if message.content.startswith('!gametime'):
                gn = commands.cmd_gametime(message)
                if gn:                                      #If a non-admin tries this command, gn will be blank
                    if gn == 'CLEAR':
                        yield from yawgmoth.change_presence()
                    else:
                        yield from yawgmoth.change_presence(game=discord.Game(name=gn))
            if message.content.startswith('!typing'):
                yield from yawgmoth.send_typing(message.channel)
                yield from yawgmoth.delete_message(message)
            if message.content.startswith('!echo'):
                eResp = commands.cmd_echo(message)
                if eResp:                                   #If a non-admin tries this command, eResp will be blank
                   response += eResp
                   yield from yawgmoth.delete_message(message)

            if response:
                yield from yawgmoth.send_message(message.channel, response)

# ---------------------------
# Startup
# ---------------------------
with open (TokenLocation, "r") as myfile:
    token=myfile.read()
yawgmoth.run(token)

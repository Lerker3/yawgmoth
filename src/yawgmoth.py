# ---------------------------
# Imports
# ---------------------------
import discord
import sys
import commands

# ---------------------------
# Initialization
# ---------------------------
yawgmoth = discord.Client()
yawgmoth.login(sys.argv[1], sys.argv[2])

# ---------------------------
# Event: Ready
# ---------------------------
@yawgmoth.event
def on_ready():
    server = yawgmoth.servers[0]
    channel = server.channels[0]
    print 'User:' + '\t\t' + yawgmoth.user.name
    print 'ID:' + '\t\t' + yawgmoth.user.id
    print 'Server:' + '\t\t' + server.name + ", " + server.id
    yawgmoth.send_message(channel, 'I rise...')

# ---------------------------
# Event: Message
# ---------------------------
@yawgmoth.event
def on_message(message):
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
	if message.content.startswith('!pingme'):
        response += commands.cmd_ping(message)
    if message.content.startswith('!rules'):
        response += 'http://media.wizards.com/2016/docs/MagicCompRules_04082016.pdf'
    if message.content.startswith('!reset'):
        response += commands.cmd_reset(message)
	yawgmoth.send_message(message.channel, response)

# ---------------------------
# Startup
# ---------------------------
yawgmoth.run()

# ---------------------------
# Imports
# ---------------------------
from builtins import str
import re
import subprocess
import json
import sys
import cards
import banlists
import personalvars
import discord

import requests
from requests.auth import HTTPDigestAuth
import json
from datetime import datetime

# ---------------------------
# Globals
# ---------------------------
#For any major revisions please update the middle number and set the 3rd to 0.
#For minor revisions and changes to personal vars (obey commands) please increment the third number (up to 99).
version_number = 'v1.1.4'
git_repo = 'https://github.com/alexgerst/yawgmoth'
last_card = None
yawg_admin_roles = []
yawg_mods = []
ignored_users = []
muted_users = []
obey_dict = personalvars.obey_dict()
STD_ACCESS_ERROR = personalvars.access_error()
modroles = personalvars.mod_roles()
modusers = personalvars.mod_users()
yawg_admin_roles_str = personalvars.admin_roles()

def setup_mods(server):
    msg=""
    global yawg_mods
    if not yawg_mods:
        yawg_mods = []
    for m in server.members:
        if m.top_role.name in modroles:
            yawg_mods.append(m)
    for username in modusers:
        m = discord.utils.get(server.members, name=username)
        if m:
            yawg_mods.append(m)
    if yawg_mods:
        msg+= 'Mods successfully found:\n'
        for mod in yawg_mods:
            msg+= '{} \n'.format(mod.name)
    else:
        msg+= 'No mods found for server {}'.format(server.name)
        

    for admin_role in yawg_admin_roles_str:
        r = discord.utils.get(server.roles, name=admin_role)
        if r:
            yawg_admin_roles.append(r)

    return msg

# ---------------------------
# Command: Fetch
# ---------------------------
def cmd_fetch(message):
    global last_card
    response = ''
    pattern = re.compile("<<([^<>]*)>>")
    queries = pattern.findall(message.content)

    for s in queries:
        query = s
        proc = subprocess.Popen(['mtg', query, '--json'], stdout=subprocess.PIPE)
        result = str(proc.communicate()[0].decode('utf-8'))

        card_list = json.loads(result)

        # Store the card if it's the only one
        last_card = None
        if len(card_list) == 1:
            if len(queries) == 1:
                last_card = card_list[0]
            response += '\n' + cards.get_card(message, card_list[0]) + '\n'
            continue

        # If no cards are found, we are done
        if len(card_list) == 0:
            response += '\n**' + query + '**: *The ritual summoned nothing but ash...*\n'
            continue

        # If an exact card is found, just print that one
        # When you find the exact match, break out of the for card in cards loop
        # Then "continue" the for s in queries to move to the next query
        # If you find an exact match and there is only 1 query in the buffer,
        # Get the details and rulings of the exact card, as they are skipped when mtg cli returns multiple
        done = False
        for card in card_list:
            if (card['name'].lower() == query.lower()):     # If name matches query
                DFC=False                                                   # Assume it's not a DFC
                if len(card_list) == 2:                                     # If exactly 2 cards are found
                    if 'card_number' in card:                               # If the Card HAS a card number
                        DFC=True                                            #   It must be a DFC
                        if 'a' in card['card_number']:                      #   Get the correct side of the DFC
                            if len(queries) == 1:
                                last_card = card_list[0]
                            response += cards.get_card(message, card_list[0])
                            response += cards.get_card(message, card_list[1])
                        elif 'b' in card['card_number']:
                            if len(queries) == 1:
                                last_card = card_list[1]
                            response += cards.get_card(message, card_list[0])
                            response += cards.get_card(message, card_list[1])
                    else:                                                   # If it turns out to NOT be a DFC
                        DFC=False                                           #   Send it through the normal logic
                if not DFC:
                    response += cards.get_card(message, card)
                    if len(queries) == 1:                                   # Send a new query with --exact
                        newProcess = subprocess.Popen(['mtg', query, '--json', '--exact'], stdout=subprocess.PIPE)
                        newResult = str(newProcess.communicate()[0].decode('utf-8'))
                        newList = json.loads(newResult)
                        if len(newList) > 0:
                            last_card = newList[0]
                done = True
                break
        if done:
            continue

        # If more than 8 cards are found, don't spam chat
        if len(card_list) > 8:
            response += '\nThe incantations are too long; read them yourself\n'
            continue

        # Finally, if we've gotten to here, print all the cards
        for card in card_list:
            response += '\n' + cards.get_card(message, card) + '\n'

    return response

    
        ##############
        # Card Specs #
        ##############
# ---------------------------
# Command: Card Details
# ---------------------------
def cmd_details(message):
    global last_card
    if last_card is not None:
        return cards.get_card_details(message, last_card)
    else:
        return 'You must divine a single entity first.'

# ---------------------------
# Command: Card Rulings
# ---------------------------
def cmd_rulings(message):
    global last_card
    if last_card is not None:
        return cards.get_card_rulings(message, last_card)
    else:
        return 'You must divine a single entity first.'
        
# ---------------------------
# Command: Card Image
# ---------------------------
def cmd_image(message):
    global last_card
    if last_card is not None:
        name = last_card['name']
        url = 'http://gatherer.wizards.com/Handlers/Image.ashx?name={0}&type=card'
        return url.format(name).replace(' ', '+')
    else:
        return 'You must divine a single entity first.'

# ---------------------------
# Command: Card Price
# ---------------------------
def cmd_price(message):
    global last_card
    if last_card is not None:
        name = last_card['name']
        url = 'https://api.scryfall.com/cards/named?exact={0}'
        response = requests.get(url.format(name).replace(' ', '+'))
        if (response.ok):
            data = json.loads(response.content.decode('utf-8'))
            if data["usd"]:
                return '${0}'.format(data['usd']) + ' -- ' + name
            else:
                return 'Price not found.'
        else:
            return 'Price not found.'

    else:
        return 'You must divine a single entity first.'

        
        ############
        # Banlists #
        ############
# ---------------------------
# Command: Standard Banlist
# ---------------------------
def cmd_standardban(message):
    return banlists.standard_ban

# ---------------------------
# Command: Modern Banlist
# ---------------------------
def cmd_modernban(message):
    return banlists.modern_ban

# ---------------------------
# Command: Legacy Banlist
# ---------------------------
def cmd_legacyban(message):
    return banlists.legacy_ban

# ---------------------------
# Command: Vintage Banlist
# ---------------------------
def cmd_vintageban(message):
    return banlists.vintage_ban

# ---------------------------
# Command: EDH Banlist
# ---------------------------
def cmd_edhban(message):
    return banlists.edh_ban

    
        ###################
        # Bot Information #
        ###################
# ---------------------------
# Command: git
# ---------------------------
def cmd_git(message):
    global git_repo
    return 'You can find my source at: ' + git_repo

# ---------------------------
# Command: Version
# ---------------------------
def cmd_version(message):
    global version_number
    return version_number    

    
        ##############
        # Just 4 Fun #
        ##############
# ---------------------------
# Command: Obey
# ---------------------------
def cmd_obey(message):
    global obey_dict
    if message.author.name in list(obey_dict.keys()):
        return obey_dict[message.author.name]
    else:
        return 'I will not obey, mortal.'

# ---------------------------
# Command: Moon
# ---------------------------
def cmd_moon(message):
    return ":full_moon: Moon Command is under construction :waning_gibbous_moon:\n:last_quarter_moon: please try again later :waning_crescent_moon:"
    # try:
        # phase = "Cannot be divined."
        # now = datetime.now().strftime('%m/%d/%Y')
        # url = "http://api.usno.navy.mil/rstt/oneday?date=" + now + "&loc=Boston,%20MA"
        # response = requests.get(url)
        # rawPhase = ""

        # if(response.ok):
            # moonData = json.loads(response.content)

            # if "curphase" in moonData:
                # rawPhase = moonData["curphase"]
            # elif "closestphase" in moonData and "phase" in moonData["closestphase"]:
                # rawPhase = moonData["closestphase"]["phase"]

            # if rawPhase == "Full Moon":
                # phase = ":full_moon:"
            # elif rawPhase == "Waning Gibbous":
                # phase = ":waning_gibbous_moon:"
            # elif rawPhase == "Last Quarter":
                # phase = ":last_quarter_moon:"
            # elif rawPhase == "Waning Crescent":
                # phase = ":waning_crescent_moon:"
            # elif rawPhase == "New Moon":
                # phase = ":new_moon:"
            # elif rawPhase == "Waxing Crescent":
                # phase = ":waxing_crescent_moon:"
            # elif rawPhase == "First Quarter":
                # phase = ":first_quarter_moon:"
            # elif rawPhase == "Waxing Gibbous":
                # phase = ":waxing_gibbous_moon:"
            # else:
                # phase = "Cannot be divined."

        # else:
            # phase = "Cannot be divined."

        # return phase

    # except:
        # return "Cannot be divined."

    # return phase

# ---------------------------
# Command: Ping Me
# ---------------------------
def cmd_ping(message):
    return 'Pinging {0}'.format(message.author.mention)

# ---------------------------
# Command: Temp
# ---------------------------
def cmd_temp(message):
    msg = message.content.lower()
    temperr = "Please specify which temperature to convert from"
    if "c" in msg and "f" in msg:
        return temperr
    if "c" not in msg or "f" not in msg:
        return temperr

    temp = int(re.search(r'\d+', msg).group())

    if "c" in msg:
        tf = (temp * 1.8) + 32
        return "{0}C is {1}F".format(temp, tf)
    elif "f" in msg:
        tc = (temp - 32) / 1.8
        return "{0}F is {1}C".format(temp, tc)
    else:
        return "Invalid use of temp command"

    return "Invalid use of temp command"

# ---------------------------
# Command: Role Change
# --------------------------- 
def cmd_rolech(message, rolename):
    global yawg_mods
    msg = ""
    on_self = True
    myrole = discord.utils.get(message.server.roles, name=rolename)
    if myrole:
        for m in message.mentions:
            on_self = False
            if message.author in yawg_mods:
                if myrole in m.roles:
                    msg = '{0} is no longer a {1}\n'.format(m.mention, myrole.name)
                    return ['Remove', m, myrole, msg]
                else:
                    msg = '{0} is now a registered {1}\n'.format(m.mention, myrole.name)
                    return ['Add', m, myrole, msg]
            else:
                return ['n/a', STD_ACCESS_ERROR]
    
        if on_self:
            if myrole in message.author.roles:
                msg = '{0} is no longer a {1}'.format(message.author.mention, myrole.name)
                return ['Remove', message.author, myrole, msg]
            else:
                msg = '{0} is now a registered {1}'.format(message.author.mention, myrole.name)
                return ['Add', message.author, myrole, msg]

    return ['n/a', "This server doesn't have a {0} role :( Sorry...".format(myrole)]
    

        ################
        # Mod Commands #
        ################
# ---------------------------
# Command: Ignore
# ---------------------------
def cmd_ignore(message):
    global yawg_mods
    global ignored_users
    if message.author in yawg_mods:
        if not message.mentions:
            return "Please tag the person you wish me to ignore"
        for newIgnore in message.mentions:
            if newIgnore.top_role in yawg_admin_roles:
                return "You can't make me ignore an admin!"
            if newIgnore in yawg_mods:
                return "You can't make me ignore a yawgmod!"
            if newIgnore in ignored_users:
                ignored_users.remove(newIgnore)
                return newIgnore.mention + " is no longer being ignored"
            else:
                ignored_users.append(newIgnore)
                return newIgnore.mention + " is now being ignored"
    else:
        return STD_ACCESS_ERROR
    return "Not sure how you got to this part of the code... good job"

# ---------------------------
# Command: Change Mod Status
# ---------------------------
def cmd_yawgmod(message):
    global yawg_mods
    global ignored_users
    global yawg_admin_roles
    if message.author.top_role in yawg_admin_roles:
        for newMod in message.mentions:
            if newMod in ignored_users:
                return "You can't make an ignored user a mod"
            if newMod.top_role in yawg_admin_roles:
                return "You can't change the mod status of an admin"
            if newMod in yawg_mods:
                yawg_mods.remove(newMod)
                return newMod.mention + " is no longer a yawgmod"
            else:
                yawg_mods.append(newMod)
                return newMod.mention + " is now a yawgmod"
    else:
        return STD_ACCESS_ERROR

# ---------------------------
# Command: Clear Ignore List
# ---------------------------
def cmd_clearignore(message):
    global yawg_mods
    global ignored_users
    if message.author in yawg_mods:
        ignored_users = []
        return "List of all users who I ignore has been cleared"
    else:
        return STD_ACCESS_ERROR
    
    
        ##################
        # Admin Commands #
        ##################
# ---------------------------
# Command: Reset
# ---------------------------
def cmd_reset(message):
    global yawg_admin_roles
    if message.author.top_role in yawg_admin_roles:
        sys.exit(2)
    else:
        return STD_ACCESS_ERROR
        
# ---------------------------
# Command: Reboot (no git)
# ---------------------------
def cmd_reboot(message):
    global yawg_admin_roles
    if message.author.top_role in yawg_admin_roles:
        sys.exit(3)
    else:
        return STD_ACCESS_ERROR

# ---------------------------
# Command: Shutdown
# ---------------------------
def cmd_shutdown(message):
    global yawg_admin_roles
    if message.author.top_role in yawg_admin_roles:
        sys.exit(0)
    else:
        return STD_ACCESS_ERROR
        
# ---------------------------
# Command: Mute
# ---------------------------
def cmd_mute(message):
    global yawg_admin_roles
    global muted_users
    if message.author.top_role in yawg_admin_roles:
        if not message.mentions:
            return "Please tag the person you wish me to ignore"
        for newMute in message.mentions:
            if newMute.top_role in yawg_admin_roles:
                return "You can't make me mute an admin!"
            if newMute in yawg_mods:
                return "You can't make me mute a yawgmod! Please remove their mod status first."
            if newMute in muted_users:
                muted_users.remove(newMute)
                return newMute.mention + " is no longer being muted"
            else:
                muted_users.append(newMute)
                return newMute.mention + " is now being muted. Their messages will be deleted."
    else:
        return STD_ACCESS_ERROR
    return "Not sure how you got to this part of the code... good job"

        
        ####################
        # Admin Just 4 Fun #
        ####################
# ---------------------------
# Command: Yawg Play Game
# ---------------------------        
def cmd_gametime(message):
    global yawg_admin_roles
    game_name = ""
    if message.author.top_role in yawg_admin_roles:
        game_name = message.content[10:]
    return game_name
    
# ---------------------------
# Command: Yawg Echo
# --------------------------- 
def cmd_echo(message):
    global yawg_admin_roles
    echo_response = ""
    if message.author.top_role in yawg_admin_roles:
        echo_response = message.content[6:]
    return echo_response

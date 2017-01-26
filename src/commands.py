# ---------------------------
# Imports
# ---------------------------
import re
import subprocess
import json
import sys
import cards
import banlists

import requests
from requests.auth import HTTPDigestAuth
import json
from datetime import datetime

# ---------------------------
# Globals
# ---------------------------
version_number = 'v0.10.5'
git_repo = 'https://github.com/alexgerst/yawgmoth'
last_card = None
reset_users = ['Gerst','aceuuuu','Lerker','Shaper', 'ShakeAndShimmy']
mute_admins = ['Gerst','aceuuuu','Lerker','Shaper', 'ShakeAndShimmy']
muted_users = []
obey_dict = {
        'Shaper': 'I obey, Master Shaper.',
        'aceuuu': 'I obey, Admiral Aceuuu~!',
        'muCephei': 'I obey, muCephei.',
        'Gerst': 'I obey, Artificer Gerst.',
        'Lerker': 'I obey, Commodore 64 Lerker.',
        'ShakeAndShimmy': 'I obey, Chancellor ShakeAndShimmy.',
        'angelforge': 'I obey, Lord AngelForge.',
        'JimWolfie': 'Suck my necrotic dick, Jim.',
        'Skuloth': 'Zur is for scrubs, I refuse to obey.',
        'Noon2Dusk': 'I obey, Inventor Noon.',
        'razzliox': 'I obey, Razzberries.',
        'ifarmpandas': 'Beep boop, pandas are the best.',
        'Rien': 'I obey, kiddo.',
        'K-Ni-Fe': 'I obey, because I\'m 40% Potassium, Nickel and Iron.',
        'BigLupu': 'Rim my necrotic yawghole, Lupu.',
        'PGleo86': 'shh bby is ok.',
        'tenrose': 'I won\'t obey, but that\'s not because you\'re a bad person. I just like to be free, as do you. You have a great day :)',
        'captainriku': 'I obey, Jund Lord Riku.',
        'Mori': ':sheep: baaa',
        'infiniteimoc': 'I obey, Imoc, Herald of the Sun.',
        'neosloth': 'Long days and pleasant nights, neosloth.',
        'Lobster': 'I obey, Spice Sommelier Lobster.',
	'Noahgs': 'I bow to thee, Master of Cows, Noahgs.',
	'Tides': 'Let me... TORTURE YOUR EXISTENCE!!!!..... sorry that was bad.'
	'Sleepy': 'No one likes you.'
}

# ---------------------------
# Command: Fetch
# ---------------------------
def cmd_fetch(message):
    global last_card
    response = ''
    queries = re.findall(("<<([^<>]*)>>"), message.content.encode('utf-8'))

    for s in queries:
        query = s.encode('utf-8')
        proc = subprocess.Popen(['mtg', query, '--json'], stdout=subprocess.PIPE)
        result = str(proc.communicate()[0])

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
            if (card['name'].encode('utf-8').lower() == query.lower()):     # If name matches query
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
                        newResult = str(newProcess.communicate()[0])
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

# ---------------------------
# Command: Details
# ---------------------------
def cmd_details(message):
    global last_card
    if last_card is not None:
        return cards.get_card_details(message, last_card)
    else:
        return 'You must divine a single entity first.'

# ---------------------------
# Command: Rulings
# ---------------------------
def cmd_rulings(message):
    global last_card
    if last_card is not None:
        return cards.get_card_rulings(message, last_card)
    else:
        return 'You must divine a single entity first.'

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

# ---------------------------
# Command: Obey
# ---------------------------
def cmd_obey(message):
    global obey_dict
    if message.author.name in obey_dict.keys():
        return obey_dict[message.author.name]
    else:
        return 'I will not obey, mortal.'

# ---------------------------
# Command: Moon
# ---------------------------
def cmd_moon(message):
    try: 
        phase = "Cannot be divined."
        now = datetime.now().strftime('%m/%d/%Y')
        url = "http://api.usno.navy.mil/rstt/oneday?date=" + now + "&loc=Boston,%20MA"
        response = requests.get(url)
        rawPhase = ""

        if(response.ok):
            moonData = json.loads(response.content)
            
            if "curphase" in moonData:
                rawPhase = moonData["curphase"]
            elif "closestphase" in moonData and "phase" in moonData["closestphase"]:
                rawPhase = moonData["closestphase"]["phase"]

            if rawPhase == "Full Moon": 
                phase = ":full_moon:"
            elif rawPhase == "Waning Gibbous":
                phase = ":waning_gibbous_moon:"
            elif rawPhase == "Last Quarter":
                phase = ":last_quarter_moon:"
            elif rawPhase == "Waning Crescent":
                phase = ":waning_crescent_moon:"
            elif rawPhase == "New Moon":
                phase = ":new_moon:"
            elif rawPhase == "Waxing Crescent":
                phase = ":waxing_crescent_moon:"
            elif rawPhase == "First Quarter":
                phase = ":first_quarter_moon:"
            elif rawPhase == "Waxing Gibbous":
                phase = ":waxing_gibbous_moon:"
            else:
                phase = "Cannot be divined."

        else:
            phase = "Cannot be divined."

        return phase

    except:
        return "Cannot be divined."

    return phase

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

# ---------------------------
# Command: Reset
# ---------------------------
def cmd_reset(message):
    global reset_users
    if message.author.name in reset_users:
        sys.exit(2)
    else:
        return "Can't let you do that, StarFox"

# ---------------------------
# Command: Mute
# ---------------------------
def cmd_mute(message):
    global mute_admins
    global muted_users
    if message.author.name in mute_admins:
        MUTEname =  message.content.encode('utf-8')[6:]
        if MUTEname in mute_admins:
            return "You can't mute an admin"
        if MUTEname in muted_users:
            muted_users.remove(MUTEname)
            return MUTEname + " has been unmuted"
        else:
            muted_users.append(MUTEname)
            return MUTEname + " has been muted"
    else:
        return "Can't let you do that, StarFox"
		
# ---------------------------
# Command: Add Mute Admin
# ---------------------------
def cmd_addadmin(message):
    global mute_admins
    global reset_users
    global muted_users
    if message.author.name in reset_users:
        newAdmin = message.content.encode('utf-8')[7:]
        if newAdmin in muted_users:
            return "You can't make a muted user an admin"
        if newAdmin in reset_users:
            return "You can't change the admin status of an owner"
        if newAdmin in mute_admins:
            mute_admins.remove(newAdmin)
            return newAdmin + " can no longer mute others"
        else:
            mute_admins.append(newAdmin)
            return newAdmin + " can now mute others"
    else:
        return "Can't let you do that, StarFox"
        
# ---------------------------
# Command: Clear Mute List
# ---------------------------
def cmd_clearmute(message):
    global mute_admins
    global muted_users
    if message.author.name in mute_admins:
        muted_users = []
        return "All muted users have been unmuted"
    else:
        return "Can't let you do that, StarFox"
        		
# ---------------------------
# Command: Ping Me
# ---------------------------
def cmd_ping(message):
    return 'Pinging {0.author.mention}'.format(message)

# ---------------------------
# Command: Card Image
# ---------------------------
def cmd_image(message):
    global last_card
    if last_card is not None:
        name = last_card['name'].encode('utf-8')
        url = 'http://gatherer.wizards.com/Handlers/Image.ashx?name={0}&type=card'
        return url.format(name).replace(' ', '+')
    else:
        return 'You must divine a single entity first.'

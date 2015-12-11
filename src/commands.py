# ---------------------------
# Imports
# ---------------------------
import re
import subprocess
import json
import sys
import cards
import banlists

# ---------------------------
# Globals
# ---------------------------
version_number = 'v0.8'
last_card = None
reset_users = ['Gerst','ace','Lerker','Shaper']
obey_dict = {
        'Shaper': 'I obey, Master Shaper.',
        'ace': 'I obey, Admiral Ace.',
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
        'K-Ni-Fe': 'I obey, because I\'m 40\% Potassium, Nickel and Iron.'
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
        if len(queries) == 1 and len(card_list) == 1:
            last_card = card_list[0]
            response += cards.get_card(message, card_list[0])
            continue

        # If no cards are found, we are done
        if len(card_list) == 0:
            response += '**' + query + '**: *The ritual summoned nothing but ash...*'
            continue

        # If an exact card is found, just print that one
        # When you find the exact match, break out of the for card in cards loop
        # Then "continue" the for s in queries to move to the next query
        # If you find an exact match and there is only 1 query in the buffer, 
        # Get the details and rulings of the exact card, as they are skipped when mtg cli returns multiple
        done = False
        for card in card_list:
            if (card['name'].encode('utf-8').lower() == query.lower()):
                response += cards.get_card(message, card)
                if len(queries) == 1:
                    newProcess = subprocess.Popen(['mtg', query, '--json', '--exact'], stdout=subprocess.PIPE)
                    newResult = str(newProcess.communicate()[0])
                    newList = json.loads(newResult)
                    last_card = newList[0]
                done = True
                break
        if done:
            continue

        # If more than 8 cards are found, don't spam chat
        if len(card_list) > 8:
            response += 'The incantations are too long; read them yourself'
            continue

        # Finally, if we've gotten to here, print all the cards
        for card in card_list:
            response += cards.get_card(message, card)

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
        return ''



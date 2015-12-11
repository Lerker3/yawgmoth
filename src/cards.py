# ---------------------------
# Imports
# ---------------------------
import re

# ---------------------------
# Get Card
# ---------------------------
def get_card(message, card):
    response = '**' + card['name'].encode('utf-8') + '**'
    if 'mana_cost' in card:
        response += ' (' + card['mana_cost'].encode('utf-8') + ')'
    response += '\n'
    if 'types' in card:
        for t in card['types']:
            response += t.encode('utf-8') + ' '
    if 'subtypes' in card:
        response += "-- "
        for st in card['subtypes']:
            response += st.encode('utf-8') + ' '
    if 'power' in card:
        response += '[' + re.sub('\*','\\\*',card['power']).encode('utf-8') + '/'
        response += re.sub('\*','\\\*',card['toughness']).encode('utf-8') + ']'
    if 'loyalty' in card:
        response += '[' + card['loyalty'].encode('utf-8') + ']'
    response += '\n'
    if 'rules_text' in card:
        for r in card['rules_text'].encode('utf-8').split(';'):
            response += r.strip() + '\n'
    return response

# ---------------------------
# Get Card Details
# ---------------------------
def get_card_details(message, card):
    response = '**' + card['name'].encode('utf-8') + '**\n'
    if 'artist' in card:
        response += 'Artist: ' + card['artist'].encode('utf-8')
    response += '\n'
    if 'community_rating' in card:
        response += 'Community Rating: ' + card['community_rating'].encode('utf-8')
    response += '\n'
    if 'printings' in card:
        response += 'Printings: '
        response += '\n'
        for printing in card['printings']:
            response += '- ' + printing[0].encode('utf-8') + ' (' + printing[1].encode('utf-8') + ')'
            response += '\n'
    return response

# ---------------------------
# Get Card Rulings
# ---------------------------
def get_card_rulings(message, card):
    response = '**' + card['name'].encode('utf-8') + '**\n'
    if 'ruling_data' in card:
        for ruling in card['ruling_data']:
            response += '- ' + ruling[1].encode('utf-8') + ' (' + ruling[0].encode('utf-8') + ')'
            response += '\n'
    return response


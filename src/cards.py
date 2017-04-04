# ---------------------------
# Imports
# ---------------------------
import re

# ---------------------------
# Get Card
# ---------------------------
def get_card(message, card):
    response = '**' + card['name'] + '**'
    if 'mana_cost' in card:
        response += ' (' + card['mana_cost'] + ')'
    response += '\n'
    if 'types' in card:
        for t in card['types']:
            response += t + ' '
    if 'subtypes' in card:
        response += "-- "
        for st in card['subtypes']:
            response += st + ' '
    if 'power' in card:
        response += '[' + re.sub('\*','\\\*',card['power']) + '/'
        response += re.sub('\*','\\\*',card['toughness']) + ']'
    if 'loyalty' in card:
        response += '[' + card['loyalty'] + ']'
    response += '\n'
    if 'rules_text' in card:
        for r in card['rules_text'].split(';'):
            response += r.strip() + '\n'
    return response

# ---------------------------
# Get Card Details
# ---------------------------
def get_card_details(message, card):
    response = '**' + card['name'] + ' (Details)**\n'
    if 'artist' in card:
        response += 'Artist: ' + card['artist']
    response += '\n'
    if 'community_rating' in card:
        response += 'Community Rating: ' + card['community_rating']
    response += '\n'
    if 'printings' in card:
        response += 'Printings: '
        response += '\n'
        for printing in card['printings']:
            response += '- ' + printing[0] + ' (' + printing[1] + ')'
            response += '\n'
    return response

# ---------------------------
# Get Card Rulings
# ---------------------------
def get_card_rulings(message, card):
    response = '**' + card['name'] + ' (Rulings)**\n'
    if 'ruling_data' in card:
        for ruling in card['ruling_data']:
            response += '- ' + ruling[1] + ' (' + ruling[0] + ')'
            response += '\n'
    return response


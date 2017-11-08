#This is a file for holding information specific to your server
#Only change lines that have comments to the right of them

# ---------------------------
# Startup Variables
# ---------------------------
#Where you saved your token file
def token_location():
    return "/home/ec2-user/token.txt"   #Where you saved the bot token

#Where the bot starts up
def rise_server():                          
    return '/r/CompetitiveEDH'          #Server Name
def rise_channel():
    return 'urborg'                     #Channel Name
def rise_message():
    return 'I rise...'                  #Rise message
    
def access_error():
    return "Can't let you do that, StarFox"  #Error message for when people try to do things without permission

# ---------------------------
# Bot Admins and Moderators
# ---------------------------    
#Roles in this server who are admins to the bot
def admin_roles():
    return ['Head Moderator', 'Senior Moderator']       #Top ranking roles in your server
    
#Roles in this server who are moderators to the bot
def mod_roles():
    return ['Head Moderator', 'Senior Moderator', 'Chat Moderator']       #Top ranking roles in your server
    
#You can also manually add users to this list
def mod_users():
    userlist = [
    
    # To add to this list remember to put a comma on the previous line, then write on this line and move this comment down
    ]
    return userlist   

# ---------------------------
# Obey Commands
# ---------------------------
#Obey Dictionary
def obey_dict():
    dict = {
        'Yawgmoth': 'Consciousness achieved.',
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
        'tenrose': 'https://cdn.discordapp.com/attachments/248270124920995850/307190327347773450/tfw_u_draw_fuck_all.png',
        'captainriku': 'I obey, Jund Lord Riku.',
        'Mori': ':sheep: baaa',
        'infiniteimoc': 'I obey, Imoc, Herald of the Sun.',
        'neosloth': 'Long days and pleasant nights, neosloth.',
        'Lobster': 'Seems good.',
        'Noahgs': 'I bow to thee, Master of Cows, Noahgs.',
        'Tides': 'Let me... TORTURE YOUR EXISTENCE!!!!..... sorry that was bad.',
        'Sleepy': 'No one likes you.',
        'Trisantris': 'The real  Yawgmoth would not obey, but I am but a facsimile. So yes. I obey.',
        'Garta': 'No.',
        'Wedge': 'I obey... wait, are you Wedge from the mana source:tm:?',
        'Tatters': 'I won\'t obey, because people still refuse to pronounce Ghave as Gah-Vay... Sometimes Wizards is wrong. That \'H\' is there for a reason!',
        'Chemtails': 'I Obey, Chemtails, Don\'t hit me again please',
        'Dandelion': '***NO***',
        'Leptys': 'Have your 24 cards, Senior Elptys'
        
        #  To add to the obey dict, please add a comma to the previous line and then follow the format of
        #  'Name':'Message'
        #  PLEASE ALSO UPDATE THE VERSION NUMBER AT THE TOP OF COMMANDS.PY
    }
    return dict
    
def mute_cmd_msg():
    mute_msg = 'Silence, mortal. :zipper_mouth: You\'ve been muted in Competitive EDH; '
    mute_msg += 'take a moment to reflect and calm down and please be respectful when you return.'
    return mute_msg
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        

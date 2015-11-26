import subprocess
#import codecs
import discord
#import time

# ---------------------------
# Initialize
# ---------------------------
Y = discord.Client()
Y.login('EMAIL', 'PASSWORD')

@Y.event
def on_ready():
   sEDH = Y.servers[0]
   cMain = sEDH.channels[0]
   print('I serve...')
   print('------')
   print('User:' + '\t\t' + Y.user.name)
   print('ID:' + '\t\t' + Y.user.id)
   print('Server:' + '\t\t' + sEDH.name + ", " + sEDH.id)
   print('------')
   #print cMain.name
   #for s in Y.servers:
   #       print s.name


   Y.send_message(cMain, 'I rise...')

# ---------------------------
# Commands
# ---------------------------
@Y.event
def on_message(message):
   # -----------------------
   # !obey
   # -----------------------
   if message.content.startswith('!obey'):
      if message.author.name.startswith('Shaper'):
         Y.send_message(message.channel, 'I obey, master Shaper.')
      elif message.author.name.startswith('ace'):
         Y.send_message(message.channel, 'I obey, as commanded.')
      elif message.author.name.startswith('JimWolfie'):
         Y.send_message(message.channel, 'Suck my necrotic dick, Jim.')
      elif message.author.name.startswith('ShakeAndShimmy'):
         Y.send_message(message.channel, 'I obey, Chancellor ShakeAndShimmy.')
      else:
         Y.send_message(message.channel, 'I will not obey, mortal.')

   # -----------------------
   # +card
   # -----------------------
   if message.content.startswith('+'):

      query = str(message.content[1:]).encode('utf-8') # input cleansing     
      

      # this sort of helps debug the string encoding issue
      #
      #io = subprocess.Popen(["mtg", query], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
      #time.sleep(3)
      #print io.communicate()

      card = subprocess.check_output(["mtg", query]).encode('utf-8') 
      print card

      if len(card) < 1000:
         Y.send_message(message.channel, card)
      else:
         Y.send_message(message.channel, "The incantations are too long; read them yourself.")

Y.run()

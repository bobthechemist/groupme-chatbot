from groupy import Client 
import os
import subprocess
from secrets import secrets
from wolframclient.evaluation import WolframLanguageSession
from wolframclient.language import wl


class myGroupMe(Client):
  def __init__(self):
    self.client = Client.from_token(secrets["GMTOKEN"])
    self.group = self.client.groups.get(secrets["GROUPID"])
    self.messages = self.group.messages
    self.bot = self.getBot(secrets["BOTID"])
    self.last_message_id = self.getCurrentMessageID()
    self.wls = WolframLanguageSession('/usr/bin/wolfram')
    self.startWolframSession()

  def getBot(self, botid):
    '''Return the requested bot'''
    response = filter(lambda x: x.bot_id == botid, self.client.bots.list())
    return list(response)[0]


  # Need to process an image before posting it
  def procImages(self, *filenames):
    '''Processes images so they can be attached to a message'''
    attachments = []
    for afile in filenames: 
      with open(afile, 'rb') as f:
        attachments.append( self.client.images.from_file(f)  )
    return attachments
  
  def getCurrentMessageID(self):
    return self.messages.list()[0].id

  def listen(self):
    '''Participate in the conversation'''
    # get oldest new message, if any
    next_message = self.group.messages.list_after(self.last_message_id,limit=1)
    if len(list(next_message)) > 0:
      if self.processMessageQ(next_message[0]):
        self.runWolfram(next_message[0].text[1:])  
      self.last_message_id = next_message[0].id 

  def processMessageQ(self, message):
    '''Determine if the bot should do something with this message'''
    if message.sender_type == 'user' and message.text.startswith(">"):
      return True
    else:
      return False

  def getMessage(self, messageid):
    '''Stupid way to get a message w/o hacking groupy'''
    messages_before = self.messages.list_before(messageid, limit=1)
    message = self.messages.list_after(messages_before[0].id,limit=1)
    return message[0]

#  def runWolfram(self, query):
#    self.bot.post("I have to think about this...")
#    cmd = './str.wls "{}"'.format(query)
#    response = subprocess.check_output(cmd, shell=True)
#    if os.path.exists('out.png'):
#      self.bot.post(query, attachments=self.procImages('out.png'))
#      os.remove('out.png')
#    else:
#      #self.bot.post(cmd)
#      self.bot.post('here we go: {}'.format(response.decode("utf-8")))
  def runWolfram(self, query):
    if self.wls.started:
      response = self.wls.evaluate(wl.Part(wl.WolframAlpha(query),2,2))
      printable = False 
      if not 'head' in dir(response):
        # probably a number or string, so print it
        printable = True
      if printable:
        self.bot.post(str(response))
      else:
        self.wls.evaluate(wl.Export('out.png',wl.ReleaseHold(response)))
        if os.path.exists('out.png'):
          self.bot.post("I think this is right", attachments=self.procImages('out.png'))
          os.remove('out.png')
        else:
          self.bot.post("I can't do that")
    else:
      self.startWolframSession()

  def startWolframSession(self):
    if not self.wls.started:
      self.bot.post("Sorry, I'm just waking up.")
      self.wls.start()




gm = myGroupMe()

# Example message post with multiple images
#g.post(text="demo is working", attachments=procImages('cat.png', 'image.gif'))



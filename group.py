from groupy import Client 
import os
import subprocess
from secrets import secrets
from wolframconnector import *
from chatterbotconnector import *

class myGroupMe(Client):
  def __init__(self):
    self.client = Client.from_token(secrets["GMTOKEN"])
    self.group = self.client.groups.get(secrets["GROUPID"])
    self.messages = self.group.messages
    self.bot = self.getBot(secrets["BOTID"])
    self.last_message_id = self.getCurrentMessageID()
    self.wc = WolframConnector()
    self.cc = ChatBotConnector()

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
        #TODO: Replace with query selection processor
        query = str(next_message[0].text[1:])
        (response, attachments) = self.queryProcessor(query)
        if response == None:
          response = "Steve doesn't know that."
        self.bot.post(response, attachments = attachments)
      self.last_message_id = next_message[0].id 
  
  def queryProcessor(self, query):
    """Cycle through processors to find a result
    """
    # Check chatterbot first
    response = self.cc.get_response(query)
    attachments = None
    if response.confidence > 0.5:
      # process this response
      response = self.cc.processResponse(response.text)
    else:
      # probably not that good so head to Wolfram alpha
      (response, attachments) = self.processWolframAlphaQuery(query)
      if response == None:
        response = "I don't know that."
    return (response, attachments)

  def processWolframAlphaQuery(self, query):
    """Performs WA call and returns a message/attachment tuple
    """
    attachments = None
    response = self.wc.queryWolframAlpha(query)
    if response == '<image>' and os.path.exists(self.wc.waimage):
      attachments = self.procImages(self.wc.waimage)
      os.remove(self.wc.waimage)
      response = query # attach query text to post of image
    return (response, attachments)


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




gm = myGroupMe()

# Example message post with multiple images
#g.post(text="demo is working", attachments=procImages('cat.png', 'image.gif'))



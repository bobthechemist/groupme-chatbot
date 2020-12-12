from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.response_selection import * 
from chatterbot.comparisons import * 
import embeddedfunctions as ef
import re

class ChatBotConnector(ChatBot):
  """Child of ChatBot
  """
  def __init__(self, botname = 'bob', botdb = 'sqlite:///bobthebot.db', training = False):
    self.botname = botname
    self.botdb = botdb
    self.readonly = not training
    super().__init__(botname,
      logic_adapters=[
        {
          'import_path': "chatterbot.logic.BestMatch",
          'response_selection_method': get_random_response,
        }
      ],
      statement_comparison_function = levenshtein_distance,
      database_uri = botdb,
      read_only = self.readonly)
    if training:
      self.trainer = ChatterBotCorpusTrainer(self)
    else:
      self.trainer = None

  def processResponse(self, response):
    """Replaces function placeholders with the result of the embedded function
    """
    responseString = response
    functions = re.findall('<\?(.*?)\((.*?)\)\?>', responseString)
    for f in functions:
      if f[0] in ef.commands:
        kwargs = eval("dict(%s)"%f[1])
        subpattern = ef.commands[f[0]](**kwargs)
      else:
        subpattern = "?" + f[0] + "(" + f[1] + ")?"
      responseString = responseString.replace("<?" + f[0] + "(" + f[1] + ")?>", subpattern)
    return responseString


'''
wolframconnector is a wrapper class for bot-related wolfram calls
'''
import os
from wolframclient.evaluation import WolframLanguageSession
from wolframclient.language import wl

class WolframConnector(WolframLanguageSession):
  """Wrapper for :class:`wolframclient.WolframLanguageSession` that facilitates communication as a bot

  :param kernel: location of the wolfram kernel
  :type kernel: str, optional
  :param waimage: filename for temporary image
  :type waimage: str, optional
  """
  def __init__(self,kernel='/usr/bin/wolfram', waimage = 'out.png'):
    """Constructor method
    """
    self.kernel = kernel
    self.waimage = waimage
    super().__init__(self.kernel)
    # Is there ever a time when we do *not* want to start the session?
    self.start() 

  def startWolframSession(self):
    """Starts the wolfram session if it is not already started.
    """
    if not self.started:
      self.start()

  def queryWolframAlpha(self, query):
    """Executes a wolfram alpha query on argument

    :param query: Query text
    :type query: str, required
    """
    if self.started:
      response = self.evaluate(wl.Quiet(wl.Part(wl.WolframAlpha(query),2,2)))
      if not 'head' in dir(response):
        # probably a number or a string, so can be returned as is
        return str(response)
      elif response.head.name == 'Part':
        # WolframAlpha has no response
        return None
      else:
        # response is graphical in nature, so create image
        # TODO: Raise exception if self.wlimage exists
        self.evaluate(wl.Export(self.waimage,wl.ReleaseHold(response)))
        return '<image>'
        



def nexttestdate(**kwargs):
  """description
  """
  return str(kwargs['a'] + kwargs['b'])

def nextquizdate(**kwargs):
  """description
  """
  return str(43)

def testtopics(**kwargs):
  """description
  """
  return str(44)

def nextassignment(**kwargs):
  """description
  """
  return str(45)

def currenttopic(**kwargs):
  """description
  """
  return str(46)


commands = {
  'nexttestdate':nexttestdate,
  'nextquizdate':nextquizdate,
  'testtopics': testtopics,
  'nextassignment': nextassignment,
  'currenttopic': currenttopic
}

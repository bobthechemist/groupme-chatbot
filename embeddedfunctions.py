import os
import pandas
from datetime import date, timedelta

# Embedded function definitions must preceed function dictionary
# TODO Optimize schedule use as it is currently read for each call
# TODO Design return strings to contain only lookup values, leave text to the chatbot
#      Use kwargs to denote which value is being returned, perhaps, or return an array
#      that can be incorporated into format

def nexttestdate(**kwargs):
  """description
  """
  df = importSchedule('./data/schedule.csv')
  obj = getNextObject(df,'test', date.today())
  return 'The next test is {}.'.format(obj['Date'].strftime("%A, %B %d"))

def nextquizdate(**kwargs):
  """description
  """
  df = importSchedule('./data/schedule.csv')
  obj = getNextObject(df,'quiz', date.today())
  return '{}'.format(obj['Date'].strftime("%A, %B %d"))

def testtopics(**kwargs):
  """description
  """
  return str(44)

def nextassignment(**kwargs):
  """description
  """
  df = importSchedule('./data/schedule.csv')
  obj = getNextObject(df,'homework', date.today())
  return 'due {} at {}. The assignment is to {}.'.format(
    obj['Date'].strftime("%A, %B %d"), obj['Time'], obj['Content'])
  
def currenttopic(**kwargs):
  """description
  """
  df = importSchedule('./data/schedule.csv')
  obj = getNextObject(df,'topic', date.today()-timedelta(1))
  return '{}, which can be found in {} of your textbook.'.format(
    obj['Content'], obj['Comment'])


commands = {
  'nexttestdate':nexttestdate,
  'nextquizdate':nextquizdate,
  'testtopics': testtopics,
  'nextassignment': nextassignment,
  'currenttopic': currenttopic
}

def importSchedule(csv):
  if os.path.exists(csv):
    df = pandas.read_csv(csv)
    df['Date'] = pandas.to_datetime(df.Date).dt.date
    return df
  else:
    return None

def getNextObject(dframe, obj, ctime):
  """Find the next occurance of obj in the schedule found in dframe
  """
  df = dframe[(dframe['Object']==obj) & (dframe['Date'] > ctime)]
  return df.sort_values('Date', ignore_index = True).iloc[0]

df = importSchedule('./data/schedule.csv')

from group import *
from time import sleep

gm.bot.post("I'm joining the conversation")
while True:
  try:
    gm.listen()
    sleep(1)
  except (KeyboardInterrupt, EOFError, SystemExit):
    gm.bot.post("Nap time - See you later!")
    gm.wc.stop()
    break


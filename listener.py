from group import *
from time import sleep

while True:
  try:
    gm.listen()
    sleep(1)
  except (KeyboardInterrupt, EOFError, SystemExit):
    gm.wls.stop()
    break


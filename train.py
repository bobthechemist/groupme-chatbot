from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

cb = ChatBot('bob',
  database_uri= "sqlite:///bobthebot.db")

trainer = ChatterBotCorpusTrainer(cb)
trainer.train(
  "./corpus/"
  )
#trainer.export_for_training('./bobthebot.json')

print("training done")

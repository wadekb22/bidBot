import discord
import os
from replit import db
from keep_alive import keep_alive

upvotes_to_support = 3

class MyClient(discord.Client):
  async def on_ready(self):
    print('Logged in as ', self.user)

  async def on_disconnect(self):
    print('Bot ', self.user, ' has disconnected')

  async def on_message(self, message):
    if message.author == self.user:
      return
    if message.content.startswith('~bid'):
      if(bid_correct_form(message)):
        await message.add_reaction('⭐')
        await message.channel.send('A user has been nominated for their bad decision. Upvote the :star: emote to support this nomination!')
      else:
        await message.channel.send('Invalid format. Nomination must be in format `~bid {@name} [space seperated other @names] {points} {reason}`')
    if message.content.startswith('~pr'):
      info = order_ranking()
      place = 1
      for i in info:
        await message.channel.send(f'Place {place}: {i["user"]} with {i["points"]} points. Reasons include: {i["reasons"]}')
        place += 1
    if message.content.startswith('~reset'):
      if message.author.top_role.name == "certified ape":
        clear_db()
    if message.content.startswith('~help'):
      await message.channel.send("`~bid`\tReport a bad decision\n`~pr`\tView current power rankings")

  async def on_reaction_add(self, reaction, user):
    if reaction.emoji == '⭐' and reaction.count > upvotes_to_support:
      if(bid_correct_form(reaction.message)):
        for dec in bid_decompose(reaction.message):
          add_decision(dec)

def add_decision(decision):
  if decision["user"] in db.keys():
    if decision["reason"] in db[decision["user"]][1:]:
      old = db[decision["user"]]
      old[0] = old[0] + decision["points"]
      old.append(decision["reason"])
      db[decision["user"]] = old
  else:
    db[decision["user"]] = [decision["points"], decision["reason"]]

def clear_db():
  for user in db.keys():
    del db[user]

def order_ranking():
  info = []
  for user in db.keys():
    temp = {}
    temp["user"] = user
    temp["points"] = db[user][0]
    temp["reasons"] = " / ".join(db[user][1:])
    info.append(temp)
  info.sort(reverse=True, key=sort_func)
  return info
  
def sort_func(dic):
  return dic["points"]

def bid_correct_form(message):
  if len(message.mentions) < 1:
    return False
  try:
    bid_decompose(message)
  except:
    return False
  return True


def bid_decompose(message):
  rtrn = []
  scale = len(message.mentions)
  for i in range(scale):
    temp = {}
    msg = message.content.split()

    temp["user"] = message.mentions[i].name

    points = int(msg[scale+1])
    if points < 3:
      temp["points"] = 1
    elif points < 5:
      temp["points"] = 3 
    else:
      temp["points"] = 5
    
    temp["reason"] = " ".join(msg[scale+2:])

    rtrn.append(temp)

  return rtrn


client = MyClient()

keep_alive()
client.run(os.getenv('TOKEN'))

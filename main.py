from csb_cmd.common import *

reactions = {
  "perry" : [387317882398441483],
  "huel": [253088742821068801]
}

reaction_emojis = {}

async def react(message):
  for reaction in message.reactions:
    if (reaction.me):
      return
  emoji = reaction_emojis.get(message.author.id)
  if emoji is not None:
    return await message.add_reaction(emoji)

is_ready = False



@client.event
async def on_ready():
  print('Bot logged in as {0.user}'.format(client))

  for emoji in client.emojis:
    users = reactions.get(emoji.name)
    if users is not None:
      for user in reactions.get(emoji.name):
        reaction_emojis[user] = emoji
  print('Emojis loaded')

  for channel_group in client.get_all_channels():
    txt = None
    try:
      txt = channel_group.text_channels
    except:
      continue
    for channel in channel_group.text_channels:
      if client.user not in channel.members:
        continue
      print('Populating ' + channel.name)
      async for msg in channel.history(limit=None):
        await react(msg)

  print('Finished Populating!')
  is_ready = True
  os.remove("canary")

client.run(token)

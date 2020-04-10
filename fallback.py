import discord
from discord.ext import commands
import os
import subprocess

# Please keep in mind that the structure of the csv file might change with time :(
# So keep it up to date new comitte people :P

token = open("token.txt","r").read()
client = commands.Bot(command_prefix='$')

def check_user(user):
  for guild in client.guilds:
    for role in guild.roles:
      if role.name == "Bot Supervisor":
        if user in role.members:
          return True;
  return False;

@client.event
async def on_message(msg):
  if not check_user(msg.author):
    return
  response = subprocess.check_output(["git", "reset", "--hard", msg.content]).decode('utf8')
  await msg.author.send("```\n" + response + "```")
  await client.logout()

@client.event
async def on_ready():
  print('PANIC!!!')
  safe = os.system("git merge-base --is-ancestor master bak") != 0;
  message = None
  if (safe):
    os.system("git reset --hard bak");
    message = "Canary failed. Reverting to backup"

  for guild in client.guilds:
    for role in guild.roles:
      if role.name == "Bot Supervisor":
        for i in role.members:
          await i.send(message)
  if (safe):
    await client.logout()

client.run(token)

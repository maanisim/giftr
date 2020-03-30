from csb_cmd.common import *
from csb_cmd.db import db
from csb_cmd.pubkey import decrypt
from csb_cmd import mail

import random
class AdminCommands(commands.Cog, name="Controller commands"):
  async def cog_check(self, ctx):
    role = discord.utils.get(ctx.guild.roles, name=botAdmin);
    return role in ctx.author.roles

  @commands.command(help="Sends tail of log to the user")
  async def log(self, ctx):
    file = open(log_path, "r")
    await ctx.author.send("```\n" + file.read()[-1980:] + "```");
    await ctx.send("Log has been sent!");

  @commands.command(help="Sends whole log file to the user")
  async def whole_log(self, ctx):
    await ctx.author.send(file=discord.File(log_path));
    await ctx.send("Log has been sent!");


  @commands.command(help="Causes bot crash")
  async def crash(self, ctx):
    if (ctx.author.id == 387317882398441483):
      await ctx.send("Your permission rank is too low!")
      return
    file = open("canary", "w+");
    arrayOfDeaths = ["killed by a kitten while helpless.","choked to death on a fortune cookie","killed by a little dog called Sirius","killed by an orc mummy, while trying to turn the monsters"]
    await ctx.send(arrayOfDeaths[random.randint(0,(len(arrayOfDeaths)-1))])
    await client.logout()

  @commands.command(help="Turns off the bot")
  async def stop(self, ctx):
    file = open("stop", "w+");
    await ctx.send(":sob:")
    await client.logout()

  @commands.command(help="Forces bot restart")
  async def restart(self, ctx):
    await ctx.send("Restarting!");
    await client.logout()

  @commands.command(help="Adds the token with the given name and encrypted pubkey to the token list")
  async def add_token(self, ctx, name, tok):
    db.set_token(name, decrypt(tok))

  @commands.command(help="pls no abuse")
  async def email(self, ctx, target):
    mail.send(target, "Test", "Test message from {}".format(ctx.author.name))
admin_impl = AdminCommands()

from csb_cmd.common import *
from csb_cmd.db import db

import requests
import tempfile
import os
import subprocess
import time

#TODO: ratelimit
#TODO: wait for complete async, to not freeze up bot

csb_basepath = os.path.expanduser("~/.csb_utils/")
os.makedirs(csb_basepath, exist_ok=True)

rockyou_path = csb_basepath+"/rockyou.txt"
rockyou_gz_url = "https://c3murk.dev/ext/rockyou.txt.gz"
if not os.path.exists(rockyou_path):
  print("Downloading rockyou")
  open(rockyou_path+'.gz', "+wb").write(requests.get(rockyou_gz_url, allow_redirects=True).content)
  subprocess.check_output(['gzip', '-d', rockyou_path + '.gz'])

john_path = csb_basepath+"/john"
john_url = "https://c3murk.dev/tool/x64/john"
if not os.path.exists(john_path):
  print("Downloading john")
  open(john_path, "+wb").write(requests.get(john_url, allow_redirects=True).content)
  os.chmod(john_path, 0o700)

ratelimits = dict()

block = False
class HashCommands(commands.Cog, name="Hash commands"):
  async def cog_check(self,ctx):
    if block == False:
      ratelimit_react = client.get_emoji(666255541722677268)
      last = ratelimits.get(ctx.author.id)
      ratelimits[ctx.author.id] = int(time.time())
      if not (last is not None and ratelimits[ctx.author.id] - last < 5): # 5 second timeout
        await ctx.message.add_reaction(ratelimit_react)
        return True
      return False

  @commands.command(help="looks up a hash on hashes.org")
  async def crack(self, ctx, *hashes):
    params = {
      "key": db.get_token("hashes.org"),
      "query": ",".join(hashes)
    }
    r = requests.get("https://hashes.org/api.php", params=params).json()
    colour = None
    if (r["status"] == "success"):
      colour = 0x00FF00 # GREEN
    else:
      colour = 0xFF0000 # RED
    embed = discord.Embed(title="Hashes.org results", colour=discord.Colour(colour))

    for key, result in r["result"].items():
      if result is not None:
        embed.add_field(name="`" + key + "` ("+result["algorithm"]+")", value="```Fix\n"+result["plain"]+"```", inline=False)
      else:
        embed.add_field(name="`"+key+"`", value="**Not found**", inline=False)

    await ctx.send(embed=embed)

  @commands.command(help="Uses johntheripper for *10* seconds MAX")
  async def john(self, ctx, hash_type, *hashes):
    file = tempfile.NamedTemporaryFile()
    for i in hashes:
      file.write((i+":"+i+"\n").encode())
    file.flush() # XD
    res = None
    try:
      await system_result_to([
        john_path, '--wordlist='+rockyou_path, "--rules=none", file.name, "--log-stderr",
        "--format="+hash_type, "--no-log", "--pot="+csb_basepath+"/john.pot", "--session="+file.name # john adds a .rec to it
      ], 5)
      res = await system_result([john_path, "--format="+hash_type, "--show", file.name, "--pot="+csb_basepath+"/john.pot"]);
    except: pass
    msg = None
    if res is None:
      return await ctx.send("Bad arguments")

    lines = res.split('\n')

    embed = discord.Embed(title="JohnTheRipper results", colour=discord.Colour(0x00FF00))
    for i in lines[0:-3]:
      kvp = i.split(':')
      embed.add_field(name="`"+kvp[0]+"`", value="```Fix\n"+kvp[1]+"\n```", inline=False)
    embed.add_field(name="Summary", value=lines[-2], inline=False)
    await ctx.send(embed=embed)

hash_impl=HashCommands()

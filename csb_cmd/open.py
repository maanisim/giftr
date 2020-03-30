from csb_cmd.common import *
from csb_cmd.pubkey import get_pubkey
import requests
from bs4 import BeautifulSoup
from tabulate import tabulate

class OpenCommands(commands.Cog, name="Open commands"):
  @commands.command(help="<arg1 = uni_username> <arg2 = dob>")
  async def verify(self, ctx, arg1, arg2):
    await ctx.message.delete()
    print("User {} tried to authenticate with {}".format(arg1, arg2))
    if(25 >= len(arg1) and 10 >= len(arg2)):
      role = discord.utils.get(ctx.guild.roles, name=userType)
      if role in ctx.author.roles:
        await ctx.send("You already have the role!")
      else:
        f=open(usersFile,"r")
        for line in f.readlines()[1:]:
          myLine = line.split(",")
          if(arg1 == myLine[2] and arg2 == myLine[5] and memberType == myLine[7]):
            with open(blackList, "r+") as file:
              for line in file:
                if (myLine[2]+","+myLine[5]) in line:
                  usedLine = line.split(",")
                  await ctx.send("Those credentials have been used by "+usedLine[2])
                  file.close()
                  break
              else:
                file.write(myLine[2]+","+myLine[5]+","+format(ctx.message.author.mention)+ "\n")
                print("Give user")
                member = ctx.message.author
                await ctx.message.author.add_roles(role)
                await ctx.send("Your role has been updated")
                break
              if(arg1 == myLine[2] and "Temporarily Free Membership" == myLine[7]):
                await ctx.send("Free users are not entitled to the member role!")
                break

  @commands.command(help="<arg1 = uni_username> <arg2 = dob>")
  async def verifyTest(self, ctx, arg1, arg2):
    await ctx.message.delete()
    print("User {} tried to authenticate with {}".format(arg1, arg2))
    if(25 >= len(arg1) and 10 >= len(arg2)):
      role = discord.utils.get(ctx.guild.roles, name=userType)
      if role in ctx.author.roles:
        await ctx.send("You already have the role!")
      else:
        f=open(usersFile,"r")
        for line in f.readlines()[1:]:
          myLine = line.split(",")
          if(arg1 == myLine[2] and arg2 == myLine[5] and memberType == myLine[7]):
            with open(blackList, "r+") as file:
              for line in file:
                if (myLine[2]+","+myLine[5]) in line:
                  usedLine = line.split(",")
                  await ctx.send("Those credentials have been used by "+usedLine[2])
                  file.close()
                  break
              else:
                file.write(myLine[2]+","+myLine[5]+","+format(ctx.message.author.mention)+ "\n")
                print("Give user")
                member = ctx.message.author
                await ctx.message.author.add_roles(role)
                await ctx.send("Your role has been updated")
                break
              if(arg1 == myLine[2] and "Temporarily Free Membership" == myLine[7]):
                await ctx.send("Free users are not entitled to the member role!")
                break
 
  @commands.command(help="Lists current cyber events")
  async def events(self, ctx):
    page = requests.get('https://www.cybersoc.cf/events/')
    soup = BeautifulSoup(page.text, 'html.parser')
    eventsTable = soup.find(class_='page__content')
    events = []
    i = 0
    for td in eventsTable.find_all("td"):
      if (i == 0):
        events.append([])
      if (i != 4):
        events[-1].append(td.get_text())
      i=(i+1)%5
    await ctx.send("```haskell\n" + tabulate(events, ["What", "Date", "Time", "Where"]) + "```")

  @commands.command(help="Lists all of the resources")
  async def resources(self, ctx):
    await ctx.send("Check out <https://www.cybersoc.cf/resources/> or #resources")

  @commands.command(help="Link to invite new people")
  async def invite(self, ctx):
    await ctx.send("https://discordapp.com/invite/p6qGd3D")

  @commands.command(help="I agree to ..")
  async def readme(self, ctx):
    await ctx.send("https://www.cybersoc.cf/code-of-conduct/")

  @commands.command(hidden=True)
  async def version(self, ctx):
    await ctx.send("Nope");

  @commands.command(help="Disclaimer")
  async def disclaimer(self, ctx):
    await ctx.send("Cybersecurity Society does not endorse the above message")

  @commands.command(help="You probably don't need this")
  async def pubkey(self, ctx):
    await ctx.author.send("```\n" + get_pubkey() + "\n```")

open_impl = OpenCommands()

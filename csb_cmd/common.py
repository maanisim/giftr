import discord
import os
import sys
from discord.ext import commands
from itertools import (takewhile,repeat)
import subprocess
import asyncio
import shlex

token = open("token.txt","r").read()
client = commands.Bot(command_prefix=os.getenv("CYBERSOCBOT_PREFIX", '$'))
usersFile = "c.csv"
blackList = "used.txt"
memberType = "Member"
userType = "Member"
botAdmin = "Bot Supervisor"
log_path = "cybersocbot.log"


async def system_result(command):
  proc = await asyncio.create_subprocess_exec(command[0], *command[1:], stdout=asyncio.subprocess.PIPE)
  stdout,_ = await proc.communicate()
  return stdout.decode()

async def system_result_to(command, timeout = 10):
  proc = await asyncio.create_subprocess_exec(command[0], *command[1:], stdout=asyncio.subprocess.PIPE)
  stdout,_ = await asyncio.wait_for(proc.communicate(), timeout)
  return stdout.decode()

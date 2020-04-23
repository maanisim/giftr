from csb_cmd.common import *
from csb_cmd.admin import admin_impl

async def get_version():
  return await system_result(["git", "rev-parse", "HEAD"])

async def get_checkpoint():
  return await system_result(["git", "rev-parse", "bak"])


class GitCommands(commands.Cog, name="Git commands"):
  async def cog_check(self, ctx):
    role = discord.utils.get(ctx.guild.roles, name=botAdmin);
    return role in ctx.author.roles

  @commands.command(help="Creates a git checkpoint")
  async def checkpoint(self, ctx):
    os.system("git branch -f bak HEAD")
    await ctx.send("Checkpoint created!")

  @commands.command(help="Reverts to last git checkpoint")
  async def revert(self, ctx):
    os.system("git reset --hard bak")
    await admin_impl.restart(ctx)

  @commands.command(help="Provides git info on version/checkpoint")
  async def git(self, ctx):
    await ctx.send("Version: `{}`Checkpoint: `{}`".format(await get_version(), await get_checkpoint()))
    
  @commands.command(help="Updates bot to the current git version")
  async def update(self, ctx):
    if (os.system("git fetch; git reset --hard origin/$(git rev-parse --abbrev-ref HEAD)") != 0):
      await ctx.send("Git pull failed")
    else:
      await admin_impl.restart(ctx)
  @commands.command(help="start backend")
  async def start(self, ctx):
    await ctx.send("python3 /home/web/giftr/backend/backend.py")
  @commands.command(help="kill backend")
  async def kill(self, ctx):
    await ctx.send("kill $(ps aux | grep 'backend.py' | awk '{print $2}')")

  @commands.command(help="Updates bot to the current git version")
  async def checkout(self, ctx, branch):
    if (subprocess.run(["git", "checkout", branch]).returncode != 0):
      await ctx.send("Git checkout failed")
    else:
      await ctx.send("Git checkout succeeded")

git_impl = GitCommands()

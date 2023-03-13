import os
import discord
from discord.ext import commands
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    
@bot.command()
async def ping(ctx):
    embed = discord.Embed(title="🏓 Pong!", color=0xC9E358)
    embed.set_footer(text="This was sent by the Developer Team Bot!")
    await ctx.send(embed=embed)

@bot.command()
async def hello(ctx):
    user = ctx.author
    user_id = user.id
    embed = discord.Embed(title="👋 Hola!", description=f"Hello <@{user_id}>!", color=0xFF5733)
    embed.set_footer(text="This was sent by the Developer Team Bot!")
    await ctx.send(embed=embed)
bot.run(os.environ["DISCORD_TOKEN"])

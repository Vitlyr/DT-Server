import os
from disnake.ext import commands
import disnake

bot = commands.Bot(command_prefix=commands.when_mentioned)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})\n------")

@bot.slash_command(name="hello", description="Send a friendly greeting from the bot")
async def hello(ctx: disnake.ApplicationCommandInteraction):
    user = ctx.author
    user_id = user.id
    user_name = user.name
    user_tag = user.tag
    embed = disnake.Embed(title="👋 Holá!", description=f"Hello <@{user_id}>, welcome to our server, we hope you have a great rest of your day!", color=0x808080)
    embed.set_footer(text="This was sent by the Developer Team Bot!")
    print(f"Command: Hello, User: {user_name}#{user_tag}, id: {user_id}")
    await ctx.response.send_message(embed=embed)

@bot.slash_command()
async def ban(ctx: disnake.ApplicationCommandInteraction, user: disnake.User, reason: str):
    user0 = ctx.author
    user0_id = user0.id
    user0_name = user0.name
    user0_tag = user0.tag
    # Check if the user has the "ban_members" permission
    if not ctx.author.guild_permissions.ban_members:
        return await ctx.response.send_message("You don't have permission to ban members.")
        print(f"Command: Ban, User: {user0_name}#{user0_tag}, id: {user0_id}, Status: No Permission")

    # Attempt to ban the user
    try:
        await ctx.guild.ban(user, reason=reason)
    except disnake.Forbidden:
        return await ctx.response.send_message("I don't have permission to ban that user.")
        print(f"Command: Ban, User: {user0_name}#{user0_tag}, id: {user0_id}, Status: No Bot Permission")
    except disnake.HTTPException:
        return await ctx.response.send_message("An error occurred while attempting to ban that user.")
        print(f"Command: Ban, User: {user0_name}#{user0_tag}, id: {user0_id}, Status: Error")

    # Send an embed with information about the ban
    embed = disnake.Embed(title=f"{user.name}#{user.discriminator} was banned", color=0xff0000)
    embed.set_footer(text=f"Reason: {reason}")
    await ctx.response.send_message(embed=embed)
    print(f"Command: Ban, User: {user0_name}#{user0_tag}, id: {user0_id}, Status: Banned {user.name}#{user.tag}, Banned User id: {user.id}")


if __name__ == "__main__":
    bot.run(os.getenv("TOKEN"))

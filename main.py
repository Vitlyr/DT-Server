import os
from disnake.ext import commands
import disnake
import asyncio

intents = disnake.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix=commands.when_mentioned, intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})\n------")


###Verify
rules = [
    "Rule 1: No spamming",
    "Rule 2: No hate speech",
    "Rule 3: No NSFW content",
    "Rule 4: Respect others",
]

class VerifyButton(disnake.ui.Button):
    def __init__(self):
        super().__init__(style=disnake.ButtonStyle.green, label="Agree")

@bot.slash_command(name="verify")
async def verify(ctx):
    user = ctx.author
    rules_list = "\n".join(rules)
    verify_embed = disnake.Embed(title="Welcome to the server! Please agree to the following rules to gain access to the server.\n", description=rules_list, color=0x808080)
    verify_embed.set_footer(text="This message will time out after 5 minutes of inactivity.")

    verify_button = VerifyButton()

    message = await user.send(embed=verify_embed, components=[verify_button])

    try:
        interaction = await bot.wait_for("button_click", timeout=300.0, check=lambda i: i.component.label.startswith("Agree") and i.user.id == user.id and i.message.id == message.id)
        await interaction.response.send_message('Verification Complete!', ephemeral=True)
    except asyncio.TimeoutError:
        await message.edit(content="Verification timed out. Please run the /verify command again to try again.", components=[])
    else:
        verified_role = disnake.utils.get(ctx.guild.roles, name="Verified")
        if verified_role is None:
            await ctx.send("The Verified role does not exist in this server. Please create a role with this name and try again.")
            return

        await user.add_roles(verified_role)
        await interaction.response.send_message("You have agreed to the rules and have been granted the Verified role. Welcome to the server!", ephemeral=True)
        # Notify the moderation team
        mod_channel = bot.get_channel(1050550574652858)
        embed = disnake.Embed(title=f"{ctx.author.name}#{ctx.author.discriminator} has been verified", color=0x00ff00)
        await mod_channel.send(embed=embed)

###Welcome
@bot.event
async def on_member_join(member: disnake.Member):
    embed = disnake.Embed(title="👋 Holá!", description=f"Hello {member.mention}, welcome to our server, feel free to explore the server. We hope you enjoy staying in this server.", color=0x808080)
    embed.set_footer(text="This was sent by the Developer Team Bot!")
    channel = member.guild.system_channel
    await channel.send(embed=embed)

    dm_channel = await member.create_dm()
    dm_embed = disnake.Embed(title="🎉 Welcome to our server!", description="We're happy to have you here! Make sure your verify using the </verify:1> command in <#1044858649027297280>", color=0x808080)
    dm_embed.set_footer(text="This was sent by the Developer Team Bot!")
    await dm_channel.send(embed=dm_embed)

@bot.event
async def on_member_ban(guild, user):
    # Get the reason for the ban
    async for entry in guild.audit_logs(limit=1, action=disnake.AuditLogAction.ban):
        if entry.target.id == user.id:
            reason = entry.reason
            break
    else:
        reason = "No reason given"

    # Send a DM to the banned user with the reason for their ban
    try:
        await user.send(f"You have been banned from {guild.name} for the following reason: {reason}")
    except disnake.Forbidden:
        pass # Ignore if the user has DMs disabled or the bot is blocked

@bot.slash_command(name="ban", description="Bans a user")
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
    
    # Log the ban
    print(f"Command: Ban, User: {user0_name}#{user0_tag}, id: {user0_id}, Status: Banned {user.name}#{user.tag}, Banned User id: {user.id}")


if __name__ == "__main__":
    bot.run(os.getenv("TOKEN"))

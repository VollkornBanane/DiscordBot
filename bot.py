import asyncio
from typing import List
import discord
from discord import app_commands
import discord.utils
import dateparser

# file with token inside
token = open("properties.txt").read()

intents = discord.Intents.default()
intents.message_content = True



client = discord.Client(intents=intents)

client.allowed_mentions = discord.AllowedMentions(roles=True,users=True,everyone=False)
tree = app_commands.CommandTree(client)

days = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]

@tree.command()
@app_commands.checks.has_role("Zero Magnum")
async def planner(interaction: discord.Interaction):
    if(interaction.channel.name != "weekplanner"):
        await interaction.response.send_message("Only works in weekplanner!",ephemeral=True)
        return
    
    await interaction.response.defer(ephemeral=True)
    for day in days:
        await interaction.channel.send(day)
        # avoid rate limiting
        await asyncio.sleep(0.5)
    await interaction.followup.send("Weekplanner updateted :D")


@tree.command()
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("pong")
    currUser = interaction.user
    roles = interaction.guild.roles
    role = discord.utils.get(roles,name = "Zero Magnum")
    if(role in currUser.roles):
         await interaction.channel.send("omg zm :D")


@tree.command(description="Converts Timestamps and inserts it into other text.\nUse _ as a Placeholder")
async def convert_time(interaction: discord.Interaction, ptime: str, other_text: str = "_" ,format: str = "Time & Date"):
    timestamp = dateparser.parse(ptime)
    if(timestamp == None):
        await interaction.response.send_message("Not a valid Timestamp!", ephemeral=True)
        return
    format_stamp = ""
    if(format == "Relative"):
        format_stamp = ":R"
    elif(format == "Time"):
        format_stamp = ":t"
    elif(format == "Date"):
        format_stamp = ":D"
    elif(format == "Time & Date"):
        format_stamp = ":f"
    elif(format == "Full"):
        format_stamp = ":F"
    else:
        await interaction.response.send_message("Not a valid Format!", ephemeral = True)
        return
    if("_" not in other_text):
        other_text = "_"
    output = "<t:" + str(int(timestamp.timestamp())) + format_stamp + ">"
    other_text = other_text.replace("_",output)
    await interaction.response.send_message(other_text)

@convert_time.autocomplete("format")
async def format_autocomplete(interaction: discord.Interaction, current: str)-> List[app_commands.Choice[str]]:
    formats = ["Relative", "Time", "Date", "Time & Date", "Full"]
    return [
        app_commands.Choice(name=format, value=format)
        for format in formats if current.lower() in format.lower()
    ]

@tree.error
async def on_error(interaction: discord.Interaction, error: discord.app_commands.AppCommandError):
    if(isinstance(error,discord.app_commands.MissingRole)):
        await interaction.response.send_message("Check if you have the right role for this and try again!", ephemeral=True)
        print(interaction.user.name + " tried to execute restricted command")

@client.event
async def on_ready():
    await tree.sync()
    print("Finished loading!")

client.run(token)

import discord
from discord import app_commands

token = open("properties.txt").read()

intents = discord.Intents.default()
intents.message_content = True
async def test(message):
    await message.channel.send("asdasd")



client = discord.Client(intents=intents)

tree = app_commands.CommandTree(client)

@tree.command()
async def planner(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    await interaction.channel.send("Monday")
    await interaction.channel.send("Tuesday")
    await interaction.channel.send("Wednesday")
    await interaction.channel.send("Thursday")
    await interaction.channel.send("Friday")
    await interaction.channel.send("Saturday")
    await interaction.channel.send("Sunday")
    await interaction.followup.send("Weekplanner updateted :D")


@tree.command()
async def ping(interaction: discord.Interaction):
    interaction.response.send_message("pong")



@client.event
async def on_ready():
    await tree.sync()
    print("test")

@client.event
async def on_message(message: discord.message):
    print(f"Message from {message.author}: {message.content}")
    if(message.author != client.user):
            await message.channel.send(message.content)
            await message.add_reaction("👍")

client.run(token)

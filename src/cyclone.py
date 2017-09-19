import discord
import asyncio
import json
import urllib.request

import config

client = discord.Client()

@client.event
async def on_ready():
  print("~~~ 🌀 ~~~")
  print("Logged in as")
  print(client.user.name)
  print(client.user.id)
  print("~~~ 🌀 ~~~")

@client.event
async def on_message(message):
  authorRole = message.author.top_role

  if message.content.startswith(".ping"):
    await client.send_message(message.channel, "Pong!")
    print ("Pong'd in #" + message.channel.name)

  elif (message.content.startswith(".setgame")) and (str(message.author.top_role) in config.ROLES):
    arg = message.content.split(" ", 1)[1]
    await client.change_presence(game=discord.Game(name=arg))
    print ("Set Game to " + arg)

  elif (message.content.startswith(".stormmode")) and (str(message.author.top_role) in config.ROLES):
    await client.delete_message(message)
    embed = discord.Embed(title = "ATTENTION!", description = "@everyone We are now in **STORM MODE**, during Storm Mode rules will be more strictly enforced. *PLEASE* keep discussion where it belongs and try to have as little non-meteorological or preparation banter as possible.", color = int("0xff0000", 16))
    embed.set_thumbnail(url = config.STORMMODEIMAGE)
    await client.send_message(message.channel, embed = embed)

  elif (message.content.startswith(".embed")) and (str(message.author.top_role) in config.ROLES):
    await client.delete_message(message)
    arg = message.content.split(" ", 1)[1]
    embedJson = urllib.request.urlopen(arg)
    embedData = json.loads(embedJson.read().decode(embedJson.info().get_param("charset") or "utf-8"))
  
    embed = discord.Embed(title = embedData["title"], description = embedData["description"], color = int(embedData["color"], 16))
    embed.set_thumbnail(url = embedData["thumbnail"])
    for field in embedData["fields"].values():
      embed.add_field(name = field["title"], value= field["content"], inline=False)
    await client.send_message(message.channel, embed = embed) 
    print ("Created Embed in #" + message.channel.name)


client.run(config.TOKEN)

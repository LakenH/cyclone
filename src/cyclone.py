import discord
import asyncio
import json
import urllib.request
import re

import config

client = discord.Client()

knotsTranslation = False

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
    if message.channel.name == "announcements":
      mention = "@everyone "
    else:
      mention = ""
    embed = discord.Embed(title = "ATTENTION!", description =  mention + "We are now in **STORM MODE**, during Storm Mode rules will be more strictly enforced. *PLEASE* keep discussion where it belongs; any non-meteorological discussion about the storm **MUST** be kept out of the met channels. Anything not storm related should be kept in #off-topic-discussion.", color = int("0xff0000", 16))
    embed.set_thumbnail(url = config.STORMMODEIMAGE)
    await client.send_message(message.channel, embed = embed)

  elif (message.content.startswith(".embed")) and (str(message.author.top_role) in config.ROLES):
    await client.delete_message(message)
    arg = message.content.split(" ", 1)[1]
    if arg == "rules":
      arg = config.EMBEDRULES
    elif arg == "roles":
      arg = config.EMBEDROLES
    embedJson = urllib.request.urlopen(arg)
    embedData = json.loads(embedJson.read().decode(embedJson.info().get_param("charset") or "utf-8"))
  
    embed = discord.Embed(title = embedData["title"], description = embedData["description"], color = int(embedData["color"], 16))
    embed.set_thumbnail(url = embedData["thumbnail"])
    for field in embedData["fields"].values():
      embed.add_field(name = field["title"], value= field["content"], inline=False)
    await client.send_message(message.channel, embed = embed) 
    print ("Created Embed in #" + message.channel.name)

  elif (message.content.startswith(".convertKnots")) and (str(message.author.top_role) in config.ROLES):
    global knotsTranslation
    if knotsTranslation == False:
      knotsTranslation = True
      await client.send_message(message.channel, "Knots -> MPH **ENABLED**")
    else:
      knotsTranslation = False
      await client.send_message(message.channel, "Knots -> MPH **DISABLED**")

  elif (re.search("([0-9]*) knots", message.content, re.IGNORECASE)) and (knotsTranslation == True) and (message.author.name != client.user.name):
    arg = re.search("([0-9]*) knots", message.content, re.IGNORECASE)
    knots = arg.group(1)
    mph = int(knots) * 1.15078
    await client.send_message(message.channel, str(knots) + " knots = " + str(mph) + " MPH")

  elif (re.search("([0-9]*) kts", message.content, re.IGNORECASE)) and (knotsTranslation == True) and (message.author.name != client.user.name):
    arg = re.search("([0-9]*) kts", message.content, re.IGNORECASE)
    knots = arg.group(1)
    mph = int(knots) * 1.15078
    await client.send_message(message.channel, str(knots) + " knots = " + str(mph) + " MPH")

  elif (re.search("([0-9]*)knots", message.content, re.IGNORECASE)) and (knotsTranslation == True) and (message.author.name != client.user.name):
    arg = re.search("([0-9]*)knots", message.content, re.IGNORECASE)
    knots = arg.group(1)
    mph = int(knots) * 1.15078
    await client.send_message(message.channel, str(knots) + " knots = " + str(mph) + " MPH")

  elif (re.search("([0-9]*)kts", message.content, re.IGNORECASE)) and (knotsTranslation == True) and (message.author.name != client.user.name):
    arg = re.search("([0-9]*)kts", message.content, re.IGNORECASE)
    knots = arg.group(1)
    mph = int(knots) * 1.15078
    await client.send_message(message.channel, str(knots) + " knots = " + str(mph) + " MPH")


client.run(config.TOKEN)

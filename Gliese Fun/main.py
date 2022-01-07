from abc import get_cache_token
from io import BytesIO
from itertools import filterfalse
import discord
from discord import emoji
from discord import reaction
from discord import embeds
from discord import colour
from discord import role
from discord import http
from discord.activity import Game
from discord.ext import commands, tasks
import asyncio
import random
import os
from discord.ext.commands.core import command
from discord.flags import Intents
from nextcord import channel
import youtube_dl
from discord_slash import ButtonStyle, SlashCommand, error
from discord_slash.utils.manage_components import *
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option, create_choice, create_permission
from discord_slash.model import PermissionData, SlashCommandPermissionType
import datetime
from discord_components import *
import aiohttp
import json
from giphy_client.rest import ApiException
import giphy_client
from random import randint
from discord.ext.commands import Bot 
import wikipedia
import googletrans
import secrets
import re
import aiofiles

prefix = '+'
bot = commands.Bot(command_prefix = commands.when_mentioned_or(prefix), description = "bot gliese", help_command=None, Intents=discord.Intents.all())

status = ["+help",
        "bot par Tawren & adan_",
        "https://discord.gg/nc8RAAF6fR"]
ownerid = [841341738358669353, 695666763597217842]


@bot.event
async def on_ready():
    print("BOT ON")
    changeStatus.start()

@bot.command()
async def start(ctx, secondes = 5):
    changeStatus.change_interval(seconds = secondes)

@tasks.loop(seconds = 5)
async def changeStatus():
    game = discord.Streaming(platform = "twitch", url = "https://www.twitch.tv/tawren007", name = "๖ζ͜͡Gliese Bots")
    await bot.change_presence(activity = game)
    



@bot.command()
async def help(ctx):
	embed = discord.Embed(title = "**Utilitaires/Fun**", description = "Voici les commandes Utilitaires/Fun", color=0xff0000)
	embed.set_thumbnail(url = "https://media.discordapp.net/attachments/894638172267507862/896284211554693140/AGvuVRb5cjLnQjUqLzEtKA.png")
	embed.add_field(name = "**Mon préfix sur ce serveur est** `+`", value = "ㅤ", inline=False)
	embed.add_field(name = "`help`", value = "**Permet de montrer ce message**", inline = False)
	embed.add_field(name = "`say [ce que vous voulez dire]`", value = "**Le bot répètera ce que vous avez mis après le say.**", inline = False)
	embed.add_field(name = "`botinvite`", value = "**Envoie un message pour m'inviter dans vos serveurs**", inline=False)
	embed.add_field(name = "`botinfo`", value = "**Affiche des information sur le bot**", inline = False)
	embed.add_field(name = "`ping`", value = "**Affiche le ping du bot**", inline = False)
	embed.add_field(name = "`counter`", value = "**Affiche le nombre de serveur sur lesquel je suis**", inline = False)
	embed.add_field(name = "`chinese [message]`", value = "**Affiche le texte en chinois.**", inline = False)
	embed.add_field(name = "`password [nombre]`", value = "**Générer un mot de passe le nombre renseigné de caractères**", inline = False)
	embed.add_field(name = "`gif`", value = "**Envoie un gif aléatoire**", inline = False)
	embed.add_field(name = "`addition [nombre 1] [nombre 2]`", value = "**Additionne 2 chiffres**", inline = False)
	embed.add_field(name = "`diviser [nombre 1] [nombre 2]`", value = "**Divise 2 chiffres**", inline = False)
	embed.add_field(name = "`multiplier [nombre 1] [nombre 2]`", value = "**Multiplie 2 chiffres**", inline = False)
	embed.add_field(name = "`dm [user ID] (message)`", value = "**DM l'utilisateur dont l'id est mentionné**", inline = False)

	embed.set_footer(text =f"Demandé par {ctx.author}・")
	await ctx.send(embed = embed)

@bot.command()
async def botinfo(ctx):
    embed = discord.Embed(title = "__Nom du bot__ : ๖ζ͜͡Gliese Fun", color=0xff0000)
    embed.add_field(name = "__ID du bot__ : ", value = bot.user.id, inline=False)
    embed.add_field(name = "Créateur du bot : ", value = "adan_ & Tawren", inline=False)
    embed.add_field(name = "Langage du bot :", value= "Discord.py `V3.8.10 64 Bit`", inline=False)
    embed.set_footer(text =f"botinfo demandé par {ctx.author}")

    await ctx.send(embed = embed)


@bot.command(aliases = ["psw"])
async def password(ctx, nbytes: int = 18):
        """ Generates a random password string for you
        This returns a random URL-safe text string, containing nbytes random bytes.
        The text is Base64 encoded, so on average each byte results in approximately 1.3 characters.
        """
        if nbytes not in range(3, 1401):
            return await ctx.send("**J'accepte uniquement les nombres entre __3__ et __1400__ !**")
        if hasattr(ctx, "guild") and ctx.guild is not None:
            await ctx.send(f"**Je t'ai envoyé un message privé avec ton mot de passe. {ctx.author.name}**")
        await ctx.author.send(f"🎁 **Ton futur mot de passe :**\n{secrets.token_urlsafe(nbytes)}")

@bot.command()
async def dm(ctx, user_id=None, *, args=None):
    if user_id != None and args != None:
        try:
            target = await bot.fetch_user(user_id)
            await target.send(args)

            await ctx.channel.send("**J'ai envoyé** '" + args + "' **à : **" + target.name)

        except:
            await ctx.channel.send("Je n'ai pas pu DM la personne.")
        

    else:
        await ctx.channel.send("Vous n'avez pas spécifier de user ID !.")

@bot.command(aliases=['8ball', '8b'])
async def eightball(ctx, *, question):
    responses = ["C'est ceratain.",
                "C'est à toi de décider.",
                "¯\_(ツ)_/¯",
                "Oui",
                "Non",
                "Je crois bien",
                "Vu",
                "absolument",
                "JAMAIS !!",
                "Si tu veut une réponse, ajoute le bot sur ton serveur x)",
                "Je ne sais pas vraiment..."]
    await ctx.send(f':8ball: **Question :** {question}\n:8ball: **Réponse :** {random.choice(responses)}')

@bot.command()
async def addition(ctx, a: int, b: int):
    embed = discord.Embed(title="Résultat :", description=a+b, color=0xff0000)
    embed.set_footer(text="Addition Embed")
    await ctx.send(embed=embed)

@bot.command()
async def multiplier(ctx, a: int, b: int):
    embed = discord.Embed(title="Résultat :", description=a*b, color = 0xff0000)
    embed.set_footer(text="Multiplication page")
    await ctx.send(embed=embed)

@bot.command()
async def diviser(ctx, a: int, b: int):
    divide25 = (a/b)
    embed = discord.Embed(title="Résultat :", description=str(divide25), color = 0xff0000)
    embed.set_footer(text="Division Page")
    await ctx.send(embed=embed)

@bot.command()
async def gif(ctx,*,q="random"):

    api_key="gYm76pYsdqenVTwYiFWB1HTpz5hFs7Xt"
    api_instance = giphy_client.DefaultApi()

    try: 
    # Search Endpoint
        
        api_response = api_instance.gifs_search_get(api_key, q, limit=5, rating='g')
        lst = list(api_response.data)
        giff = random.choice(lst)

        emb = discord.Embed(title=q)
        emb.set_image(url = f'https://media.giphy.com/media/{giff.id}/giphy.gif')

        await ctx.channel.send(embed=emb)
    except ApiException as e:
        print("Exception when calling DefaultApi->gifs_search_get: %s\n" % e)

@bot.command()
async def chinese(ctx, *text):
	chineseChar = "丹书匚刀巳下呂廾工丿片乚爪冂口尸Q尺丂丁凵V山乂Y乙"
	chineseText = []
	for word in text:
		for char in word:
			if char.isalpha():
				index = ord(char) - ord("a")
				transformed = chineseChar[index]
				chineseText.append(transformed)
			else:
				chineseText.append(char)
		chineseText.append(" ")
	await ctx.send("".join(chineseText))
  
@bot.command(aliases = ["pic", "pp", "pdp"])
async def avatar(ctx, user: discord.User = None):
    if user is None:
        user = ctx.author
   
 
    avatarEmbed = discord.Embed(title = f"{user.name}\'s Avatar", color = 0xFFA500)
 
    avatarEmbed.set_image(url = user.avatar.url)
 
    avatarEmbed.timestamp = ctx.message.created_at 
 
    await ctx.send(embed = avatarEmbed)

@bot.command()
async def botinvite(ctx):
    embed = discord.Embed(title = "Support me", description = "**Invite moi sur ton serveur ! **", color=0xff0000)
    embed.set_thumbnail(url = "https://media.discordapp.net/attachments/867657920769294356/893537752933597204/g.png")
    embed.add_field(name = "Lien d'invitaion : ", value = "**https://bit.ly/2ZBhhbr**", inline = True)
    embed.add_field(name = "Serveur de support : ", value = "**https://discord.gg/nc8RAAF6fR**", inline = True)
    embed.set_footer(text =f"demandé par {ctx.author}")

    await ctx.send(embed = embed)

  

@bot.command()
async def say(ctx, *texte):
    await ctx.message.delete()
    await ctx.send(" ".join(texte))

# Affiche le ping du botd
@bot.command(name="ping")
async def ping(ctx: commands.Context):
    embed = discord.Embed(title =f":ping_pong: Pong ! {round(bot.latency * 1000)}ms", description ="", color=0xff0000)
    await ctx.send(embed = embed)

@bot.command()
async def counter(ctx):
    embed = discord.Embed(title ="**Je suis sur __" + str(len(bot.guilds)) + "__ serveurs**", description ="", color=0xff0000)

    await ctx.send(embed = embed)

bot.run("--")
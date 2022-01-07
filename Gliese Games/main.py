from abc import get_cache_token
from io import BytesIO
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
import time
import math

prefix = '-'
bot = commands.Bot(command_prefix = commands.when_mentioned_or(prefix), description = "bot gliese", help_command=None, Intents=discord.Intents.all())

status = ["-tictactoe",
        "bot par Tawren & adan_",
        "https://discord.gg/nc8RAAF6fR"]
ownerid = [841341738358669353, 695666763597217842]

player1 = ""
player2 = ""
turn = ""
gameOver = True

board = []

winningConditions = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]

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

# les erreurs
@bot.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.CommandNotFound):
		await ctx.send("**Cette commande n'existe pas.**")
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send("**Il manque un argument.**")
	elif isinstance(error, commands.MissingPermissions):
		await ctx.send("**Vous n'avez pas les permissions pour faire cette commande.**")
	elif isinstance(error, commands.CheckFailure):
		await ctx.send("**Vous ne pouvez utiliser cette commande.**")
	if isinstance(error.original, discord.Forbidden):
		await ctx.send("**Oups, je n'ai pas les permissions nécéssaires pour faire cette commmande**")

@bot.command()
async def games(ctx):
	embed = discord.Embed(title = "**Jeux**", description = "Voici les commandes jeux", color=0xff0000)
	embed.set_thumbnail(url = "https://media.discordapp.net/attachments/894638172267507862/896284211554693140/AGvuVRb5cjLnQjUqLzEtKA.png")
	embed.add_field(name = "**Mon préfix sur ce serveur est** `-`", value = "ㅤ", inline=False)
	embed.add_field(name = "`tictactoe [joueur 1] [joueur 2]`", value = "**Joue au jeu du tictactoe**", inline = False)
	embed.add_field(name = "`place [nombre]`", value = "**Place :regional_indicator_x: ou :o2: sur le plateau du tictactoe**", inline = False)

	embed.set_footer(text =f"Demandé par {ctx.author}・")
	await ctx.send(embed = embed)

@bot.command()
async def tictactoe(ctx, p1: discord.Member, p2: discord.Member):
    global count
    global player1
    global player2
    global turn
    global gameOver

    if gameOver:
        global board
        board = [":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:"]
        turn = ""
        gameOver = False
        count = 0

        player1 = p1
        player2 = p2

        # print the board
        line = ""
        for x in range(len(board)):
            if x == 2 or x == 5 or x == 8:
                line += " " + board[x]
                await ctx.send(line)
                line = ""
            else:
                line += " " + board[x]

        # determine who goes first
        num = random.randint(1, 2)
        if num == 1:
            turn = player1
            await ctx.send("**C'est au tour de** <@" + str(player1.id) + ">")
        elif num == 2:
            turn = player2
            await ctx.send("**C'est au tour de** <@" + str(player2.id) + ">")
    else:
        await ctx.send("**Une parte est déjà en cours ! Terminez-la avant de commencer une nouvelle.**")

@bot.command()
async def place(ctx, pos: int):
    global turn
    global player1
    global player2
    global board
    global count
    global gameOver

    if not gameOver:
        mark = ""
        if turn == ctx.author:
            if turn == player1:
                mark = ":regional_indicator_x:"
            elif turn == player2:
                mark = ":o2:"
            if 0 < pos < 10 and board[pos - 1] == ":white_large_square:" :
                board[pos - 1] = mark
                count += 1

                # print the board
                line = ""
                for x in range(len(board)):
                    if x == 2 or x == 5 or x == 8:
                        line += " " + board[x]
                        await ctx.send(line)
                        line = ""
                    else:
                        line += " " + board[x]

                checkWinner(winningConditions, mark)
                print(count)
                if gameOver == True:
                    await ctx.send(mark + " **gagne !**")
                elif count >= 9:
                    gameOver = True
                    await ctx.send("**égalité !**")

                # switch turns
                if turn == player1:
                    turn = player2
                elif turn == player2:
                    turn = player1
            else:
                await ctx.send("**Assurez-vous de choisir un nombre entier compris entre 1 et 9 (inclus) ou de vérifier si il n'a pas déjà été pris.**")
        else:
            await ctx.send("**Ce n'est pas à toi !**")
    else:
        await ctx.send("**Merci de lancer une partie en utilisant la commande** `-tictactoe`.")


def checkWinner(winningConditions, mark):
    global gameOver
    for condition in winningConditions:
        if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
            gameOver = True

@bot.command(name="ping")
async def ping(ctx: commands.Context):
    embed = discord.Embed(title =f":ping_pong: Pong ! {round(bot.latency * 1000)}ms", description ="", color=0xff0000)
    await ctx.send(embed = embed)

@bot.command()
async def counter(ctx):
    embed = discord.Embed(title ="**Je suis sur __" + str(len(bot.guilds)) + "__ serveurs**", description ="", color=0xff0000)

    await ctx.send(embed = embed)

@bot.command()
async def botinvite(ctx):
    embed = discord.Embed(title = "Support me", description = "**Invite moi sur ton serveur ! **", color=0xff0000)
    embed.set_thumbnail(url = "https://media.discordapp.net/attachments/867657920769294356/893537752933597204/g.png")
    embed.add_field(name = "Lien d'invitaion : ", value = "**https://bit.ly/3mqJRoB**", inline = True)
    embed.add_field(name = "Serveur de support : ", value = "**https://discord.gg/nc8RAAF6fR**", inline = True)
    embed.set_footer(text =f"demandé par {ctx.author}")

    await ctx.send(embed = embed)

bot.run("OTE3MDcyMTMzNjMxMzk3OTIw.YazX-w.cIbapyFcMYaUL7JTuNdmXIGULTw")
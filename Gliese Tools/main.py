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
from nextcord.activity import Streaming
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
from youtube_dl.postprocessor import ffmpeg

prefix = ';'
bot = commands.Bot(command_prefix = commands.when_mentioned_or(prefix), description = "bot gliese", help_command=None, Intents=discord.Intents.all())

status = [";help",
        "bot par Tawren"]
ownerid = [841341738358669353, 804387422758371358]

youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

# quand le bot est prêt on affiche "print"
@bot.event
async def on_ready():
    print("BOT ON")
    changeStatus.start()

@bot.command()
async def start(ctx, secondes = 5):
    changeStatus.change_interval(seconds = secondes)

snipe_message_author = {}
snipe_message_content = {}
 
@bot.event
async def on_message_delete(message):
     snipe_message_author[message.channel.id] = message.author
     snipe_message_content[message.channel.id] = message.content
     await asyncio.sleep(60)
     del snipe_message_author[message.channel.id]
     del snipe_message_content[message.channel.id]

@tasks.loop(seconds = 5)
async def changeStatus():
    game = discord.Streaming(platform = "twitch", url = "https://www.twitch.tv/tawren007", name = "Dev By Tawren")
    await bot.change_presence(activity = game)



@bot.event
async def on_raw_reaction_add(payload):

    if payload.member.bot:
        pass

    else:
        with open('reactrole.json') as react_file:
            data = json.load(react_file)
            for x in data:
                if x['emoji'] == payload.emoji.name:
                    role = discord.utils.get(client.get_guild(
                        payload.guild_id).roles, id=x['role_id'])

                    await payload.member.add_roles(role)


@bot.event
async def on_raw_reaction_remove(payload):

    with open('reactrole.json') as react_file:
        data = json.load(react_file)
        for x in data:
            if x['emoji'] == payload.emoji.name:
                role = discord.utils.get(client.get_guild(
                    payload.guild_id).roles, id=x['role_id'])

                
                await client.get_guild(payload.guild_id).get_member(payload.user_id).remove_roles(role)



# les erreurs


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


# --------------------
# Les commandes
# --------------------

@bot.command()
async def help(ctx):
	embed = discord.Embed(title = "**Modéartion**", description = "Voici les commandes de modération", color=0xff0000)
	embed.set_thumbnail(url = "https://media.discordapp.net/attachments/894638172267507862/896282039198814248/2047-certifiedmoderator.png")
	embed.add_field(name = "**Mon préfix sur ce serveur est** `g!`", value = "ㅤ", inline=False)
	embed.add_field(name = "`ban [@mention] (raison)`", value = "**Permet de bannir la personne mentionné.**", inline = False)
	embed.add_field(name = "`unban [@mention] (raison)`", value = "**Permet de débannir la personne mentionné.**", inline = False)

	embed.add_field(name = "`mute [@mention] (raison)`", value = "**Permet de réduire au silence la personne mentioné.**", inline=False)
	embed.add_field(name = "`unmute [@mention] (raison)`", value = "**Permet de redonner la voix à la personne mentioné.**", inline=False)
	embed.add_field(name = "`tempmute [@mention] [chiffre] [s, m, h, d] (raison)`", value = "**Permet de réduire temporairement au silence la personne mentioné.**", inline=False)

	embed.add_field(name = "`kick [@mention] (raison)`", value = "**Permet de kick la personne mentionné.**", inline = False)

	embed.add_field(name = "`lock` || BIENTOT ||", value = "**Vérrouille un salon**", inline = False)
	embed.add_field(name = "`unlock` || BIENTOT ||", value = "**Dévérouille un salon**", inline = False)
	embed.add_field(name = "`snipe`", value = "**Récupérer un message qui a été supprimé.**", inline = False)
	embed.add_field(name = "`slowmod [secondes]`", value = "**Ajoute un slowmod à un salon**", inline = False)
	embed.add_field(name = "`removerole [role] [membre]`", value = "**Supprime le rôle mentionné au membre mentionné**", inline = False)

	embed.add_field(name = "`serverinfo`", value = "**Affiche les informations sur le serveur.**", inline = False)
	embed.add_field(name = "`ping`", value = "**Affiche le ping du bot**", inline = False)
	embed.add_field(name = "`userinfo (@mention)`", value = "**Permet de montrer les information de la personne mentionnée**", inline=False)
	embed.add_field(name = "`clear [nombre]`", value = "**Permet de supprimer le nombre de message indiqué.**", inline = False)
	embed.add_field(name = "`setnick [mention] [newnick]`", value = "**Change le pseudo d'un utilisateur**", inline = False)
    

	embed.set_footer(text =f"Demandé par {ctx.author}・DEv By Tawren")
	await ctx.send(embed = embed)

#----------------------
# Tempban/ban/unban
#----------------------

# Banni member mention
@bot.command()
@commands.has_permissions(ban_members = True)
async def ban(ctx, user : discord.Member, *, reason = "Aucune raison n'a été donné"):
    await ctx.guild.ban(user, reason = reason)
    embed = discord.Embed(title = "**Banissement**", description = "Un membre à été banni !", color=0xff0000)
    embed.set_thumbnail(url = "https://emoji.gg/assets/emoji/9005-abanhammer.gif")
    embed.add_field(name = "Membre banni", value = user.name, inline = True)
    embed.add_field(name = "Raison", value = reason, inline = True)
    embed.add_field(name = "Modérateur", value = ctx.author.name, inline = True)
    embed.set_footer(text = "Dev By Tawren")

    await ctx.send(embed = embed)

# Unban
@bot.command()
@commands.has_permissions(ban_members = True)
async def unban(ctx, user, *reason):
    reason = " ".join(reason)
    userName, userId = user.split("#")
    bannedUsers = await ctx.guild.bans()
    for i in bannedUsers:
        if i.user.name == userName and i.user.discriminator == userId:
            await ctx.guild.unban(i.user, reason = reason)

            embed = discord.Embed(title = "Débanissement", description = f"{user} a été unban de ce serveur.", color=0xff0000)
            embed.set_thumbnail(url = "https://media.discordapp.net/attachments/894638172267507862/904006388894818354/g.png")
            embed.set_footer(text = "Dev By Tawren")

            await ctx.send(embed = embed)

#--------
# Warn
#--------

# Warn A FAIRE MARCHER
@bot.command()
@commands.has_permissions(kick_members=True)
async def warn(ctx, server, member:discord.Member, *, raison = None):
    user = member.mention
    serveurnom = server.name
    embed = discord.Embed(title="Warn : ", value = "Un membre viens d\'être avertis !", color=0xff0000)
    embed.add_field(name="Warn : ", value=f'Raison : {raison}', inline=False)
    embed.add_field(name="User warn: ", value=f'{member.mention}', inline=False)
    embed.add_field(name="Warn par : ", value=f'{ctx.author}', inline=False)
    embed.set_footer(text="๖ζ͜͡Gliese")
    
    await user.send(f'Vous avez été warn sur le serveur {serveurnom} pour la raison suivante : **{raison}** !')
    await ctx.send(embed=embed)

#--------
# Kick
#--------

# Kick
@bot.command()
@commands.has_permissions(kick_members = True)
async def kick(ctx, user : discord.User, reason = "Aucune raison n'a été donné"):
    await ctx.guild.kick(user, reason = reason)
    embed = discord.Embed(title = "**Kick**", description = "Un membre à été kick !", color=0xff0000)
    embed.set_thumbnail(url = "https://emoji.gg/assets/emoji/7783-discordkickicon.png")
    embed.add_field(name = "Membre kick", value = user.name, inline = True)
    embed.add_field(name = "Raison", value = reason, inline = True)
    embed.add_field(name = "Modérateur", value = ctx.author.name, inline = True)
    embed.set_footer(text = "Dev By Tawren")

    await ctx.send(embed = embed)

#--------------------
# Botservers/botinfo
#--------------------

@bot.command()
async def counter(ctx):
    embed = discord.Embed(title ="**Je suis sur __" + str(len(bot.guilds)) + "__ serveurs**", description ="", color=0xff0000)

    await ctx.send(embed = embed)

@bot.command()
async def botinfo(ctx):
    embed = discord.Embed(title = "__Nom du bot__ : ๖ζ͜͡Gliese Tools", color=0xff0000)
    embed.set_thumbnail(url=bot.user.avatar_url)
    embed.add_field(name = "__ID du bot__ : ", value = bot.user.id, inline=False)
    embed.add_field(name = "Créateur du bot : ", value = "adan_ & Tawren", inline=False)
    embed.set_footer(text =f"Dev By Tawren")

    await ctx.send(embed = embed)

#---------------
# Lock/Unlock/Nick
#---------------
@bot.command()
@commands.has_permissions(manage_channels=True)
async def lock(ctx):
    overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages=False
    await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    await ctx.send("**Ce salon est véruoillé !**")

@bot.command()
@commands.has_permissions(manage_channels=True)
async def unlock(ctx):
    overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages=True
    await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    await ctx.send("**Ce salon est n'est plus vérouillé !**")

@bot.command()
@commands.has_permissions(manage_nicknames=True)
async def setnick(ctx, member:discord.Member,*,nick=None):
    old_nick = member.display_name

    await member.edit(nick=nick)

    new_nick = member.display_name

    await ctx.send(f'**Le pseudo de** *{old_nick}* **a été modifié !**')

#----------------------------
# Mute/tempmute/unmute
#----------------------------

# Tempmute, Membre mention + chiffre + time
@bot.command()
@commands.has_permissions(administrator = True)
async def tempmute(ctx, member: discord.Member, time: int, d, reason="Aucune"):
    guild = ctx.guild

    for role in guild.roles:
        if role.name == "Muted":
            await member.add_roles(role)

            embed = discord.Embed(title="Tempmute", description=f"{member.mention} à été tempmute ", colour=discord.Colour.red())
            embed.set_thumbnail(url = "https://emoji.gg/assets/emoji/1558_muted.gif")
            embed.add_field(name="raison :", value=reason, inline=False)
            embed.add_field(name="Vous pouvez parler dans :", value=f"{time}{d}", inline=False)
            embed.set_footer(text = "๖ζ͜͡Gliese")
            await ctx.send(embed=embed)

            if d == "s":
                await asyncio.sleep(time)

            if d == "m":
                await asyncio.sleep(time*60)

            if d == "h":
                await asyncio.sleep(time*60*60)

            if d == "d":
                await asyncio.sleep(time*60*60*24)

            await member.remove_roles(role)

            embed = discord.Embed(title="Unmute !", description=f"unmute -{member.mention} ", colour=discord.Colour.red())
            embed.set_thumbnail(url = "https://emoji.gg/assets/emoji/4991-unmute.png")
            embed.set_footer(text = "Dev By Tawren")
            await ctx.send(embed=embed)

            return

# Création du rôle : "Muted"
async def createMutedRole(ctx):
    mutedRole = await ctx.guild.create_role(name = "Muted",
                                            permissions = discord.Permissions(
                                                send_messages = False,
                                                speak = False),
                                            reason = "Creation du role Muted pour mute des personne.")
    for channel in ctx.guild.channels:
        await channel.set_permissions(mutedRole, send_messages = False, speak = False)
    return mutedRole

async def getMutedRole(ctx):
    roles = ctx.guild.roles
    for role in roles:
        if role.name == "Muted":
            return role
    
    return await createMutedRole(ctx)

# Mute, donne le rôle mute à membrer mention
@bot.command()
@commands.has_permissions(administrator = True)
async def mute(ctx, member : discord.Member, *, reason = "Aucune raison n'a été renseigné"):
    mutedRole = await getMutedRole(ctx)
    await member.add_roles(mutedRole, reason = reason)
    embed = discord.Embed(title = "**Mute**", description = "Un membre a été mute", color=0xFF0000)
    embed.add_field(name = "__Raison__", value = reason, inline = False)
    embed.add_field(name = "__Membre__", value = member.mention, inline = False)
    embed.set_footer(text = "Dev By Tawren")

    await ctx.send(embed = embed)

# Erreur si il manque un argument
@mute.error
async def mute_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("La commande mute prend en paramètre une mention.")
        await ctx.send("Veuillez réessayer.")

# Unmute, enleve le rôle muted et envoit l'embed
@bot.command()
@commands.has_permissions(administrator = True)
async def unmute(ctx, member : discord.Member, *, reason = "Aucune raison n'a été renseigné"):
    mutedRole = await getMutedRole(ctx)
    await member.remove_roles(mutedRole, reason = reason)
    embed = discord.Embed(title = "**Unmute**", description = "Un membre a été unmute", color=0xFF0000)
    embed.add_field(name = "__Raison__", value = reason, inline = False)
    embed.add_field(name = "__Membre__", value = member.mention, inline = False)
    embed.set_footer(text = "Dev By Tawren")

    await ctx.send(embed = embed)

# Erreur, si il manque un argument
@unmute.error
async def unmute_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("La commande unmute prend en paramètre une mention.")
        await ctx.send("Veuillez réessayer.")

#--------
# Ping
#--------

# Affiche le ping du botd
@bot.command(name="ping")
async def ping(ctx: commands.Context):
    embed = discord.Embed(title =f":ping_pong: Pong ! {round(bot.latency * 1000)}ms", description ="", color=0xff0000)
    await ctx.send(embed = embed)

#--------
# Clear
#--------

# Clear, Supprime le nombre de message voulu puis supprime le message de confirmation au bout de 5s
@bot.command()
@commands.has_permissions(manage_messages = True)
async def clear(ctx, nombre : int):
    messages = await ctx.channel.history(limit = nombre + 1).flatten()
    for message in messages:
        await message.delete()
    await ctx.send(f"**{nombre} messages ont été supprimés.**")   
    await asyncio.sleep(5)
    aaa = await ctx.channel.history(limit = 1).flatten()
    for message in aaa:
        await message.delete()

@bot.command()
async def botinvite(ctx):
    embed = discord.Embed(title = "Support me", description = "**Invite moi sur ton serveur ! **", color=0xff0000)
    embed.set_thumbnail(url = "https://media.discordapp.net/attachments/867657920769294356/893537752933597204/g.png")
    embed.add_field(name = "Lien d'invitaion : ", value = "**https://bit.ly/3nFe96x**", inline = True)
    embed.add_field(name = "Serveur de support : ", value = "**https://discord.gg/nc8RAAF6fR**", inline = True)
    embed.set_footer(text =f"demandé par {ctx.author}")

    await ctx.send(embed = embed)

@bot.command()
async def userinfo(ctx, *, user: discord.User = None):
    if user is None:
        user = ctx.author
    voice_state = None if not user.voice else user.voice.channel
    date_format = "%a %d %b %Y %H:%M "
    if isinstance(user, discord.Member):
                role = user.top_role.name
                if role == "@everyone":
                    role = "N/A"
    embed = discord.Embed(color=0xfccf03, description=user.mention)
    embed.set_author(name=str(user), icon_url=user.avatar_url)
    embed.set_thumbnail(url=user.avatar_url)
    embed.add_field(name="A rejoint", value=user.joined_at.strftime(date_format), inline=False)
    embed.add_field(name="Création du compte", value=user.created_at.strftime(date_format), inline=False)
    embed.add_field(name='Surnom', value=user.nick, inline=True)
    embed.add_field(name='Status', value=user.status, inline=True)   
    embed.add_field(name='Jeux', value=user.activity, inline=True)
    embed.add_field(name='En vocal', value=voice_state, inline=True)
    embed.add_field(name='Plus au rôle', value=role, inline=True)
    embed.set_footer(text='ID: ' + str(user.id))
    await ctx.send(embed=embed)

@bot.command()
async def serverinfo(ctx):
    server = ctx.guild
    number_textchannel = len(server.text_channels)
    number_voicechannel = len(server.voice_channels)
    serveurdescription = server.description
    number_members = server.member_count
    serveurname = server.name

    embed = discord.Embed(title = f"Informations sur le serveur {serveurname}", color=0xff0000)
    embed.add_field(name="Nombre de salons textuels :", value=f"{number_textchannel} salons textuels.")
    embed.add_field(name="Nombre de salons vocaux :", value=f"{number_voicechannel} salons vocaux.")
    embed.add_field(name="Description du serveur :", value=f"{serveurdescription}")
    embed.add_field(name="Le serveur contient :", value=f"{number_members} membres")
    embed.set_footer(text="๖ζ͜͡Gliese | Server info page")
    await ctx.send(embed = embed)

bot.command()
async def sondage(ctx,*,message):
    embed = discord.Embed(title="Répond à la question posée !", description=f"__{message}__")
    embed.add_field(name="**Réagis avec** `✅` **pour OUI**", value="*Tu est d'accord avec la question*")
    embed.add_field(name="**Réagis avec** `❌` **pour NON**", value="*Tu n'es pas d'accord avec la question*")
    embed.set_footer(text="Nouveau sondage !")
    msg=await ctx.channel.send(embed=embed)
    await msg.add_reaction('✅')
    await msg.add_reaction('❌')

@bot.command()
@commands.has_permissions(administrator=True, manage_roles=True)
async def reactrole(ctx, emoji, role: discord.Role, *, message):

    emb = discord.Embed(description=message)
    msg = await ctx.channel.send(embed=emb)
    await msg.add_reaction(emoji)

    with open('reactrole.json') as json_file:
        data = json.load(json_file)

        new_react_role = {'role_name': role.name, 
        'role_id': role.id,
        'emoji': emoji,
        'message_id': msg.id}

        data.append(new_react_role)

    with open('reactrole.json', 'w') as f:
        json.dump(data, f, indent=4)

@bot.command()
async def snipe(ctx):
    channel = ctx.channel 
    try:
        snipeEmbed = discord.Embed(title=f"Dernier message supprimé dans #{channel.name}", description = snipe_message_content[channel.id])
        snipeEmbed.set_footer(text=f"Supprimé par {snipe_message_author[channel.id]}")
        await ctx.send(embed = snipeEmbed)
    except:
        await ctx.send(f"Il n'y a pas de messages supprimés dans #{channel.name}")

@bot.command(case_insensitive=True)
async def slowmod(ctx, time:int):
    if (not ctx.author.guild_permissions.manage_messages):
        await ctx.send('**Vous ne pouvez pas utiliser cette commande ! Requires :** ``Manage Messages``')
        return
    if time == 0:
        await ctx.send('**Slowmod actuellement à** `0`')
        await ctx.channel.edit(slowmode_delay = 0)
    elif time > 21600:
        await ctx.send('**Tu ne peut pas mettre un slowmod de plus de 6h !**')
        return
    else:
        await ctx.channel.edit(slowmode_delay = time)
        await ctx.send(f"**Slowmod réglé sur** `{time}` **secondes !**")

@bot.command()
async def removerole(ctx, role: discord.Role=None, member:discord.Member=None):
    if role == None:
        return await ctx.send("**Merci de mentionner un rôle !**")
    elif member == None:
        return await ctx.send("**Merci de mentionner un membre !**")       
    await member.remove_roles(role)
    embed = discord.Embed(title="Rôle Supprimé !", description=f"J'ai retirer **{role}** à {member.mention} !", timestamp= ctx.message.created_at, color= discord.Color.red())
    await ctx.send(embed = embed)

bot.run("OTE5MTUyNTM1Nzk1ODAyMTMz.YbRpgQ.2yFB21dIb7Wm2-ZW1hN8n-Su5O8")
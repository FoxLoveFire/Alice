import discord
import random
import helper as func
from discord.ext import commands
from discord import utils
import requests
import json

import configparser

config = configparser.ConfigParser()

config.read('discord.conf')
prefix = config['BOT']['command_prefix'] + " "
token = config['BOT']['token']

intents = discord.Intents.all()
intents.reactions = True

ROLES = {
	'😘' : 1201891190174384188, 
	'🐍' : 1201901774349549608,
	'🥰': 1201902864876982303
	}

post_id = config['POST']["id"]

MAX = 4 

explores = {}

bot = commands.Bot(command_prefix=prefix, intents=intents)

serverlist = requests.get('https://servers.minetest.net/list')
data = json.loads(serverlist.content)

@bot.event
async def on_ready():
	print(f'Logged in Discord as {bot.user.name}')


@bot.command(help = "Random")
async def Alice_Random(ctx, min: int, max: int):
	try:
		await ctx.send(random.randint(min, max))
	except ValueError:
		await ctx.send("Arguments are integer max and integer min!")


@bot.command(help = "Whoami")
async def whoami(ctx):
	if ctx.message.author.guild_permissions.administrator:
		await ctx.send(f'You`re an admin {ctx.author.mention} ')
	else:
		await ctx.send(f'You`re an average joe {ctx.author.mention} ')

@bot.command(help = "Server list")
async def server_list(ctx,*, string = None):
	embed = discord.Embed(
		title = func.get_name(string, data),
		color = discord.Color.green())

	embed.add_field(name = "Players: ", value = func.server(string, data), inline = True)
	embed.add_field(name = "Online: ", value = func.get_online(string, data), inline = True)
	embed.add_field(name = "Minetest version: ", value = func.version(string, data), inline = True)
	embed.add_field(name = "Protocol: ", value = func.protocol(string, data), inline = True)
	embed.add_field(name = "Address and Port: ", value = func.addressandport(string, data), inline = True)
	embed.add_field(name = "Game: ", value = func.game(string, data), inline = True)
	embed.set_author(name = "Alice", url = "https://servers.minetest.net/list")

	await ctx.send(embed = embed)

@bot.command(help = "Write something")
async def say(ctx, string: str, color: str, *, string1: str):
	embed = discord.Embed(
	title = string,
	description = string1,
	color = func.colors[color])
	user = ctx.author
	embed.set_author(name = ctx.message.author.display_name, icon_url = str(user.avatar))

	await ctx.send(embed = embed)

@bot.command(help = "Generate password")
async def generatepassword(ctx, num1: int):
	await ctx.author.send(f'Generated password: {func.password(num1)}')


@bot.command(help = "Information")
async def info(ctx):
	embed = discord.Embed(
		title = "Information",
		color = discord.Color.green())
	embed.add_field(name = "Prefix", value = "Prefix is  `Alice ` ", inline = False)
	embed.add_field(name = "Server List", value = "Command: `server_list`. Argument: server name", inline = False)
	embed.add_field(name = "Generate password", value = "Command: `generatepassword`. Argument: lenght of password", inline = False)
	embed.add_field(name = "Reverse word", value = "Command: `reverse`. Argument: word or string", inline = False)
	await ctx.send(embed = embed)

@bot.command(help = "Reverse word")
async def reverse(ctx, *, string = None):
	await ctx.send(func.reverse(string))


@bot.command(help = "status")
async def status(ctx):
	embed = discord.Embed(
		title = "Hosting info",
		color = discord.Color.green())
	embed.add_field(name = "Status of RAM: ", value = func.stats(), inline = False)
	embed.add_field(name = "Base: ", value = func.architecture(), inline = False)
	embed.add_field(name = "Version: ", value = func.versionofdevice(), inline = False)
	await ctx.send(embed = embed)

@bot.command()
async def mods(ctx, string):
	await ctx.send(f'On {func.get_name(string, data)}, mods: {func.mods(string, data)}')

@bot.event
async def on_raw_reaction_add(payload):
    channel = bot.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    member = utils.get(message.guild.members, id=payload.user_id)

    try:
        emoji = str(payload.emoji)
        role = utils.get(message.guild.roles, id=ROLES[emoji])

        if len([i for i in member.roles if i.id not in explores]) <= MAX:
            await member.add_roles(role)
            print('[Granted] User {0.display_name} got role {1.name}'.format(member, role))
        else:
            await member.remove_reaction(payload.emoji, member)
            print('[WARN] User have too many roles: {0.display_name}'.format(member, role))

    except KeyError as e:
        print('[Error] KeyError, no role found for ' + emoji)
    except Exception as e:
        print(repr(e))

@bot.event
async def on_raw_reaction_remove(payload):
    channel = bot.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    member = utils.get(message.guild.members, id=payload.user_id)

    try:
        emoji = str(payload.emoji)
        role = utils.get(message.guild.roles, id=ROLES[emoji])

        await member.remove_roles(role)
        print('[REMOVED] User {0.display_name} lost role {1.name}'.format(member, role))

    except KeyError as e:
        print('[Error] KeyError, no role found for ' + emoji)
    except Exception as e:
        print(repr(e))


bot.run(token)


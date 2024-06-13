import discord
import random
import requests
import json
import helper as func
from discord.ext import commands
from discord import utils

import configparser

config = configparser.ConfigParser()

config.read('discord.conf')
prefix = config['BOT']['command_prefix'] + " "
token = config['BOT']['token']

intents = discord.Intents.all()
intents.reactions = True

ROLES = {
	'😘' : 1107683127188529183,
	'🐍' : 1201901774349549608,
	'🥰': 1201902864876982303
	}

post_id = config['POST']["id"]

bot = commands.Bot(command_prefix=prefix, intents=intents)

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


@bot.command(help = "Say")
@commands.has_permissions(administrator = True)
async def say(ctx, string: str, color: str, hide: bool, *, string1: str):
	embed = discord.Embed(
	title = string,
	description = string1,
	color = func.colors[color])

	if hide:
		user = ctx.author
		embed.set_author(name=ctx.message.author.display_name, icon_url=str(user.avatar))

	await ctx.send(embed = embed)
@say.error
async def say_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("У вас недостаточно прав для выполнения этой команды.")
@bot.command(help= "Say an")
@commands.has_permissions(administrator = True)
async def sayAn(ctx, title: str, color: str, channel_id: str, *, description: str):
  embed = discord.Embed(
    title=title,
    description=description,
    color=func.colors[color]
  )

  channel_id = int(channel_id.replace("<#", "").replace(">", ""))

  channel = ctx.guild.get_channel(channel_id)

  if channel is None:
    await ctx.send(f"Канал с ID {channel_id} не найден.")
    return

  await channel.send(embed=embed)

  await ctx.send(f"Сообщение отправлено в канал с ID {channel_id}")
@sayAn.error
async def sayAn_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("У вас недостаточно прав для выполнения этой команды.")
@bot.command(help="Server say")
@commands.has_permissions(administrator=True)  # Проверка наличия прав администратора
async def serverSay(ctx, channel_id: str, *, description: str):
    embed = discord.Embed(
        title="Server",
        description=description,
        color=discord.Colour.red()
    )

    channel_id = int(channel_id.replace("<#", "").replace(">", ""))
    channel = ctx.guild.get_channel(channel_id)

    if channel is None:
        await ctx.send(f"Канал с ID {channel_id} не найден.")
        return

    await channel.send(embed=embed)
    await ctx.send(f"Сообщение отправлено в канал с ID {channel_id}")

@serverSay.error
async def serverSay_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("У вас недостаточно прав для выполнения этой команды.")


@bot.command(help = "Generate password")
async def generatepassword(ctx, num1: int):
	await ctx.author.send(f'Generated password: {func.password(num1)}')


@bot.command(help = "Ban member")
@commands.has_permissions(kick_members=True, ban_members=True,
						  manage_roles=True)
async def ban(ctx, member: discord.Member, *, reason=None):
	if member.guild_permissions.administrator:
		await ctx.channel.send(
			f'Hi {ctx.author.name}! The member you aer trying to mute is a server Administrator. Please don\'t try this on them else they can get angry! :person_shrugging:')

	else:
		if reason is None:
			await member.send(
				f'Привет {member.name}! Ты был забанен {ctx.channel.guild.name} по неизвесной причине')
			await ctx.channel.send(
				f'Привет {ctx.author.name}! {member.name} был успешно забанен по неизвесной причине')
			await member.ban()
		else:
			await member.send(
				f'Hi {member.name}! Ты был забанен {ctx.channel.guild.name} по причине: \n \n {reason}')
			await ctx.channel.send(
				f'Hi {ctx.author.name}! {member.name} был забанен по причине: \n \n {reason}')
			await member.ban()

@bot.command(help="Unban a member")
async def unban(ctx, id: int):
    user = await bot.fetch_user(id)
    if user is None:
        await ctx.send(f"Пользователь с ID {id} не найден.")
        return

    try:
        await ctx.guild.unban(user)
        await ctx.send(f'{user.name} был разбанен.')
    except discord.HTTPException:
        await ctx.send(f"У меня нет прав на разбан этого пользователя.")


@bot.command(name="kick", help="Kick a member from the server")
async def kick(ctx, member: discord.Member, *, reason=None):
    if not ctx.author.guild_permissions.kick_members:
        await ctx.send("У вас нет прав на кик!")
        return

    if reason is None:
        reason = "Не указана причина"

    await member.kick(reason=reason)
    await ctx.send(f'{member.name} был кикнут с причиной: {reason}.')
@bot.command(help = "info")
async def info(ctx):
  embed = discord.Embed(
    title = "Information",
    color = discord.Color.green())
  embed.add_field(name = "Prefix", value = "Prefix is  Alice  ", inline = False)
  embed.add_field(name = "Server List", value = "Command: server_list. Argument: server name", inline = False)
  embed.add_field(name = "Generate password", value = "Command: generatepassword. Argument: lenght of password", inline = False)
  embed.add_field(name = "Reverse word", value = "Command: reverse. Argument: word or string", inline = False)
  embed.add_field(name = "Server Say", value = "Server Say: Сервер говорит. (serverSay 'argument') ", inline = False)
  embed.add_field(name = "Say An", value= "Say An: Сказать ананимно (sayAn 'text', 'color','channel', 'text1' )", inline = False)
  embed.add_field(name = "Say", value = "Say: сказать (say 'text', 'color', 'bool', 'text')", inline = False)
  embed.add_field(name = "ban/unban", value = "ban 'member', 'reason', unban 'member ID'")  # Исправлено:  включен  'member ID'
  await ctx.send(embed = embed)


@bot.command(help = "Reverse word")
async def reverse(ctx, *, string = None):
	await ctx.send(func.reverse(string))

@bot.event
async def on_raw_reaction_add(payload):
    channel = bot.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    member = utils.get(message.guild.members, id=payload.user_id)

    try:
        emoji = str(payload.emoji)
        role = utils.get(message.guild.roles, id=ROLES[emoji])

        await member.add_roles(role)
        print('[Granted] User {0.display_name} got role {1.name}'.format(member, role))


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

serverlist = requests.get('https://servers.minetest.net/list')
data = json.loads(serverlist.content)

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

@bot.command()
async def mods(ctx, string):
	await ctx.send(f'On {func.get_name(string, data)}, mods: {func.mods(string, data)}')

bot.run(token)


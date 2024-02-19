import random
import requests
import json
import discord
import os
import subprocess

colors = {
	"red": discord.Color.red(),
	"blue": discord.Color.blue(),
	"green": discord.Color.green(),
	"orange": discord.Color.orange(),
	"pink": discord.Color.pink(),
	"default": discord.Color.default()
}

def server(string, data):
	try:
		lst = data["list"]
		for s in lst:
			if string.lower() in s["name"].lower():
				res = ", ".join(s["clients_list"])
				lenght = len(res.split())
				if lenght == 1:
					return f'1 player: ' + res
				else:
					return f'Players: ' + res
		else:
			return "Cannot be found"
	except KeyError:
		return "KeyError"

def protocol(string, data):
	lst = data["list"]
	for s in lst:
		return f'Min: {s["proto_min"]} | Max: {s["proto_max"]}'

def get_name(string, data):
	lst = data["list"]
	for s in lst:
		if string.lower() in s["name"].lower():
			return str(s["name"])

def get_online(string, data):
	lst = data["list"]
	for s in lst:
		res = ", ".join(s["clients_list"])
		online = len(res.split())
		if string.lower() in s["name"].lower():
			return f'Online: {online} / {str(s["clients_max"])}'

def addressandport(string, data):
	lst = data["list"]
	for s in lst:
		if string.lower() in s["name"].lower():
			return f'Addres: `{s["address"]}` | Port: `{s["port"]}`' 

def version(string, data):
	lst = data["list"]
	for s in lst:
		if string.lower() in s["name"].lower():
			return str(s["version"])

def game(string, data):
	lst = data["list"]
	for s in lst:
		if string.lower() in s["name"].lower():
			return str(s["gameid"])

def mods(string, data):
	lst = data["list"]
	for s in lst:
		if string.lower() in s["name"].lower():
			res = ", ".join(s["mods"])
			return f'`{res}`'
		
def password(n):
	chars = '+-/*!&$#?=@<>abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
	password = ''
	for i in range(1):
		for s in range(n):
			password += random.choice(chars)
	return password

def reverse(n):
	return n[::-1]

def stats():
	total_memory, used_memory, free_memory = map(int, os.popen('free -t -m').readlines()[-1].split()[1:])
	return f'Free RAM: {free_memory} Mib, Used Memory: {used_memory} Mib, Total Memory: {total_memory} Mib'

def architecture():
	arch = subprocess.check_output(["uname", "-s", "-o","-m"]).decode('utf-8').strip()
	return arch

def versionofdevice():
	model = subprocess.check_output(["cat", "/sys/firmware/devicetree/base/model"]).decode('utf-8').strip()
	return model
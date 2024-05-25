from pathlib import Path
import requests
import discord
import os
import random
import json
import requests
from datetime import datetime
from colorama import Fore
from discord.ext import commands


        
activity = discord.Activity(type=discord.ActivityType.playing, name=f"discord.gg/nexustools")
intents=discord.Intents.default()
intents.members = True
intents.presences = True
bot = discord.Bot(command_prefix="*", activity=activity, status=discord.Status.online, intents=intents)

##########################################################
config = json.load(open("config.json", encoding="utf-8"))
#########################################################

guild_id = config['server_id']
owner_id = config['owner_id']
bot_token = config['bot_token']
status = config['bot_status']
##################################

free_gen_config = config['free_gen']

free_gen_role = free_gen_config['free_gen_role']
free_gen_channel_id = free_gen_config['free_gen_channel']
free_gen_cooldown = free_gen_config['free_gen_cooldown']
free_gen_status = free_gen_config['free_gen_status']
status_logs = free_gen_config['status_log_channel']
free_gen_folder = free_gen_config['free_gen_folder']
#######################################################

boost_gen_config = config['boost_gen']

boost_gen_role = boost_gen_config['boost_gen_role']
boost_gen_channel_id = boost_gen_config['boost_gen_channel']
boost_gen_cooldown = boost_gen_config['boost_gen_cooldown']
boost_gen_folder = boost_gen_config['boost_gen_folder']
##########################################################

premium_gen_config = config['premium_gen']

premium_gen_role = premium_gen_config['premium_gen_role']
premium_gen_channel_id = premium_gen_config['premium_gen_channel']
premium_gen_cooldown = premium_gen_config['premium_gen_cooldown']
premium_gen_folder = premium_gen_config['premium_gen_folder']
###############################################################

log_config = config['logs']

freegenhook = log_config['free_gen_log_webhook']
boostgenhook = log_config['booster_gen_log_webhook']
premiumgenhook = log_config['premium_gen_log_webhook']
admincommandshook = log_config['admin_commands_log_webhook']
###############################################################

class Utils():
    @staticmethod
    async def isWhitelisted(ctx) -> bool:
        if (
            str(ctx.author.id) in open("assets/whitelist.txt", "r").read().splitlines()
            or str(ctx.author.id) == str(owner_id)
        ):  
            return True
        else:
            return False

folder_list = [free_gen_folder, boost_gen_folder, premium_gen_folder]

def gen_get_stock(folder):
    path = Path(folder)
    stock = [file.name for file in path.glob('*.txt')]
    return stock

def count_stock(gen, file):
    with open(f"{gen}/{file}", 'r') as file:
        lines = file.readlines()
    return len(lines)

async def get_free_service_options(ctx: discord.AutocompleteContext):
    stock = gen_get_stock(free_gen_folder)
    stock_list = []
    for service in stock:
        service = service[:-4]
        stock_list.append(service)  
    return stock_list

async def get_booster_service_options(ctx: discord.AutocompleteContext):
    stock = gen_get_stock(boost_gen_folder)
    stock_list = []
    for service in stock:
        service = service[:-4]
        stock_list.append(service)  
    return stock_list

async def get_premium_service_options(ctx: discord.AutocompleteContext):
    stock = gen_get_stock(premium_gen_folder)
    stock_list = []
    for service in stock:
        service = service[:-4]
        stock_list.append(service)  
    return stock_list

def get_random_non_empty_line(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    if not lines:
        raise ValueError("The file is empty")

    non_empty_lines = [line for line in lines if line.strip() != ""]
    if not non_empty_lines:
        raise ValueError("The file contains no non-empty lines")

    chosen_line = random.choice(non_empty_lines).strip()
    remaining_lines = [line for line in lines if line.strip() != chosen_line]

    with open(file_path, 'w') as file:
        file.writelines(remaining_lines)

    return chosen_line

def remove_empty(file):
    with open(file, 'r') as f:
        lines = f.readlines()

    non_empty_lines = [line for line in lines if line.strip()]

    with open(file, 'w') as f:
        f.writelines(non_empty_lines)

def log_action_webhook(webhook, message, logtype):
    now = datetime.now()
    embed = {
        "title": f"{logtype} Log",
        "description": f"{message}",
        "color": 16056575,
        "footer": {
            "text": "Made by github.com/vatosv2 & discord.gg/nexustools"
        }
    }
    payload = {
        "embeds": [embed]
    }
    requests.post(webhook, json=payload)

def log_action_file(message):
    now = datetime.now()
    print(f"{Fore.RESET}[{Fore.GREEN}{now}{Fore.RESET}] {message} \n")
    with open("assets/logs.txt", "a", encoding="utf-8") as nexus:
        nexus.write(f"[{now}] {message} \n")
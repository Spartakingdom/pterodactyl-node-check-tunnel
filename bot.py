import discord
from discord.ext import commands, tasks
import requests
import json
import os
import time
import logging

logging.basicConfig(level=logging.DEBUG, filename="logs/debug.log", filemode="w", format="%(asctime)s - %(levelname)s - %(message)s")
console = logging.StreamHandler()
console.setLevel(logging.ERROR)
formatter = logging.Formatter("%(asctime)s - %(message)s")
console.setFormatter(formatter)
logging.getLogger().addHandler(console)

with open("config.json", "r") as f:
    config = json.load(f)

def load_nodes():
    return json.load(open("nodes.json", "r")) if os.path.exists("nodes.json") else {"nodes": []}

def save_nodes(nodes_data):
    with open("nodes.json", "w") as f:
        json.dump(nodes_data, f, indent=4)

intents = discord.Intents.default()
intents.messages = intents.guilds = intents.message_content = intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

@tasks.loop(minutes=1)
async def check_nodes():
    channel = bot.get_channel(config["alert_channel_id"])
    nodes_data = load_nodes()
    for node_url in nodes_data["nodes"]:
        try:
            start_time = time.time()
            response = requests.get(node_url, verify=False, timeout=10)
            response_time = round((time.time() - start_time) * 1000)
            status, color = (
                ("✅ Node Status: Operational", 0x00FF00) if response.status_code == 200 else
                ("✅ Node Status: Expected", 0x00FF00) if response.status_code == 401 else
                ("⚠️ Node Status: Warning", 0xFFA500)
            )
            embed = discord.Embed(
                title=status,
                description=f"Node `{node_url}` responded with status `{response.status_code}`.\nResponse Time: {response_time}ms",
                color=color
            )
            embed.set_footer(text="All systems functional!" if response.status_code == 200 else "Check configurations.")
            await channel.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(
                title="❌ Node Status: Critical",
                description=f"Node `{node_url}` is unreachable.\nError: {e}",
                color=0xFF0000
            )
            embed.set_footer(text="Immediate attention required!")
            await channel.send(embed=embed)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        return
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"⚠️ Missing argument: {error.param.name}.")
    elif isinstance(error, commands.CommandNotFound):
        return
    else:
        await ctx.send("❌ An unexpected error occurred.")
        raise error

@bot.event
async def on_ready():
    print(f"Bot connected as {bot.user}")
    check_nodes.start()
    for filename in os.listdir("./commands"):
        if filename.endswith(".py"):
            try:
                await bot.load_extension(f"commands.{filename[:-3]}")
            except Exception as e:
                print(f"Failed to load {filename}: {e}")

def command_restriction(ctx):
    if ctx.command and ctx.command.name == "rmv":
        role = discord.utils.get(ctx.author.roles, id=config["tag_role_id"])
        return role is not None
    if ctx.channel.id != config["command_channel_id"]:
        return False
    role = discord.utils.get(ctx.author.roles, id=config["tag_role_id"])
    return role is not None

bot.add_check(command_restriction)

bot.run(config["bot_token"])

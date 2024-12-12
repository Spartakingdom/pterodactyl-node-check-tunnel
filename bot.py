import discord
from discord.ext import commands, tasks
import requests
import json
import logging

logging.basicConfig(level=logging.DEBUG, filename="logs/debug.log", filemode="w", format="%(asctime)s - %(levelname)s - %(message)s")
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(message)s")
console.setFormatter(formatter)
logging.getLogger().addHandler(console)

with open('config.json', 'r') as f:
    config = json.load(f)

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    logging.info(f'Logged in as {bot.user}')
    print(f'Logged in as {bot.user}')
    check_nodes.start()

@tasks.loop(minutes=5)
async def check_nodes():
    channel = bot.get_channel(config['alert_channel_id'])
    for node_url in config['node_urls']:
        try:
            response = requests.get(node_url, verify=False)
            if response.status_code == 401:
                embed = discord.Embed(title="Node Status", description=f"✅ Node `{node_url}` is working correctly.", color=0x00FF00)
            else:
                embed = discord.Embed(title="Node Status", description=f"⚠️ Node `{node_url}` returned status code {response.status_code}.", color=0xFFA500)
            await channel.send(embed=embed)
        except Exception as e:
            logging.error(f"Error checking node {node_url}: {e}")
            embed = discord.Embed(title="Node Status", description=f"❌ Node `{node_url}` is down or unreachable. Error: {e}", color=0xFF0000)
            await channel.send(embed=embed)

@bot.event
async def on_message(message):
    if message.content.startswith("!check"):
        role_id = config['tag_role_id']
        if any(role.id == role_id for role in message.author.roles):
            await check_nodes()
        else:
            await message.channel.send("❌ You are not authorized to run this command!")
    await bot.process_commands(message)

bot.run(config['bot_token'])

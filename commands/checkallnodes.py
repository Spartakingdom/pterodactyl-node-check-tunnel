from discord.ext import commands
import json
import os
import requests
import discord

def load_nodes():
    if os.path.exists('nodes.json'):
        with open('nodes.json', 'r') as f:
            return json.load(f)
    return {"nodes": []}

async def setup(bot):
    @bot.command(name="checkall")
    async def check_all_nodes(ctx):
        """Command to check the status of all nodes."""
        nodes_data = load_nodes()
        if not nodes_data["nodes"]:
            await ctx.send("No nodes found in the configuration.")
            return

        for node_url in nodes_data["nodes"]:
            try:
                response = requests.get(node_url, timeout=10)
                response_time = response.elapsed.total_seconds() * 1000

                if response.status_code == 200:
                    embed = discord.Embed(
                        title="✅ Node Status: Operational",
                        description=f"Node `{node_url}` is operational.\nResponse Time: {response_time:.2f}ms",
                        color=0x00FF00
                    )
                    embed.set_footer(text="All systems functional!")
                    await ctx.send(embed=embed)
                elif response.status_code == 401:
                    embed = discord.Embed(
                        title="✅ Node Status: Expected",
                        description=f"Node `{node_url}` is operational with expected status code 401.\nResponse Time: {response_time:.2f}ms",
                        color=0x00FF00
                    )
                    embed.set_footer(text="Authentication required but operational.")
                    await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(
                        title="⚠️ Node Status: Warning",
                        description=f"Node `{node_url}` returned unexpected status code `{response.status_code}`.\nResponse Time: {response_time:.2f}ms",
                        color=0xFFA500
                    )
                    embed.add_field(name="Suggestions", value="Check SSL, logs, or service configurations.", inline=False)
                    await ctx.send(embed=embed)
            except requests.RequestException as e:
                embed = discord.Embed(
                    title="❌ Node Status: Critical",
                    description=f"Node `{node_url}` is unreachable.\nError: {e}",
                    color=0xFF0000
                )
                embed.add_field(name="Suggestions", value="Check if the node is running and verify network or Cloudflare settings.", inline=False)
                embed.set_footer(text="Immediate attention required!")
                await ctx.send(embed=embed)

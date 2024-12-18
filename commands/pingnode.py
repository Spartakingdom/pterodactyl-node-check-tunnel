from discord.ext import commands
import discord
import requests
import time

async def setup(bot):
    @bot.command(name="pingnode")
    async def ping_node(ctx, node_url: str = None):
        """Ping a node to check its response time."""
        if not node_url:
            await ctx.send("⚠️ Please provide a valid node URL. Example: `!pingnode https://example.com`")
            return

        try:
            start_time = time.time()
            response = requests.get(node_url, timeout=10)
            response_time = round((time.time() - start_time) * 1000)

            if response.status_code == 200:
                embed = discord.Embed(
                    title="✅ Node Ping Successful",
                    description=f"Node `{node_url}` responded successfully.",
                    color=discord.Color.green()
                )
            else:
                embed = discord.Embed(
                    title="⚠️ Node Ping Warning",
                    description=f"Node `{node_url}` responded with status code `{response.status_code}`.",
                    color=discord.Color.orange()
                )

            embed.add_field(name="Response Time", value=f"{response_time}ms", inline=False)
            embed.set_footer(text="Ping operation completed.")
            await ctx.send(embed=embed)

        except requests.RequestException as e:
            embed = discord.Embed(
                title="❌ Node Ping Failed",
                description=f"Node `{node_url}` could not be reached.",
                color=discord.Color.red()
            )
            embed.add_field(name="Error", value=str(e), inline=False)
            embed.set_footer(text="Ping operation failed.")
            await ctx.send(embed=embed)

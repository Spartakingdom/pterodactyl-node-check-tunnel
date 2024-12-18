from discord.ext import commands
import discord
import requests

async def setup(bot):
    @bot.command(name="nodestatus")
    async def node_status(ctx, node_url: str = None):
        """Check the status of a specific node."""
        if not node_url:
            await ctx.send("⚠️ Please provide a node URL. Example: `!nodestatus https://example.com`")
            return

        try:
            response = requests.get(node_url, timeout=10)
            response_time = round(response.elapsed.total_seconds() * 1000)

            if response.status_code == 200:
                embed = discord.Embed(
                    title="✅ Node Status: Operational",
                    description=f"Node `{node_url}` is operational.",
                    color=discord.Color.green()
                )
            elif response.status_code == 401:
                embed = discord.Embed(
                    title="✅ Node Status: Authentication Required",
                    description=f"Node `{node_url}` responded with status code 401.",
                    color=discord.Color.orange()
                )
            else:
                embed = discord.Embed(
                    title="⚠️ Node Status: Warning",
                    description=f"Node `{node_url}` responded with status code `{response.status_code}`.",
                    color=discord.Color.orange()
                )

            embed.add_field(name="Response Time", value=f"{response_time}ms", inline=False)
            embed.set_footer(text="Node status check completed.")
            await ctx.send(embed=embed)

        except requests.RequestException as e:
            embed = discord.Embed(
                title="❌ Node Status: Unreachable",
                description=f"Node `{node_url}` could not be reached.",
                color=discord.Color.red()
            )
            embed.add_field(name="Error", value=str(e), inline=False)
            embed.set_footer(text="Node status check failed.")
            await ctx.send(embed=embed)

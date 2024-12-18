from discord.ext import commands
import discord

async def setup(bot):
    @bot.command(name="status")
    async def status(ctx):
        """Check the bot's current status."""
        embed = discord.Embed(
            title="Bot Status",
            description="The bot is currently online and operational.",
            color=discord.Color.green()
        )
        embed.add_field(name="Latency", value=f"{round(bot.latency * 1000)}ms", inline=False)
        embed.set_footer(text="Status check completed.")
        await ctx.send(embed=embed)

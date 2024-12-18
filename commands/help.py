from discord.ext import commands
import discord

async def setup(bot):
    @bot.command(name="help")
    async def help_command(ctx):
        """Shows this help message."""
        embed = discord.Embed(
            title="Bot Commands",
            description="Here's a list of all available commands and their descriptions:",
            color=discord.Color.blue()
        )
        embed.add_field(
            name="!help",
            value="Shows this help message.",
            inline=False
        )
        embed.add_field(
            name="!addnode <url>",
            value="Adds a new node to the list.",
            inline=False
        )
        embed.add_field(
            name="!removenode <url>",
            value="Removes a node from the list.",
            inline=False
        )
        embed.add_field(
            name="!showlog [lines]",
            value="Displays the last few lines of the log file. Defaults to 10 lines if not specified.",
            inline=False
        )
        embed.add_field(
            name="!pingnode <url>",
            value="Pings a node to check its response time.",
            inline=False
        )
        embed.add_field(
            name="!nodestatus <url>",
            value="Checks the status of a specific node.",
            inline=False
        )
        embed.add_field(
            name="!status",
            value="Checks the bot's current status.",
            inline=False
        )
        embed.set_footer(text="Use these commands in the right channel command.")

        await ctx.send(embed=embed)

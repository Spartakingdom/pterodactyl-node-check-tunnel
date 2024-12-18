from discord.ext import commands
import discord
import os

LOG_FILE_PATH = "logs/debug.log"

async def setup(bot):
    @bot.command(name="showlog")
    async def show_log(ctx, lines: int = 10):
        """Show the last few lines of the log file."""
        if not os.path.exists(LOG_FILE_PATH):
            await ctx.send("Log file not found.")
            return

        try:
            with open(LOG_FILE_PATH, "r") as log_file:
                log_lines = log_file.readlines()

            last_lines = log_lines[-lines:]

            log_content = "".join(last_lines)
            if len(log_content) > 1990:
                log_content = log_content[-1990:]

            embed = discord.Embed(
                title="Node Logs",
                description=f"Last {lines} lines from the log file:",
                color=discord.Color.blue()
            )
            embed.add_field(name="Logs", value=f"```{log_content}```", inline=False)
            embed.set_footer(text="Log retrieval successful.")

            await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send(f"An error occurred while reading the log file: {e}")

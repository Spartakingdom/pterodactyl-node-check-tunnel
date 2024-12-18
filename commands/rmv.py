from discord.ext import commands
import discord

async def setup(bot):
    @bot.command(name="rmv")
    async def remove_messages(ctx):
        if not ctx.channel.permissions_for(ctx.guild.me).manage_messages:
            await ctx.send("I do not have permission to delete messages in this channel.")
            return
        try:
            def is_bot_or_command(m):
                return m.author == bot.user or m.content.startswith("!")
            deleted = await ctx.channel.purge(limit=100, check=is_bot_or_command)
            await ctx.send(f"Removed {len(deleted)} bot and command messages.", delete_after=5)
        except discord.Forbidden:
            await ctx.send("I do not have permission to delete messages in this channel.")
        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

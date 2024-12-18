from discord.ext import commands
import json
import os

def load_nodes():
    if os.path.exists("nodes.json"):
        with open("nodes.json", "r") as f:
            return json.load(f)
    return {"nodes": []}

def save_nodes(nodes_data):
    with open("nodes.json", "w") as f:
        json.dump(nodes_data, f, indent=4)

async def setup(bot):
    @bot.command(name="removenode")
    async def remove_node(ctx, node_url: str = None):
        """Remove a node from the list."""
        if not node_url:
            await ctx.send("⚠️ Please provide a node URL. Example: `!removenode https://example.com`")
            return

        nodes_data = load_nodes()

        if node_url not in nodes_data["nodes"]:
            await ctx.send(f"⚠️ Node `{node_url}` is not in the list.")
            return

        nodes_data["nodes"].remove(node_url)
        save_nodes(nodes_data)
        await ctx.send(f"✅ Node `{node_url}` has been removed successfully!")

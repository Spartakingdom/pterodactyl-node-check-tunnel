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
    @bot.command(name="addnode")
    async def add_node(ctx, node_url: str = None):
        """Add a new node to the list."""
        if not node_url:
            await ctx.send("⚠️ Please provide a node URL. Example: `!addnode https://example.com`")
            return

        nodes_data = load_nodes()

        if node_url in nodes_data["nodes"]:
            await ctx.send(f"⚠️ Node `{node_url}` is already in the list.")
            return

        nodes_data["nodes"].append(node_url)
        save_nodes(nodes_data)
        await ctx.send(f"✅ Node `{node_url}` has been added successfully!")

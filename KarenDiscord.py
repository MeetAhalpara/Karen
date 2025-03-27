# # from app.discordBot.discordApi import client, discordToken

# # if __name__ == "__main__":
# #     client.run(discordToken)

import discord
import openai
import os
from dotenv import load_dotenv
from discord.ext import commands

# Load API keys
load_dotenv()
DISCORD_TOKEN = os.getenv("KAREN_DISCORD")
OPENAI_API_KEY = os.getenv("KAREN_API")

# Set up OpenAI API
client = openai.OpenAI(api_key=OPENAI_API_KEY)    # Updated client instantiation

# Create Discord bot
intents = discord.Intents.default()
intents.message_content = True  # Ensure the bot can read messages
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()  # Sync slash commands
        print(f"✅ Logged in as {bot.user}")
        print(f"🔄 Synced {len(synced)} commands: {[cmd.name for cmd in synced]}")
    except Exception as e:
        print(f"❌ Slash command sync error: {e}")

@bot.tree.command(name="karen", description="Ask the Karen a question")
async def chat(interaction: discord.Interaction, message: str):
    await interaction.response.defer(thinking=True)
    await interaction.followup.send("Karen is thinking...")
    
    try:
        print("🔄 Sending request to OpenAI...")
        response = client.chat.completions.create(  # New API format
            model="gpt-4o",
            messages=[{"role": "user", "content": message}]
        )
        reply = response.choices[0].message.content
    except Exception as e:
        reply = f"❌ OpenAI Error: {str(e)}"

    await interaction.followup.send(reply)

# Run the bot
bot.run(DISCORD_TOKEN)

# import discord
# import os
# import requests
# from dotenv import load_dotenv
# from discord.ext import commands

# # Load API keys
# load_dotenv()
# DISCORD_TOKEN = os.getenv("KAREN_DISCORD")
# DEEPSEEK_API_KEY = os.getenv("KAREN_API2")
# DEEPSEEK_ENDPOINT = "https://api.deepseek.com"  # Adjust if necessary

# # Create Discord bot
# intents = discord.Intents.default()
# intents.message_content = True  # Ensure the bot can read messages
# bot = commands.Bot(command_prefix="!", intents=intents)

# @bot.event
# async def on_ready():
#     try:
#         synced = await bot.tree.sync()  # Sync slash commands
#         print(f"✅ Logged in as {bot.user}")
#         print(f"🔄 Synced {len(synced)} commands: {[cmd.name for cmd in synced]}")
#     except Exception as e:
#         print(f"❌ Slash command sync error: {e}")

# @bot.tree.command(name="karen", description="Ask the Karen a question")
# async def chat(interaction: discord.Interaction, message: str):
#     await interaction.response.defer(thinking=True)
#     await interaction.followup.send("Karen is thinking...")
    
#     try:
#         print("🔄 Sending request to DeepSeek API...")
#         headers = {"Authorization": f"Bearer {DEEPSEEK_API_KEY}", "Content-Type": "application/json"}
#         payload = {
#             "model": "deepseek-chat",
#             "messages": [{"role": "user", "content": message}]
#         }
        
#         response = requests.post(DEEPSEEK_ENDPOINT, json=payload, headers=headers)
#         response_data = response.json()
        
#         if "choices" in response_data and response_data["choices"]:
#             reply = response_data["choices"][0]["message"]["content"]
#         else:
#             reply = "❌ DeepSeek API Error: No valid response received."
        
#     except Exception as e:
#         reply = f"❌ DeepSeek API Error: {str(e)}"
    
#     await interaction.followup.send(reply)

# # Run the bot
# bot.run(DISCORD_TOKEN)

# import discord
# import os
# import requests
# import json
# from dotenv import load_dotenv
# from discord.ext import commands

# # Load API keys from .env
# load_dotenv()
# DISCORD_TOKEN = os.getenv("KAREN_DISCORD")
# DEEPSEEK_API_KEY = os.getenv("KAREN_API2")
# DEEPSEEK_ENDPOINT = "https://api.deepseek.com/v1/chat/completions"  # Corrected endpoint

# # Create Discord bot
# intents = discord.Intents.default()
# intents.message_content = True  # Ensure the bot can read messages
# bot = commands.Bot(command_prefix="!", intents=intents)

# @bot.event
# async def on_ready():
#     try:
#         synced = await bot.tree.sync()  # Sync slash commands
#         print(f"✅ Logged in as {bot.user}")
#         print(f"🔄 Synced {len(synced)} commands: {[cmd.name for cmd in synced]}")
#     except Exception as e:
#         print(f"❌ Slash command sync error: {e}")

# @bot.tree.command(name="karen", description="Ask the Karen a question")
# async def chat(interaction: discord.Interaction, message: str):
#     await interaction.response.defer(thinking=True)  # Shows "Bot is thinking..." in Discord

#     try:
#         print("🔄 Sending request to DeepSeek API...")
#         headers = {
#             "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
#             "Content-Type": "application/json"
#         }
#         payload = {
#             "model": "deepseek-chat",  # Use "deepseek-reasoner" if you need better reasoning
#             "messages": [{"role": "user", "content": message}],
#             "stream": False  # Set to True if you want a streaming response
#         }

#         response = requests.post(DEEPSEEK_ENDPOINT, json=payload, headers=headers)
#         response_data = response.json()

#         if response.status_code == 200 and "choices" in response_data:
#             reply = response_data["choices"][0]["message"]["content"]
#         else:
#             reply = f"❌ DeepSeek API Error: {response_data.get('error', 'Unknown error')}"

#         print(f"✅ DeepSeek API Response: {reply}")

#     except Exception as e:
#         reply = f"❌ DeepSeek API Error: {str(e)}"

#     await interaction.followup.send(reply)

# # Run the bot
# bot.run(DISCORD_TOKEN)

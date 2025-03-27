# import discord
# import google.generativeai as genai
# import os
# from dotenv import load_dotenv
# from discord.ext import commands

# # Load API keys
# load_dotenv()
# DISCORD_TOKEN = os.getenv("KAREN_GEMINI_DISCORD")
# GEMINI_API_KEY = os.getenv("KAREN_GEMINI")

# # Configure Google Gemini API
# genai.configure(api_key=GEMINI_API_KEY)

# # Create Discord bot
# intents = discord.Intents.default()
# intents.message_content = True
# bot = commands.Bot(command_prefix="!", intents=intents)

# @bot.event
# async def on_ready():
#     await bot.tree.sync()
#     print(f"✅ Logged in as {bot.user}")

# @bot.tree.command(name="google_karen", description="Ask the Karen a question")
# async def chat(interaction: discord.Interaction, message: str):
#     await interaction.response.defer(thinking=True)
#     await interaction.followup.send("Karen is thinking...")

    
#     try:
#         model = genai.GenerativeModel("gemini-2.0-flash")
#         response = model.generate_content([{"text": message}])
#         reply = response.text if response.text else "🤖 No response received!"
#     except Exception as e:
#         reply = f"❌ Error: {str(e)}"

#     await interaction.followup.send(reply)

# # Run the bot
# bot.run(DISCORD_TOKEN)

# import discord
# import google.generativeai as genai
# import os
# from dotenv import load_dotenv
# from discord.ext import commands

# # Load API keys
# load_dotenv()
# DISCORD_TOKEN = os.getenv("KAREN_GEMINI_DISCORD")
# GEMINI_API_KEY = os.getenv("KAREN_GEMINI")

# # Configure Google Gemini API
# genai.configure(api_key=GEMINI_API_KEY)

# # Create Discord bot
# intents = discord.Intents.default()
# intents.message_content = True
# bot = commands.Bot(command_prefix="!", intents=intents)

# @bot.event
# async def on_ready():
#     await bot.tree.sync()
#     print(f"✅ Logged in as {bot.user}")

# @bot.tree.command(name="google_karen", description="Ask Karen a question")
# async def chat(interaction: discord.Interaction, message: str):
#     await interaction.response.defer()  # Shows "Karen is thinking..." in UI

#     try:
#         model = genai.GenerativeModel("gemini-2.0-flash")
#         response = model.generate_content([{"text": message}])
#         reply = response.text if response.text else "🤖 No response received!"

#         MAX_LENGTH = 2000  # Discord's character limit

#         if len(reply) > MAX_LENGTH:
#             await interaction.followup.send(
#                 "❌ Response is too long! Please try a shorter question."
#             )
#             print("⚠️ Error: Response exceeded 2000 characters.")
#         else:
#             await interaction.followup.send(reply)

#     except Exception as e:
#         error_msg = f"❌ Error: {str(e)}"
#         print(error_msg)  # Logs error in console
#         await interaction.followup.send(error_msg)

# # Run the bot
# bot.run(DISCORD_TOKEN)

import discord
import google.generativeai as genai
import os
from dotenv import load_dotenv
from discord.ext import commands

# Load API keys
load_dotenv()
DISCORD_TOKEN = os.getenv("KAREN_GEMINI_DISCORD")
GEMINI_API_KEY = os.getenv("KAREN_GEMINI")
NOTIFY_CHANNEL_ID = int(os.getenv("DISCORD_NOTIFY_CHANNEL", 0))  # Channel ID for bot status updates

# Configure Google Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# Create Discord bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"✅ Logged in as {bot.user}")

    # Send online message in the configured channel
    if NOTIFY_CHANNEL_ID:
        channel = bot.get_channel(NOTIFY_CHANNEL_ID)
        if channel:
            await channel.send("✅ **Karen is now online!**")


@bot.tree.command(name="google_karen", description="Ask Karen a question")
async def chat(interaction: discord.Interaction, message: str):
    await interaction.response.defer()  # Shows "Karen is thinking..." in UI

    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content([{"text": message}])
        reply = response.text if response.text else "🤖 No response received!"

        MAX_LENGTH = 2000  # Discord's character limit

        if len(reply) > MAX_LENGTH:
            await interaction.followup.send(
                "❌ Response is too long! Please try a shorter question."
            )
            print("⚠️ Error: Response exceeded 2000 characters.")
        else:
            await interaction.followup.send(reply)

    except Exception as e:
        error_msg = f"❌ Error: {str(e)}"
        print(error_msg)  # Logs error in console
        await interaction.followup.send(error_msg)

# Run the bot
bot.run(DISCORD_TOKEN)
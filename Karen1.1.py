# import os
# import discord
# import requests
# import json
# import re
# import google.generativeai as genai
# from dotenv import load_dotenv

# # Load API keys from .env file
# load_dotenv()
# KarenDiscord = os.getenv("KAREN_GEMINI_DISCORD")
# TMDB_API_KEY = os.getenv("TMDB_API_KEY")
# GOOGLE_API_KEY = os.getenv("KAREN_GEMINI")

# # Configure Gemini AI
# genai.configure(api_key=GOOGLE_API_KEY)

# # Enable intents
# intents = discord.Intents.default()
# intents.messages = True
# intents.message_content = True  # Required to read messages

# # Create bot instance
# client = discord.Client(intents=intents)
# user_states = {}

# def get_genres():
#     """Fetches movie genres from TMDB API."""
#     url = f"https://api.themoviedb.org/3/genre/movie/list?api_key={TMDB_API_KEY}&language=en-US"
#     response = requests.get(url)
    
#     if response.status_code == 200:
#         genres = response.json().get("genres", [])
#         genre_dict = {genre["name"].lower(): genre["id"] for genre in genres}
#         return genre_dict
#     return {}  # Return empty dict if API call fails

# # Fetch genres at bot startup
# GENRE_DICT = get_genres()

# def analyze_preferences(user_input):
#     """Uses Gemini API to analyze user preferences for genres and moods."""
#     model = genai.GenerativeModel("gemini-2.0-flash")
#     prompt = f'''
#     Extract movie preferences from the user's message. Identify:
#     - Preferred genre (if mentioned, else omit it)
#     - Disliked genres (if mentioned, else omit it)
#     - Mood (if mentioned, else omit it)
#     User's Message: "{user_input}"
#     Reply in JSON format:
#     {{
#         "preferred_genre": "Extracted preferred genre (if any, else omit)",
#         "disliked_genre": ["Extracted disliked genre(s) (if any, else omit)"],
#         "mood": "Extracted mood (if any, else omit)"
#     }}
#     '''
#     try:
#         response = model.generate_content(prompt)
#         if response and response.text.strip():  # Ensure response is not empty
#             try:
#                 return json.loads(response.text)  # Try direct JSON parsing first
#             except json.JSONDecodeError:
#                 pass  # Move to regex extraction
            
#         json_match = re.search(r'\{.*\}', response.text.strip(), re.DOTALL)
#         if json_match:
#             return json.loads(json_match.group())

#         print("⚠️ No valid JSON found in Gemini response. Returning empty preferences.")
#         return {}

#     except Exception as e:
#         print(f"❌ Error parsing Gemini response: {e}. Using default values.")
#         return {}

# @client.event
# async def on_ready():
#     print(f"Bot is online as {client.user}")

# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return

#     user_id = message.author.id  # Track user ID for state handling

#     if message.content.lower() == "hello":
#         await message.channel.send("Hey there! How you doing? 😊 Ready to find a great movie? \n (Reply with 'yeah', 'yes', or 'yo' to continue, or 'no' to exit)")
#         user_states[user_id] = "awaiting_confirmation"  # Store state for user response

#     elif user_states.get(user_id) == "awaiting_confirmation":
#         if message.content.lower() in ["yeah", "yes", "yo"]:
#             if not GENRE_DICT:
#                 await message.channel.send("❌ Unable to fetch genres. Please try again later.")
#                 return

#             genres_message = "**🎬 Available Genres:**\n" + "\n".join([f"- {genre.capitalize()}" for genre in GENRE_DICT.keys()])
#             genres_message += "\n\n👉 **Describe the kind of movies you like** (e.g., 'I love sci-fi but hate romance and slow movies'):"
            
#             await message.channel.send(genres_message)
#             user_states[user_id] = "awaiting_preferences"  # Move to next state

#         elif message.content.lower() == "no":
#             await message.channel.send("Alright, no worries! Have a great day! 😊")
#             user_states.pop(user_id, None)  # Reset state

#     elif user_states.get(user_id) == "awaiting_preferences":
#         preferences = analyze_preferences(message.content)

#         preferred_genre = preferences.get("preferred_genre", "").lower() if isinstance(preferences.get("preferred_genre"), str) else ""
#         disliked_genres = preferences.get("disliked_genre", []) if isinstance(preferences.get("disliked_genre"), list) else []
#         mood = preferences.get("mood", "").lower() if isinstance(preferences.get("mood"), str) else ""

#         valid_disliked_genres = [dg for dg in disliked_genres if dg in GENRE_DICT]

#         if not preferred_genre:
#             await message.channel.send("\n❌ You must select a genre you like. Please try again.")
#             return

#         if not valid_disliked_genres:
#             await message.channel.send("\n🤔 Do you want to continue without a Disliked Genre? (yes/no):")
#             user_states[user_id] = "awaiting_disliked_confirmation"
#             return

#         await message.channel.send(f"🎥 Your Preferences:\n- **Preferred Genre:** {preferred_genre.capitalize()}\n- **Disliked Genres:** {', '.join(valid_disliked_genres) if valid_disliked_genres else 'None'}\n- **Mood:** {mood.capitalize() if mood else 'Not specified'}")
#         user_states.pop(user_id, None)  # Reset state after handling

#     elif user_states.get(user_id) == "awaiting_disliked_confirmation":
#         if message.content.lower() == "yes":
#             await message.channel.send("Great! I'll find movies based on your preferences. 🎬🍿")
#         elif message.content.lower() == "no":
#             await message.channel.send("👉 Enter genres you dislike (comma-separated):")
#             user_states[user_id] = "awaiting_disliked_genres"

#     elif user_states.get(user_id) == "awaiting_disliked_genres":
#         disliked_genres_input = message.content.lower().split(",")
#         valid_disliked_genres = [g.strip() for g in disliked_genres_input if g.strip() in GENRE_DICT]

#         await message.channel.send(f"🎥 Updated Preferences:\n- **Disliked Genres:** {', '.join(valid_disliked_genres) if valid_disliked_genres else 'None'}")
#         user_states.pop(user_id, None)  # Reset state

# # Run the bot
# client.run(KarenDiscord)

# import os
# import discord
# import requests
# import json
# import re
# import google.generativeai as genai
# from dotenv import load_dotenv

# # Load API keys from .env file
# load_dotenv()
# KarenDiscord = os.getenv("KAREN_GEMINI_DISCORD")
# TMDB_API_KEY = os.getenv("TMDB_API_KEY")
# GOOGLE_API_KEY = os.getenv("KAREN_GEMINI")

# # Configure Gemini AI
# genai.configure(api_key=GOOGLE_API_KEY)

# # Enable intents
# intents = discord.Intents.default()
# intents.messages = True
# intents.message_content = True  # Required to read messages

# # Create bot instance
# client = discord.Client(intents=intents)
# user_states = {}

# MOODS = {
#     "fast-paced": ["action-packed", "intense", "high-energy"],
#     "slow": ["calm", "leisurely", "steady"],
#     "thoughtful": ["deep", "philosophical", "insightful"],
#     "emotional": ["heartfelt", "moving", "tearjerker"],
#     "relaxing": ["chill", "easygoing", "soothing"],
#     "thrilling": ["suspenseful", "exciting", "edge-of-seat"]
# }

# def get_genres():
#     """Fetches movie genres from TMDB API."""
#     url = f"https://api.themoviedb.org/3/genre/movie/list?api_key={TMDB_API_KEY}&language=en-US"
#     response = requests.get(url)
    
#     if response.status_code == 200:
#         genres = response.json().get("genres", [])
#         return {genre["name"].lower(): genre["id"] for genre in genres}
#     return {}

# # Fetch genres at bot startup
# GENRE_DICT = get_genres()

# def analyze_preferences(user_input):
#     """Uses Gemini AI to analyze user preferences."""
#     model = genai.GenerativeModel("gemini-2.0-flash")
#     prompt = f'''
#     Extract movie preferences from the user's message. Identify:
#     - Preferred genre (if mentioned, else omit it)
#     - Disliked genres (if mentioned, else omit it)
#     - Mood (if mentioned, else omit it)
#     User's Message: "{user_input}"
#     Reply in JSON format:
#     {{
#         "preferred_genre": "Extracted preferred genre (if any, else omit)",
#         "disliked_genre": ["Extracted disliked genre(s) (if any, else omit)"],
#         "mood": "Extracted mood (if any, else omit)"
#     }}
#     '''
#     try:
#         response = model.generate_content(prompt)
#         if response and response.text.strip():
#             try:
#                 return json.loads(response.text)  # Try direct JSON parsing
#             except json.JSONDecodeError:
#                 pass  # Move to regex extraction
            
#         json_match = re.search(r'\{.*\}', response.text.strip(), re.DOTALL)
#         if json_match:
#             return json.loads(json_match.group())

#         return {}
#     except Exception as e:
#         print(f"❌ Error parsing Gemini response: {e}")
#         return {}

# def get_closest_mood(user_input):
#     """Finds the closest matching mood."""
#     for mood, synonyms in MOODS.items():
#         if user_input.lower() in [mood] + synonyms:
#             return mood
#     return None

# @client.event
# async def on_ready():
#     print(f"Bot is online as {client.user}")

# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return

#     user_id = message.author.id  # Track user ID for state handling

#     if message.content.lower() == "hello":
#         await message.channel.send("Hey there! 😊 Ready to find a great movie? \n (Reply with 'yeah', 'yes', or 'yo' to continue, or 'no' to exit)")
#         user_states[user_id] = "awaiting_confirmation"

#     elif user_states.get(user_id) == "awaiting_confirmation":
#         if message.content.lower() in ["yeah", "yes", "yo"]:
#             if not GENRE_DICT:
#                 await message.channel.send("❌ Unable to fetch genres. Please try again later.")
#                 return

#             genres_message = "**🎬 Available Genres:**\n" + "\n".join([f"- {genre.capitalize()}" for genre in GENRE_DICT.keys()])
#             genres_message += "\n\n👉 **Describe the kind of movies you like** (e.g., 'I love sci-fi but hate romance and slow movies'):"
            
#             await message.channel.send(genres_message)
#             user_states[user_id] = "awaiting_preferences"

#         elif message.content.lower() == "no":
#             await message.channel.send("Alright, no worries! Have a great day! 😊")
#             user_states.pop(user_id, None)

#     elif user_states.get(user_id) == "awaiting_preferences":
#         preferences = analyze_preferences(message.content)

#         preferred_genre = preferences.get("preferred_genre", "").lower() if isinstance(preferences.get("preferred_genre"), str) else ""
#         disliked_genres = preferences.get("disliked_genre", []) if isinstance(preferences.get("disliked_genre"), list) else []
#         mood = preferences.get("mood", "").lower() if isinstance(preferences.get("mood"), str) else ""

#         valid_disliked_genres = [dg for dg in disliked_genres if dg in GENRE_DICT]

#         if not preferred_genre:
#             await message.channel.send("\n❌ You must select a genre you like. Please try again.")
#             return

#         if not valid_disliked_genres:
#             await message.channel.send("\n🤔 Do you want to continue without a Disliked Genre? (yes/no):")
#             user_states[user_id] = "awaiting_disliked_confirmation"
#             user_states[f"{user_id}_preferred_genre"] = preferred_genre
#             return

#         user_states[user_id] = "awaiting_mood"
#         user_states[f"{user_id}_preferred_genre"] = preferred_genre
#         user_states[f"{user_id}_disliked_genres"] = valid_disliked_genres
#         await message.channel.send("\n🎭 Available Moods: " + ", ".join(MOODS.keys()) + "\n\n🤔 Do you want to continue without selecting a Mood? (yes/no):")

#     elif user_states.get(user_id) == "awaiting_disliked_confirmation":
#         if message.content.lower() == "yes":
#             await message.channel.send("\n🎭 Available Moods: " + ", ".join(MOODS.keys()) + "\n\n🤔 Do you want to continue without selecting a Mood? (yes/no):")
#             user_states[user_id] = "awaiting_mood"
#         elif message.content.lower() == "no":
#             await message.channel.send("\n👉 Enter genres you dislike (comma-separated):")
#             user_states[user_id] = "awaiting_disliked_genres"

#     elif user_states.get(user_id) == "awaiting_disliked_genres":
#         disliked_genres_input = message.content.lower().split(",")
#         valid_disliked_genres = [g.strip() for g in disliked_genres_input if g.strip() in GENRE_DICT]

#         await message.channel.send(f"\n🎭 Available Moods: " + ", ".join(MOODS.keys()) + "\n\n🤔 Do you want to continue without selecting a Mood? (yes/no):")
#         user_states[user_id] = "awaiting_mood"
#         user_states[f"{user_id}_disliked_genres"] = valid_disliked_genres

#     elif user_states.get(user_id) == "awaiting_mood":
#         if message.content.lower() == "yes":
#             mood = "Not specified"
#         else:
#             mood = get_closest_mood(message.content)
#             if not mood:
#                 await message.channel.send("\n❌ Invalid mood. Please choose from the available moods.")
#                 return

#         preferred_genre = user_states.pop(f"{user_id}_preferred_genre", "Unknown")
#         disliked_genres = user_states.pop(f"{user_id}_disliked_genres", [])

#         await message.channel.send(f"\n🎬 **Extracted Preferences:**\n✅ Preferred Genre: {preferred_genre.capitalize()}\n❌ Disliked Genres: {', '.join(disliked_genres).capitalize() if disliked_genres else 'None'}\n🎭 Mood: {mood.capitalize()}")
#         user_states.pop(user_id, None)

# client.run(KarenDiscord)



import os
import discord
import requests
import json
import re
import google.generativeai as genai
from dotenv import load_dotenv
from fetchMovies import fetchMovies

# Load API keys from .env file
load_dotenv()
KarenDiscord = os.getenv("KAREN_GEMINI_DISCORD")
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
GOOGLE_API_KEY = os.getenv("KAREN_GEMINI")

# Configure Gemini AI
genai.configure(api_key=GOOGLE_API_KEY)

# Enable intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True  # Required to read messages

# Create bot instance
client = discord.Client(intents=intents)
user_states = {}

MOODS = {
    "fast-paced": ["action-packed", "intense", "high-energy"],
    "slow": ["calm", "leisurely", "steady"],
    "thoughtful": ["deep", "philosophical", "insightful"],
    "emotional": ["heartfelt", "moving", "tearjerker"],
    "relaxing": ["chill", "easygoing", "soothing"],
    "thrilling": ["suspenseful", "exciting", "edge-of-seat"]
}

def get_genres():
    """Fetches movie genres from TMDB API."""
    url = f"https://api.themoviedb.org/3/genre/movie/list?api_key={TMDB_API_KEY}&language=en-US"
    response = requests.get(url)
    
    if response.status_code == 200:
        genres = response.json().get("genres", [])
        return {genre["name"].lower(): genre["id"] for genre in genres}
    return {}

# Fetch genres at bot startup
GENRE_DICT = get_genres()

def analyze_preferences(user_input):
    """Uses Gemini AI to analyze user preferences."""
    model = genai.GenerativeModel("gemini-2.0-flash")
    prompt = f'''
    Extract movie preferences from the user's message. Identify:
    - Preferred genre (if mentioned, else omit it)
    - Disliked genres (if mentioned, else omit it)
    - Mood (if mentioned, else omit it)
    User's Message: "{user_input}"
    Reply in JSON format:
    {{
        "preferred_genre": "Extracted preferred genre (if any, else omit)",
        "disliked_genre": ["Extracted disliked genre(s) (if any, else omit)"],
        "mood": "Extracted mood (if any, else omit)"
    }}
    '''
    try:
        response = model.generate_content(prompt)
        if response and response.text.strip():
            try:
                return json.loads(response.text)  # Try direct JSON parsing
            except json.JSONDecodeError:
                pass  # Move to regex extraction
            
        json_match = re.search(r'\{.*\}', response.text.strip(), re.DOTALL)
        if json_match:
            return json.loads(json_match.group())

        return {}
    except Exception as e:
        print(f"❌ Error parsing Gemini response: {e}")
        return {}

def get_closest_mood(user_input):
    """Finds the closest matching mood."""
    for mood, synonyms in MOODS.items():
        if user_input.lower() in [mood] + synonyms:
            return mood
    return None

@client.event
async def on_ready():
    print(f"Bot is online as {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    user_id = message.author.id  # Track user ID for state handling

    if message.content.lower() == "hello":
        await message.channel.send("Hey there! 😊 Ready to find a great movie? \n (Reply with 'yeah', 'yes', or 'yo' to continue, or 'no' to exit)")
        user_states[user_id] = "awaiting_confirmation"

    elif user_states.get(user_id) == "awaiting_confirmation":
        if message.content.lower() in ["yeah", "yes", "yo"]:
            if not GENRE_DICT:
                await message.channel.send("❌ Unable to fetch genres. Please try again later.")
                return

            genres_message = "**🎬 Available Genres:**\n" + "\n".join([f"- {genre.capitalize()}" for genre in GENRE_DICT.keys()])
            genres_message += "\n\n👉 **Describe the kind of movies you like** (e.g., 'I love sci-fi but hate romance and slow movies'):"
            
            await message.channel.send(genres_message)
            user_states[user_id] = "awaiting_preferences"

        elif message.content.lower() == "no":
            await message.channel.send("Alright, no worries! Have a great day! 😊")
            user_states.pop(user_id, None)

    elif user_states.get(user_id) == "awaiting_preferences":
        preferences = analyze_preferences(message.content)

        preferred_genre = preferences.get("preferred_genre", "").lower() if isinstance(preferences.get("preferred_genre"), str) else ""
        disliked_genres = preferences.get("disliked_genre", []) if isinstance(preferences.get("disliked_genre"), list) else []
        mood = preferences.get("mood", "").lower() if isinstance(preferences.get("mood"), str) else ""

        valid_disliked_genres = [dg for dg in disliked_genres if dg in GENRE_DICT]

        if not preferred_genre:
            await message.channel.send("\n❌ You must select a genre you like. Please try again.")
            return

        if not valid_disliked_genres:
            await message.channel.send("\n🤔 Do you want to continue without a Disliked Genre? (yes/no):")
            user_states[user_id] = "awaiting_disliked_confirmation"
            user_states[f"{user_id}_preferred_genre"] = preferred_genre
            return

        user_states[user_id] = "awaiting_mood"
        user_states[f"{user_id}_preferred_genre"] = preferred_genre
        user_states[f"{user_id}_disliked_genres"] = valid_disliked_genres
        await message.channel.send("\n🎭 Available Moods: " + ", ".join(MOODS.keys()) + "\n\n🤔 Do you want to continue without selecting a Mood? (yes/no):")

    elif user_states.get(user_id) == "awaiting_disliked_confirmation":
        if message.content.lower() == "yes":
            await message.channel.send("\n🎭 Available Moods: " + ", ".join(MOODS.keys()) + "\n\n🤔 Do you want to continue without selecting a Mood? (yes/no):")
            user_states[user_id] = "awaiting_mood"
        elif message.content.lower() == "no":
            await message.channel.send("\n👉 Enter genres you dislike (comma-separated):")
            user_states[user_id] = "awaiting_disliked_genres"

    elif user_states.get(user_id) == "awaiting_disliked_genres":
        disliked_genres_input = message.content.lower().split(",")
        valid_disliked_genres = [g.strip() for g in disliked_genres_input if g.strip() in GENRE_DICT]

        await message.channel.send(f"\n🎭 Available Moods: " + ", ".join(MOODS.keys()) + "\n\n🤔 Do you want to continue without selecting a Mood? (yes/no):")
        user_states[user_id] = "awaiting_mood"
        user_states[f"{user_id}_disliked_genres"] = valid_disliked_genres

    elif user_states.get(user_id) == "awaiting_mood":
        if message.content.lower() == "yes":
            mood = None  # Keep it None instead of "Not specified"
        else:
            mood = get_closest_mood(message.content)
            if not mood:
                await message.channel.send("\n❌ Invalid mood. Please choose from the available moods.")
                return

        # ✅ Ensure genre is stored correctly
        preferred_genre = user_states.get(f"{user_id}_preferred_genre", None)
        disliked_genres = user_states.get(f"{user_id}_disliked_genres", [])

        if not preferred_genre:
            await message.channel.send("❌ Error: Preferred genre is missing. Please restart the process.")
            return

        extracted_preferences = "**🎬 Extracted Preferences:**\n"
        extracted_preferences += f"✅ **Preferred Genre:** {preferred_genre.capitalize()}\n"

        if disliked_genres:
            extracted_preferences += f"❌ **Disliked Genre(s):** {', '.join([genre.capitalize() for genre in disliked_genres])}\n"

        if mood:
            extracted_preferences += f"🎭 **Mood:** {mood.capitalize()}\n"

        await message.channel.send(extracted_preferences)

        # ✅ Store genre & disliked_genres before transitioning state
        user_states[user_id] = "awaiting_movie_source"
        user_states[f"{user_id}_preferred_genre"] = preferred_genre
        user_states[f"{user_id}_disliked_genres"] = disliked_genres

        selection_prompt = (
            "\n👉 **Do you want to see movies from Online or Karen's list?**\n"
            "1️⃣ **Online**\n"
            "2️⃣ **Karen**\n"
            "**Choose 1 or 2:**"
        )
        await message.channel.send(selection_prompt)

    elif user_states.get(user_id) == "awaiting_movie_source":
        preferred_genre = user_states.pop(f"{user_id}_preferred_genre", None)
        disliked_genres = user_states.pop(f"{user_id}_disliked_genres", [])

        if not preferred_genre:
            await message.channel.send("❌ Error: Preferred genre is missing. Please restart the process.")
            user_states.pop(user_id, None)  # Clear all states for fresh restart
            return

        if message.content == "1":
            await message.channel.send("\n📡 **Fetching fresh movies from Online...**")
            movies = await fetchMovies(preferred_genre, disliked_genres)

            if isinstance(movies, str):
                await message.channel.send(movies)
            elif movies:
                movie_list = "\n".join([f"🎬 {movie['title']} ({movie['release_date'][:4]})" for movie in movies[:10]])
                await message.channel.send(f"\n**I got the top {len(movies)} movies based on your preferences.**\nHere are some of them:\n{movie_list}")
            else:
                await message.channel.send("⚠️ No movies found. Try a different genre.")

        elif message.content == "2":
            await message.channel.send("✅ **You chose Karen's cached list! 🗂️**")
            # Implement fetching from Karen's list

        else:
            await message.channel.send("❌ **Invalid choice! Please select 1 (Online) or 2 (Karen).**")
            return

        user_states.pop(user_id, None)


client.run(KarenDiscord)
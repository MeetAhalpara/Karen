import discord
import os
import json
import re
import requests
import google.generativeai as genai
from dotenv import load_dotenv
from getMovies import fetch_movies_from_tmdb

# Load environment variables
load_dotenv()
DISCORD_TOKEN = os.getenv("KAREN_GEMINI_DISCORD")
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
GEMINI_API_KEY = os.getenv("KAREN_GEMINI")
CACHE_FILE = "movies_cache.json"

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# Common moods with synonyms
MOODS = {
    "fast-paced": ["fast", "quick", "intense"],
    "slow": ["slow-burn", "steady"],
    "thoughtful": ["deep", "philosophical"],
    "emotional": ["touching", "tearjerker", "heartfelt"],
    "relaxing": ["calm", "peaceful", "chill"],
    "thrilling": ["exciting", "suspenseful", "edge-of-seat"]
}

intents = discord.Intents.default()
intents.messages = True
client = discord.Client(intents=intents)

def get_genres():
    """Fetches movie genres from TMDB API."""
    url = f"https://api.themoviedb.org/3/genre/movie/list?api_key={TMDB_API_KEY}&language=en-US"
    response = requests.get(url)
    if response.status_code == 200:
        genres = response.json().get("genres", [])
        return {genre["name"].lower(): genre["id"] for genre in genres}
    return {}

def analyze_preferences(user_input):
    """Uses Gemini API to analyze user preferences for genres and moods."""
    model = genai.GenerativeModel("gemini-2.0-flash")
    prompt = f'''
    Extract movie preferences from the user's message. Identify:
    - Preferred genre (if mentioned, else omit it)
    - Disliked genres (if mentioned, else omit it)
    - Mood (if mentioned, else omit it)
    User's Message: "{user_input}"
    Reply in JSON format:
    {{"preferred_genre": "Extracted preferred genre (if any, else omit)",
      "disliked_genre": ["Extracted disliked genre(s) (if any, else omit)"],
      "mood": "Extracted mood (if any, else omit)"}}
    '''
    try:
        response = model.generate_content(prompt)
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

def load_cached_movies():
    """Loads cached movies from a JSON file."""
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as file:
            return json.load(file)
    return []

@client.event
async def on_ready():
    print(f'✅ {client.user} is now running!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return  # Ignore bot's own messages

    user_input = message.content.strip()
    genre_dict = get_genres()

    preferences = analyze_preferences(user_input)
    preferred_genre = preferences.get("preferred_genre", "").lower() if isinstance(preferences.get("preferred_genre"), str) else ""
    disliked_genres = preferences.get("disliked_genre", []) if isinstance(preferences.get("disliked_genre"), list) else []
    mood = preferences.get("mood", "").lower() if isinstance(preferences.get("mood"), str) else ""

    valid_disliked_genres = [dg for dg in disliked_genres if dg in genre_dict]

    for dg in disliked_genres:
        if dg in MOODS:
            mood = dg
            valid_disliked_genres.remove(dg)

    if not preferred_genre:
        await message.channel.send("❌ You must select a genre you like. Please try again.")
        return

    # Fetch movies from TMDB or cached data
    movies = fetch_movies_from_tmdb() if os.path.exists(CACHE_FILE) else load_cached_movies()

    preferred_genre_id = genre_dict.get(preferred_genre)
    filtered_movies = [
        movie for movie in movies
        if preferred_genre_id in movie.get("genre_ids", []) and
        not any(genre_dict.get(dg) in movie.get("genre_ids", []) for dg in valid_disliked_genres)
    ]

    if not filtered_movies:
        await message.channel.send("❌ No movies match your preferences. Showing top movies instead.")
        filtered_movies = movies[:5]  # Show top 5 movies if no exact match

    response = f"🎬 **Recommended Movies for You:**\n"
    for i, movie in enumerate(filtered_movies[:5], start=1):
        title = movie.get('title', 'Unknown Title')
        release_date = movie.get('release_date', 'Unknown Date')
        overview = movie.get('overview', 'No description available.')
        response += f"**{i}. {title} ({release_date})**\n   📝 {overview}\n\n"

    await message.channel.send(response)

# Run the bot
client.run(DISCORD_TOKEN)

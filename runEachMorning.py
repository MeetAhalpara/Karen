import requests
import os
import json
import re
import google.generativeai as genai
from dotenv import load_dotenv
from getMovies import fetch_movies_from_tmdb

# Load API keys
load_dotenv()
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

def load_cached_movies():
    """Loads cached movies efficiently and refreshes if outdated."""
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r") as file:
                data = json.load(file)
                if isinstance(data, list) and all("title" in movie for movie in data):
                    print(f"\n📁 Loaded {len(data)} cached movies.")
                    return data
        except (json.JSONDecodeError, KeyError) as e:
            print(f"⚠️ Cache error: {e}. Fetching fresh data...")
    else:
        print("⚠️ No cached movies found. Fetching fresh movie data...")
    
    # Fetch new movies if cache is missing or invalid
    movies = fetch_movies_from_tmdb()
    with open(CACHE_FILE, "w") as file:
        json.dump(movies, file, indent=4)
    print(f"✅ Cached {len(movies)} movies for future use.")
    return movies

if __name__ == "__main__":
    print("\n🎬 Welcome to the Karen Movie Recommendation Bot!")
    cached_movies = load_cached_movies()
    print(f"Loaded {len(cached_movies)} movies from cache.")

# import time

# CACHE_EXPIRATION = 24 * 60 * 60  # 24 hours

# def load_cached_movies():
#     """Loads cached movies from a JSON file and checks expiration."""
#     if os.path.exists(CACHE_FILE):
#         with open(CACHE_FILE, "r") as file:
#             data = json.load(file)
#             last_updated = data.get("timestamp", 0)
#             if time.time() - last_updated < CACHE_EXPIRATION:
#                 return data.get("movies", [])

#     print("⚠️ No cached movies found or expired. Fetching fresh movie data...")
#     fresh_movies = fetch_movies_from_tmdb()
    
#     # Save fresh data with timestamp
#     with open(CACHE_FILE, "w") as file:
#         json.dump({"timestamp": time.time(), "movies": fresh_movies}, file, indent=4)

#     return fresh_movies

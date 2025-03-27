import requests
import os
from dotenv import load_dotenv

# Load API Key from .env file
load_dotenv()
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
TMDB_MOVIE_URL = "https://api.themoviedb.org/3/discover/movie"

# A dictionary to hold user states
user_states = {}

# TMDB Genre ID Mapping
GENRE_MAPPING = {
    "action": 28, "adventure": 12, "animation": 16, "comedy": 35, "crime": 80,
    "documentary": 99, "drama": 18, "family": 10751, "fantasy": 14, "history": 36,
    "horror": 27, "music": 10402, "mystery": 9648, "romance": 10749, "sci-fi": 878,
    "thriller": 53, "war": 10752, "western": 37
}

def fetch_from_tmdb(pages=5):
    """Fetch top movies from TMDB API across multiple pages."""
    try:
        all_movies = []
        for page in range(1, pages + 1):
            params = {
                "api_key": TMDB_API_KEY,
                "language": "en-US",
                "sort_by": "popularity.desc",
                "include_adult": False,
                "include_video": False,
                "page": page
            }
            response = requests.get(TMDB_MOVIE_URL, params=params)
            response.raise_for_status()  # Raises error for HTTP failures
            data = response.json()
            movies = data.get("results", [])
            
            if not movies:
                break  # Stop if no movies on this page

            all_movies.extend(movies)

        return all_movies  # List of movies

    except Exception as e:
        print(f"❌ TMDB API Error: {e}")
        return []  # Return empty list if error occurs

async def fetchMovies(preferred_genre, disliked_genres, message, user_id):
    """Fetch movies from TMDB API and filter based on user preferences."""
    try:
        movies = fetch_from_tmdb()  # Fetch top movies

        if not movies:  # If empty list returned, means API error
            await message.channel.send("⚠️ **Error fetching movies. Please try again later.**")
            return

        total_movies = len(movies)  # Total fetched movies
        
        # ✅ Get genre ID for preferred genre
        preferred_genre_id = GENRE_MAPPING.get(preferred_genre.lower())

        if not preferred_genre_id:
            await message.channel.send("❌ **Invalid genre! Try again.**")
            return

        # ✅ Convert disliked genres to IDs
        disliked_genre_ids = {GENRE_MAPPING[g.lower()] for g in disliked_genres if g.lower() in GENRE_MAPPING}

        # ✅ Filter movies based on preferred genre
        filtered_movies = [
            movie for movie in movies if preferred_genre_id in movie.get('genre_ids', [])
        ]

        # ✅ Remove movies that contain any disliked genre
        if disliked_genre_ids:
            filtered_movies = [
                movie for movie in filtered_movies if not any(
                    genre in disliked_genre_ids for genre in movie.get("genre_ids", [])
                )
            ]

        filtered_count = len(filtered_movies)  # Number of filtered movies

        # ✅ Store filtered list for later use
        user_states[f"{user_id}_filtered_movies"] = filtered_movies

        # ✅ Notify user and ask how many movies they want
        await message.channel.send(
            f"\n📡 **Fetching fresh movies from Online...**\n"
            f"✅ **I got the top {total_movies} movies based on your preferences.**\n"
            f"⏳ Others will take more time as the server is busy.\n"
            f"🎬 **There are {filtered_count} {preferred_genre.lower()} movies selected based on your preferences.**\n\n"
            f"👉 **How many {preferred_genre.lower()} movies do you want to see?**"
        )

        # ✅ Update state for user to enter movie count
        user_states[user_id] = {
            "status": "awaiting_movie_count",
            "available_movies": filtered_count
        }

    except Exception as e:
        print(f"❌ Error fetching movies: {e}")
        await message.channel.send("⚠️ **Error fetching movies. Please try again later.**")

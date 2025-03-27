import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
TMDB_MOVIE_URL = "https://api.themoviedb.org/3/discover/movie"

def fetch_movies_from_tmdb(preferred_genre=None, disliked_genres=[], pages=5):
    if not TMDB_API_KEY:
        print("❌ TMDB API Key is missing. Please set it in environment variables.")
        return []
    TMDB_GENRES = {
    'action': 28,
    'adventure': 12,
    'animation': 16,
    'comedy': 35,
    'crime': 80,
    'documentary': 99,
    'drama': 18,
    'family': 10751,
    'fantasy': 14,
    'history': 36,
    'horror': 27,
    'music': 10402,
    'mystery': 9648,
    'romance': 10749,
    'science fiction': 878,
    'tv movie': 10770,
    'thriller': 53,
    'war': 10752,
    'western': 37
    }

    # Convert genre name to ID
    preferred_genre_id = TMDB_GENRES.get(preferred_genre.lower()) if preferred_genre else None
    disliked_genre_ids = [TMDB_GENRES.get(g.lower()) for g in disliked_genres if g.lower() in TMDB_GENRES]

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

        if preferred_genre_id:  
            params["with_genres"] = preferred_genre_id  # ✅ Fix: Pass the ID, not name

        # print(f"🛠️ DEBUG: Sending request to TMDB with params: {params}")  # Debugging line

        response = requests.get(TMDB_MOVIE_URL, params=params)

        if response.status_code == 200:
            movies = response.json().get("results", [])
            if not movies:
                print(f"⚠️ No movies found on page {page}.")
                break

            # Filter out disliked genres
            if disliked_genre_ids:
                movies = [
                    movie for movie in movies if not any(
                        genre in movie["genre_ids"] for genre in disliked_genre_ids
                    )
                ]

            all_movies.extend(movies)
        else:
            print(f"❌ Failed to fetch page {page}. Error {response.status_code}: {response.text}")
            break

    return all_movies

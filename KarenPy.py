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

def get_genres():
    """Fetches movie genres from TMDB API."""
    url = f"https://api.themoviedb.org/3/genre/movie/list?api_key={TMDB_API_KEY}&language=en-US"
    response = requests.get(url)
    if response.status_code == 200:
        genres = response.json().get("genres", [])
        genre_dict = {genre["name"].lower(): genre["id"] for genre in genres}
        print("\n🎬 Available Genres:")
        for genre in genre_dict.keys():
            print(f"- {genre.capitalize()}")
        return genre_dict
    print("❌ Error fetching genres:", response.status_code)
    return {}
#  Says catchs new movie each time 
# From here to 
def load_cached_movies():
    """Loads cached movies from a JSON file."""
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as file:
            return json.load(file)
    return []

def save_movies_to_cache(movies):
    """Saves movies to the cache file."""
    with open(CACHE_FILE, "w") as file:
        json.dump(movies, file, indent=4)

def fetch_movies():
    """Fetches movies from cache if available, otherwise fetches fresh data."""
    cached_movies = load_cached_movies()
    if cached_movies:
        print("⚡ Using cached movie data.")
        return cached_movies
    print("📡 Fetching fresh movies from TMDB...")
    movies = fetch_movies_from_tmdb()
    save_movies_to_cache(movies)
    return movies
# Here
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
    {{
        "preferred_genre": "Extracted preferred genre (if any, else omit)",
        "disliked_genre": ["Extracted disliked genre(s) (if any, else omit)"],
        "mood": "Extracted mood (if any, else omit)"
    }}
    '''
    try:
        response = model.generate_content(prompt)
        if response and response.text.strip():  # Ensure response is not empty
            try:
                return json.loads(response.text)  # Try direct JSON parsing first
            except json.JSONDecodeError:
                pass  # Move to regex extraction
            
        json_match = re.search(r'\{.*\}', response.text.strip(), re.DOTALL)
        if json_match:
            return json.loads(json_match.group())

        print("⚠️ No valid JSON found in Gemini response. Returning empty preferences.")
        return {}

    except Exception as e:
        print(f"❌ Error parsing Gemini response: {e}. Using default values.")
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
    print("⚠️ No cached movies found. Fetching fresh movie data...")
    return []

if __name__ == "__main__":
    print("\n🎬 Welcome to the Karen Movie Recommendation Bot!")
    genre_dict = get_genres()
    
    if not genre_dict:
        print("❌ No genres found. Exiting.")
        exit()

    while True:
        user_input = input("\n👉 Describe the kind of movies you like (e.g., 'I love sci-fi but hate romance and slow movies'): ")
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
            print("\n❌ You must select a genre you like. Please try again.")
            continue

        if not valid_disliked_genres:
            choice = input("\n🤔 Do you want to continue without a Disliked Genre? (yes/no): ").strip().lower()
            if choice == "no":
                disliked_genres_input = input("\n👉 Enter genres you dislike (comma-separated): ")
                valid_disliked_genres = [g.strip().lower() for g in disliked_genres_input.split(",") if g.strip().lower() in genre_dict]

        if not mood:
            print("\n🎭 Available Moods: " + ", ".join(MOODS.keys()))
            choice = input("\n🤔 Do you want to continue without selecting a Mood? (yes/no): ").strip().lower()
            if choice == "no":
                while True:
                    mood_input = input("\n👉 Enter your preferred movie mood: ").strip().lower()
                    matched_mood = get_closest_mood(mood_input)
                    if matched_mood:
                        mood = matched_mood
                        break
                    else:
                        print("\n❌ Invalid mood. Please choose from the available moods.")

        break

    print(f"\n🎬 Extracted Preferences:")
    print(f"✅ Preferred Genre: {preferred_genre.capitalize()}")    
    if valid_disliked_genres:
        print(f"❌ Disliked Genre(s): {', '.join(valid_disliked_genres)}")
    if mood:
        print(f"🎭 Mood: {mood.capitalize()}")

    # Asking for the source of movies
    while True:
        source_choice = input("\n👉 Do you want to see movies from Online or Karen's cached list?\n1. Online\n2. Karen\nChoose 1 or 2: ").strip()
        if source_choice == "1":
            print("\n📡 Fetching fresh movies from Online...")
            # Fetch movies from TMDB
            movies = fetch_movies_from_tmdb()  # I will give to you 
            print(f"\nI got the top {len(movies)} movies based on your preferences. Others will take more time as the server is busy.")
            break
        elif source_choice == "2": # Ignore for now
            movies = load_cached_movies() 
            if not movies:
                print("⚠️ No cached movies found. Fetching fresh movie data...")
                movies = fetch_movies_from_tmdb()  # In case the cached file is empty
            print(f"\nThere are {len(movies)} movies available.")
            break
        else:
            print("❌ Invalid choice. Please enter '1' for Online or '2' for Karen's cached list.")

    preferred_genre_id = genre_dict.get(preferred_genre)
    filtered_movies = [
        movie for movie in movies
        if preferred_genre_id in movie.get("genre_ids", []) and
        not any(genre_dict.get(dg) in movie.get("genre_ids", []) for dg in valid_disliked_genres)
    ]

    if len(filtered_movies) == 0:
        print("\n❌ No movies match your preferences. Showing ALL movies in preferred genre instead.")
        filtered_movies = [movie for movie in movies if preferred_genre_id in movie.get("genre_ids", [])]

    
    print(f"There are {len(filtered_movies)} movies selected based on your preferences.")

    while True:
        try:
            count = int(input(f"\n👉 How many {preferred_genre} movies do you want to see? "))
            if count <= 0 or count > len(filtered_movies):
                print(f"⚠️ Please enter a number between 1 and {len(filtered_movies)}.")
                continue
            break
        except ValueError:
            print("❌ Invalid input. Please enter a valid number.")

    print("\n🎬 Recommended Movies:")
    for i, movie in enumerate(filtered_movies[:count], start=1):
        title = movie.get('title', 'Unknown Title')
        release_date = movie.get('release_date', 'Unknown Date')
        overview = movie.get('overview', 'No description available.')
        print(f"{i}. {title} ({release_date})")
        print(f"   Overview: {overview}\n")



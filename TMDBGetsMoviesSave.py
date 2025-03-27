# import requests
# import os
# import json
# from dotenv import load_dotenv

# # Load API keys
# load_dotenv()
# API_KEY = os.getenv("TMDB_API_KEY")
# CACHE_FILE = "movies_cache.json"

# # Function to fetch genres dynamically
# def get_genres():
#     url = f"https://api.themoviedb.org/3/genre/movie/list?api_key={API_KEY}&language=en-US"
#     response = requests.get(url)

#     if response.status_code == 200:
#         genres = response.json()["genres"]
#         return {genre["name"].lower(): genre["id"] for genre in genres}
#     else:
#         print("❌ Error fetching genres:", response.status_code)
#         exit()

# # Function to fetch all movies of a genre with proper pagination
# def fetch_movies(genre_id):
#     all_movies = []
#     page = 1

#     while True:
#         url = f"https://api.themoviedb.org/3/discover/movie"
#         params = {
#             "api_key": API_KEY,
#             "with_genres": genre_id,
#             "page": page
#         }
#         response = requests.get(url, params=params)

#         if response.status_code == 200:
#             data = response.json()
#             movies = data.get("results", [])

#             if not movies:  # Stop if no more movies
#                 break

#             all_movies.extend(movies)
#             page += 1

#             # Save the latest fetched movies to cache
#             with open(CACHE_FILE, "w") as file:
#                 json.dump(all_movies, file, indent=4)

#             if page > data.get("total_pages", 1):  # Stop if no more pages
#                 break
#         else:
#             print("❌ Error fetching movies:", response.status_code, response.text)
#             break

#     return all_movies

# # Function to load movies from cache if available
# def load_cached_movies():
#     if os.path.exists(CACHE_FILE):
#         with open(CACHE_FILE, "r") as file:
#             return json.load(file)
#     return None

# # Get available genres
# genre_dict = get_genres()

# # Display available genres
# print("\n🎬 Available Genres:")
# for genre in genre_dict.keys():
#     print(f"- {genre.capitalize()}")

# # Get user input
# preferred_genre = input("\nEnter your preferred genre from the list: ").strip().lower()
# disliked_genre = input("Enter a genre to exclude (optional): ").strip().lower()

# # Validate user input
# preferred_genre_id = genre_dict.get(preferred_genre)
# disliked_genre_id = genre_dict.get(disliked_genre)

# if not preferred_genre_id:
#     print("\n❌ Invalid genre! Please choose from the list above.")
#     exit()

# # Check if cache exists, otherwise fetch from API
# movies = load_cached_movies() or fetch_movies(preferred_genre_id)

# # Filter out movies containing the disliked genre
# filtered_movies = []
# for movie in movies:
#     movie_genres = movie.get("genre_ids", [])
#     if disliked_genre_id and genre_dict.get(disliked_genre) in movie_genres:
#         continue  # Skip movie if it contains the disliked genre
#     filtered_movies.append(movie)

# available_movies = len(filtered_movies)

# if available_movies == 0:
#     print("\nNo movies found that match your preferences.")
#     exit()

# # Ask how many movies to show (handle large dataset properly)
# while True:
#     num_movies = input(f"\nThere are {available_movies} movies available. How many do you want to see? ").strip()
#     if num_movies.isdigit() and 0 < int(num_movies) <= available_movies:
#         num_movies = int(num_movies)
#         break
#     print(f"❌ Please enter a number between 1 and {available_movies}.")

# # Display results
# print("\n🎬 Recommended Movies:")
# for i, movie in enumerate(filtered_movies[:num_movies], start=1):
#     title = movie.get("title", "Unknown Title")
#     release_date = movie.get("release_date", "Unknown Date")
#     overview = movie.get("overview", "No description available.")
#     print(f"{i}. {title} ({release_date})")
#     print(f"   Overview: {overview}\n")

# import requests
# import os
# import json
# from dotenv import load_dotenv

# # Load API keys
# load_dotenv()
# API_KEY = os.getenv("TMDB_API_KEY")
# CACHE_FILE = "movies_cache.json"

# # Function to fetch and cache genres from TMDB
# def get_genres():
#     url = f"https://api.themoviedb.org/3/genre/movie/list?api_key={API_KEY}&language=en-US"
#     response = requests.get(url)

#     if response.status_code == 200:
#         genres = response.json()["genres"]
#         return {genre["name"].lower(): genre["id"] for genre in genres}
#     else:
#         print("❌ Error fetching genres:", response.status_code)
#         exit()

# # Function to fetch and cache movies (avoids API limit issues)
# def fetch_movies(genre_id):
#     all_movies = []
#     page = 1

#     while True:
#         url = f"https://api.themoviedb.org/3/discover/movie?api_key={API_KEY}&with_genres={genre_id}&page={page}"
#         response = requests.get(url)

#         if response.status_code == 200:
#             data = response.json()
#             movies = data.get("results", [])

#             if not movies:  # Stop if no more movies
#                 break

#             all_movies.extend(movies)
#             page += 1

#             # Store data in cache file to avoid repeated API calls
#             with open(CACHE_FILE, "w") as file:
#                 json.dump(all_movies, file, indent=4)

#         else:
#             print("❌ Error fetching movies:", response.status_code)
#             break

#     return all_movies

# # Function to load movies from cache
# def load_cached_movies():
#     if os.path.exists(CACHE_FILE):
#         with open(CACHE_FILE, "r") as file:
#             return json.load(file)
#     return None

# # Get available genres
# genre_dict = get_genres()

# # Display available genres
# print("\n🎬 Available Genres:")
# for genre in genre_dict.keys():
#     print(f"- {genre.capitalize()}")

# # Get user input
# preferred_genre = input("\nEnter your preferred genre from the list: ").strip().lower()
# disliked_genre = input("Enter a genre to exclude (optional): ").strip().lower()

# # Validate user input
# preferred_genre_id = genre_dict.get(preferred_genre)
# disliked_genre_id = genre_dict.get(disliked_genre)

# if not preferred_genre_id:
#     print("\n❌ Invalid genre! Please choose from the list above.")
#     exit()

# # Check cache first, otherwise fetch from TMDB
# movies = load_cached_movies() or fetch_movies(preferred_genre_id)

# # ✅ Step 1: Get total movies before filtering
# total_movies = len(movies)

# # ✅ Step 2: Ensure proper filtering of the excluded genre
# if disliked_genre_id:
#     filtered_movies = [
#         movie for movie in movies
#         if str(disliked_genre_id) not in map(str, movie.get("genre_ids", []))  # Ensure proper filtering
#     ]
# else:
#     filtered_movies = movies

# available_movies = len(filtered_movies)  # Count only filtered movies

# if available_movies == 0:
#     print("\nNo movies found that match your preferences.")
#     exit()

# # ✅ Step 3: Show both total & filtered count before asking for user input
# print(f"\nThere are {total_movies} movies available.")
# print(f"There are {available_movies} movies selected based on your preferences.")

# # Ask how many movies to show
# while True:
#     num_movies = input(f"How many do you want to see? ").strip()
#     if num_movies.isdigit():
#         num_movies = int(num_movies)
#         if 0 < num_movies <= available_movies:
#             break
#     print(f"❌ Please enter a number between 1 and {available_movies}.")

# # Display results
# print("\n🎬 Recommended Movies:")
# for i, movie in enumerate(filtered_movies[:num_movies], start=1):
#     title = movie.get("title", "Unknown Title")
#     release_date = movie.get("release_date", "Unknown Date")
#     overview = movie.get("overview", "No description available.")
#     print(f"{i}. {title} ({release_date})")
#     print(f"   Overview: {overview}\n")


import requests
import os
import json
from dotenv import load_dotenv

# Load API keys
load_dotenv()
API_KEY = os.getenv("TMDB_API_KEY")
CACHE_FILE = "movies_cache.json"

# Function to fetch and cache genres from TMDB
def get_genres():
    url = f"https://api.themoviedb.org/3/genre/movie/list?api_key={API_KEY}&language=en-US"
    response = requests.get(url)

    if response.status_code == 200:
        genres = response.json()["genres"]
        return {genre["name"].lower(): genre["id"] for genre in genres}
    else:
        print("❌ Error fetching genres:", response.status_code)
        exit()

# Function to fetch and cache movies (avoids API limit issues)
def fetch_movies(genre_id):
    all_movies = []
    page = 1

    while True:
        url = f"https://api.themoviedb.org/3/discover/movie?api_key={API_KEY}&with_genres={genre_id}&page={page}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            movies = data.get("results", [])

            if not movies:  # Stop if no more movies
                break

            all_movies.extend(movies)
            page += 1

            # Store data in cache file to avoid repeated API calls
            with open(CACHE_FILE, "w") as file:
                json.dump(all_movies, file, indent=4)

        else:
            print("❌ Error fetching movies:", response.status_code)
            break

    return all_movies

# Function to load movies from cache
def load_cached_movies():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as file:
            return json.load(file)
    return None

# Get available genres
genre_dict = get_genres()

# Display available genres
print("\n🎬 Available Genres:")
for genre in genre_dict.keys():
    print(f"- {genre.capitalize()}")

# Get user input
preferred_genre = input("\nEnter your preferred genre from the list: ").strip().lower()
disliked_genre = input("Enter a genre to exclude (optional): ").strip().lower()

# Validate user input
preferred_genre_id = genre_dict.get(preferred_genre)
disliked_genre_id = genre_dict.get(disliked_genre)

if not preferred_genre_id:
    print("\n❌ Invalid genre! Please choose from the list above.")
    exit()

# Check cache first, otherwise fetch from TMDB
movies = load_cached_movies() or fetch_movies(preferred_genre_id)

# ✅ Step 1: Get the total number of movies fetched (before filtering)
total_movies = len(movies)

# ✅ Step 2: Filter movies based on preferred and disliked genres
filtered_movies = []
for movie in movies:
    movie_genres = movie.get("genre_ids", [])

    # Movie must contain the preferred genre
    if preferred_genre_id in movie_genres:
        # Movie must NOT contain the disliked genre (if specified)
        if not disliked_genre_id or disliked_genre_id not in movie_genres:
            filtered_movies.append(movie)

# ✅ Step 3: Get the number of movies after filtering
available_movies = len(filtered_movies)
availableMovies = available_movies - 1

# ✅ Step 4: Print correct numbers before asking for user input
print(f"\nThere are {total_movies} movies available.")
print(f"There are {availableMovies} movies selected based on your preferences.")

# ✅ Step 5: Ask user how many movies they want to see
while True:
    num_movies = input(f"How many do you want to see? ").strip()
    if num_movies.isdigit():
        num_movies = int(num_movies)
        if 0 < num_movies <= available_movies:
            break
    print(f"❌ Please enter a number between 1 and {available_movies}.")

# Display results
print("\n🎬 Recommended Movies:")
for i, movie in enumerate(filtered_movies[:num_movies], start=1):
    title = movie.get("title", "Unknown Title")
    release_date = movie.get("release_date", "Unknown Date")
    overview = movie.get("overview", "No description available.")
    print(f"{i}. {title} ({release_date})")
    print(f"   Overview: {overview}\n")
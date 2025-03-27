# import requests
# import os
# from dotenv import load_dotenv

# # Load API keys
# load_dotenv()
# API_KEY = os.getenv("TMDB_API_KEY")

# # Genre mapping
# genre_dict = {
#     "action": 28, "adventure": 12, "animation": 16, "comedy": 35, "crime": 80,
#     "documentary": 99, "drama": 18, "family": 10751, "fantasy": 14, "history": 36,
#     "horror": 27, "music": 10402, "mystery": 9648, "romance": 10749, 
#     "science fiction": 878, "tv movie": 10770, "thriller": 53, "war": 10752, "western": 37
# }

# # Display available genres to the user
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

# # Ask how many movies to show
# while True:
#     num_movies = input("\nHow many movies do you want to see? (5 or 10): ").strip()
#     if num_movies.isdigit() and int(num_movies) in [5, 10]:
#         num_movies = int(num_movies)
#         break
#     print("❌ Please enter a valid number (5 or 10).")

# # Fetch movies from TMDB based on user's preferred genre
# url = f"https://api.themoviedb.org/3/discover/movie?api_key={API_KEY}&with_genres={preferred_genre_id}"
# response = requests.get(url)

# if response.status_code == 200:
#     data = response.json()
#     movies = data.get("results", [])

#     # Filter out movies containing the disliked genre and remove duplicates
#     filtered_movies = []
#     seen_movies = set()

#     for movie in movies:
#         movie_id = movie.get("id")
#         movie_genres = movie.get("genre_ids", [])

#         if disliked_genre_id and disliked_genre_id in movie_genres:
#             continue  # Skip movie if it contains the disliked genre

#         if movie_id not in seen_movies:
#             seen_movies.add(movie_id)
#             filtered_movies.append(movie)

#     # Ensure the requested number of movies doesn't exceed available movies
#     if len(filtered_movies) < num_movies:
#         num_movies = len(filtered_movies)  # Adjust number if fewer movies are available

#     # Display results
#     if filtered_movies:
#         print("\n🎬 Recommended Movies:")
#         for i, movie in enumerate(filtered_movies[:num_movies], start=1):
#             title = movie.get("title", "Unknown Title")
#             release_date = movie.get("release_date", "Unknown Date")
#             overview = movie.get("overview", "No description available.")
#             print(f"{i}. {title} ({release_date})")
#             print(f"   Overview: {overview}\n")
#     else:
#         print("\nNo movies found that match your preferences.")
# else:
#     print("❌ Error fetching data:", response.status_code, response.text)

# import requests
# import os
# from dotenv import load_dotenv

# # Load API keys
# load_dotenv()
# API_KEY = os.getenv("TMDB_API_KEY")

# # Genre mapping
# genre_dict = {
#     "action": 28, "adventure": 12, "animation": 16, "comedy": 35, "crime": 80,
#     "documentary": 99, "drama": 18, "family": 10751, "fantasy": 14, "history": 36,
#     "horror": 27, "music": 10402, "mystery": 9648, "romance": 10749, 
#     "science fiction": 878, "tv movie": 10770, "thriller": 53, "war": 10752, "western": 37
# }

# # Display available genres to the user
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

# # Ask how many movies to show
# while True:
#     num_movies = input("\nHow many movies do you want to see? (Enter any number): ").strip()
#     if num_movies.isdigit() and int(num_movies) > 0:
#         num_movies = int(num_movies)
#         break
#     print("❌ Please enter a valid number greater than 0.")

# # Fetch movies from TMDB based on user's preferred genre
# url = f"https://api.themoviedb.org/3/discover/movie?api_key={API_KEY}&with_genres={preferred_genre_id}"
# response = requests.get(url)

# if response.status_code == 200:
#     data = response.json()
#     movies = data.get("results", [])

#     # Filter out movies containing the disliked genre and remove duplicates
#     filtered_movies = []
#     seen_movies = set()

#     for movie in movies:
#         movie_id = movie.get("id")
#         movie_genres = movie.get("genre_ids", [])

#         if disliked_genre_id and disliked_genre_id in movie_genres:
#             continue  # Skip movie if it contains the disliked genre

#         if movie_id not in seen_movies:
#             seen_movies.add(movie_id)
#             filtered_movies.append(movie)

#     # Ensure the requested number of movies doesn't exceed available movies
#     num_movies = min(num_movies, len(filtered_movies))

#     # Display results
#     if filtered_movies:
#         print("\n🎬 Recommended Movies:")
#         for i, movie in enumerate(filtered_movies[:num_movies], start=1):
#             title = movie.get("title", "Unknown Title")
#             release_date = movie.get("release_date", "Unknown Date")
#             overview = movie.get("overview", "No description available.")
#             print(f"{i}. {title} ({release_date})")
#             print(f"   Overview: {overview}\n")
#     else:
#         print("\nNo movies found that match your preferences.")
# else:
#     print("❌ Error fetching data:", response.status_code, response.text)



# import requests
# import os
# from dotenv import load_dotenv

# # Load API keys
# load_dotenv()
# API_KEY = os.getenv("TMDB_API_KEY")

# # Genre mapping
# genre_dict = {
#     "action": 28, "adventure": 12, "animation": 16, "comedy": 35, "crime": 80,
#     "documentary": 99, "drama": 18, "family": 10751, "fantasy": 14, "history": 36,
#     "horror": 27, "music": 10402, "mystery": 9648, "romance": 10749, 
#     "science fiction": 878, "tv movie": 10770, "thriller": 53, "war": 10752, "western": 37
# }

# # Display available genres to the user
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

# # Fetch movies from TMDB based on user's preferred genre
# url = f"https://api.themoviedb.org/3/discover/movie?api_key={API_KEY}&with_genres={preferred_genre_id}"
# response = requests.get(url)

# if response.status_code == 200:
#     data = response.json()
#     movies = data.get("results", [])

#     # Filter out movies containing the disliked genre and remove duplicates
#     filtered_movies = []
#     seen_movies = set()

#     for movie in movies:
#         movie_id = movie.get("id")
#         movie_genres = movie.get("genre_ids", [])

#         if disliked_genre_id and disliked_genre_id in movie_genres:
#             continue  # Skip movie if it contains the disliked genre

#         if movie_id not in seen_movies:
#             seen_movies.add(movie_id)
#             filtered_movies.append(movie)

#     available_movies = len(filtered_movies)

#     if available_movies == 0:
#         print("\nNo movies found that match your preferences.")
#         exit()

#     # Ask how many movies to show
#     while True:
#         num_movies = input(f"\nThere are {available_movies} movies available. How many do you want to see? ").strip()
#         if num_movies.isdigit() and 0 < int(num_movies) <= available_movies:
#             num_movies = int(num_movies)
#             break
#         print(f"❌ Please enter a number between 1 and {available_movies}.")

#     # Display results
#     print("\n🎬 Recommended Movies:")
#     for i, movie in enumerate(filtered_movies[:num_movies], start=1):
#         title = movie.get("title", "Unknown Title")
#         release_date = movie.get("release_date", "Unknown Date")
#         overview = movie.get("overview", "No description available.")
#         print(f"{i}. {title} ({release_date})")
#         print(f"   Overview: {overview}\n")
# else:
#     print("❌ Error fetching data:", response.status_code, response.text)
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

# Filter out movies containing the disliked genre
filtered_movies = []
for movie in movies:
    movie_genres = movie.get("genre_ids", [])
    if disliked_genre_id and disliked_genre_id in movie_genres:
        continue  # Skip movie if it contains the disliked genre
    filtered_movies.append(movie)

available_movies = len(filtered_movies)

if available_movies == 0:
    print("\nNo movies found that match your preferences.")
    exit()

# Ask how many movies to show
while True:
    num_movies = input(f"\nThere are {available_movies} movies available. How many do you want to see? ").strip()
    if num_movies.isdigit() and 0 < int(num_movies) <= available_movies:
        num_movies = int(num_movies)
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

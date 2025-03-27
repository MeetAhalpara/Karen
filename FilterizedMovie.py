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

# # Get user input
# preferred_genre = input("Enter your preferred genre (e.g., Action, Drama): ").strip().lower()
# disliked_genre = input("Enter a genre to exclude (optional, e.g., Horror): ").strip().lower()

# # Validate user input
# preferred_genre_id = genre_dict.get(preferred_genre)
# disliked_genre_id = genre_dict.get(disliked_genre)

# if not preferred_genre_id:
#     print("Invalid preferred genre. Please check the available genres and try again.")
#     exit()

# # Fetch movies from TMDB based on user's preferred genre
# url = f"https://api.themoviedb.org/3/discover/movie?api_key={API_KEY}&with_genres={preferred_genre_id}"
# response = requests.get(url)

# if response.status_code == 200:
#     data = response.json()
#     movies = data.get("results", [])

#     # Filter out movies containing the disliked genre
#     filtered_movies = []
#     for movie in movies:
#         movie_genres = movie.get("genre_ids", [])
#         if disliked_genre_id and disliked_genre_id in movie_genres:
#             continue  # Skip movie if it contains the disliked genre
#         filtered_movies.append(movie)

#     # Display results
#     if filtered_movies:
#         print("\n🎬 Recommended Movies:")
#         for i, movie in enumerate(filtered_movies, start=1):
#             print(f"{i}. {movie['title']} ({movie['release_date']})")
#             print(f"   Overview: {movie['overview']}\n")
#     else:
#         print("\nNo movies found that match your preferences.")
# else:
#     print("Error:", response.status_code, response.text)
# Display all Selected Movie
import requests
import os
from dotenv import load_dotenv

# Load API keys
load_dotenv()
API_KEY = os.getenv("TMDB_API_KEY")

# Genre mapping
genre_dict = {
    "action": 28, "adventure": 12, "animation": 16, "comedy": 35, "crime": 80,
    "documentary": 99, "drama": 18, "family": 10751, "fantasy": 14, "history": 36,
    "horror": 27, "music": 10402, "mystery": 9648, "romance": 10749, 
    "science fiction": 878, "tv movie": 10770, "thriller": 53, "war": 10752, "western": 37
}

# Display available genres to the user
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

# Fetch movies from TMDB based on user's preferred genre
url = f"https://api.themoviedb.org/3/discover/movie?api_key={API_KEY}&with_genres={preferred_genre_id}"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    movies = data.get("results", [])

    # Filter out movies containing the disliked genre
    filtered_movies = []
    for movie in movies:
        movie_genres = movie.get("genre_ids", [])
        if disliked_genre_id and disliked_genre_id in movie_genres:
            continue  # Skip movie if it contains the disliked genre
        filtered_movies.append(movie)

    # Display results
    if filtered_movies:
        print("\n🎬 Recommended Movies:")
        for i, movie in enumerate(filtered_movies[:10], start=1):  # Show top 10 movies
            print(f"{i}. {movie['title']} ({movie['release_date']})")
            print(f"   Overview: {movie['overview']}\n")
    else:
        print("\nNo movies found that match your preferences.")
else:
    print("Error:", response.status_code, response.text)

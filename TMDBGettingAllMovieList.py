import requests
import os
from dotenv import load_dotenv

# Load API keys
load_dotenv()
API_KEY = os.getenv("TMDB_API_KEY")

# Base URL for TMDB API
base_url = "https://api.themoviedb.org/3/movie/popular"
page = 1  # Start from page 1
all_movies = []  # Store all movies

while True:
    url = f"{base_url}?api_key={API_KEY}&page={page}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        movies = data.get("results", [])
        
        if not movies:  # If no movies are returned, stop the loop
            break

        all_movies.extend(movies)  # Add movies to the list

        # TMDB returns 20 movies per page. Stop if we reach the last page.
        if page >= data.get("total_pages", 1):  
            break

        page += 1  # Move to the next page
    else:
        print("Error:", response.status_code, response.text)
        break

# Print all movies
for i, movie in enumerate(all_movies, start=1):
    print(f"{i}. {movie['title']} ({movie['release_date']})")
    print(f"   Overview: {movie['overview']}\n")

print(f"Total movies fetched: {len(all_movies)}")
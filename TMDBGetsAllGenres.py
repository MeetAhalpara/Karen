import requests
import os
from dotenv import load_dotenv

# Load API keys
load_dotenv()
API_KEY = os.getenv("TMDB_API_KEY")

# Get the list of genres from TMDB
url = f"https://api.themoviedb.org/3/genre/movie/list?api_key={API_KEY}&language=en-US"
response = requests.get(url)

if response.status_code == 200:
    genres = response.json()["genres"]
    genre_dict = {genre["name"].lower(): genre["id"] for genre in genres}

    print("Available genres:")
    for name, id in genre_dict.items():
        print(f"{name.capitalize()} - ID: {id}")
else:
    print("Error fetching genres:", response.status_code)

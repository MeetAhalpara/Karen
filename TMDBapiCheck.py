# import requests

# API_KEY = "eaf7e6e126b75caff6815c2103b6b5b6"  # Replace with your API key
# url = f"https://api.themoviedb.org/3/movie/popular?api_key={API_KEY}"
# data = {
#     "page": 1,
#     "results": [
#         {
#             "title": "The Gorge",
#             "release_date": "2025-02-13",
#             "vote_average": 7.826
#         },
#         {
#             "title": "Mufasa: The Lion King",
#             "release_date": "2024-12-18",
#             "vote_average": 7.5
#         }
#     ]
# }

# response = requests.get(url)

# if response.status_code == 200:
#     print(response.json())  # Print movie data
# else:
#     print("Error:", response.status_code, response.text)
# for movie in data["results"]:
#     print(f"Title: {movie['title']}, Release Date: {movie['release_date']}, Rating: {movie['vote_average']}")
# import requests

# API_BEARER_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJlYWY3ZTZlMTI2Yjc1Y2FmZjY4MTVjMjEwM2I2YjViNiIsIm5iZiI6MTc0MDUxMDY2NC40NzksInN1YiI6IjY3YmUxNWM4MTBiNDY1ZGEwMjU2MTEwNiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.dwYda8xcuilgdSW-Nh3EZaUvZxZFzT6JNbaUFbtiw8I"  # Replace with your Bearer Token
# url = "https://api.themoviedb.org/3/movie/popular"

# headers = {
#     "accept": "application/json",
#     "Authorization": f"Bearer {API_BEARER_TOKEN}"
# }

# response = requests.get(url, headers=headers)

# if response.status_code == 200:
#     print(response.json())  # Print movie data
# else:
#     print("Error:", response.status_code, response.text)
# data = {
#     "page": 1,
#     "results": [
#         {
#             "title": "The Gorge",
#             "release_date": "2025-02-13",
#             "vote_average": 7.826
#         },
#         {
#             "title": "Mufasa: The Lion King",
#             "release_date": "2024-12-18",
#             "vote_average": 7.5
#         }
#     ]
# }
# for movie in data["results"]:
#     print(f"Title: {movie['title']}, Release Date: {movie['release_date']}, Rating: {movie['vote_average']}")